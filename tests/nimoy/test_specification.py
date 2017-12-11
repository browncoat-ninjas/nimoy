import unittest
from unittest import mock
from nimoy.specification import Specification


class FeatureBlockRuleEnforcerTest(unittest.TestCase):
    def test_that_where_function_is_called_before_feature(self):
        class SomeSpec(Specification):
            def test_something(self, where_visited=False):
                self.assertTrue(where_visited)

            def test_something_where(self, data_to_inject):
                assert isinstance(data_to_inject, dict)
                data_to_inject['where_visited'] = [True]

        SomeSpec().test_something()

    def test_that_normal_feature_is_called(self):
        class SomeSpec(Specification):
            def test_something(self, where_visited=False):
                self.assertFalse(where_visited)

        SomeSpec().test_something()


class InternalSpecificationMethodsTest(unittest.TestCase):
    def test_that_a_feature_block_context_is_returned(self):
        class SomeSpec(Specification):
            pass

        spec = SomeSpec()
        feature_block = spec._feature_block_context('jimbob')
        self.assertEqual(feature_block.block_type, 'jimbob')
        self.assertEqual(feature_block.thrown_exceptions, spec.thrown_exceptions)

    @mock.patch('nimoy.specification.Compare')
    def test_that_internal_comparison_is_called(self, compare_mock):
        class SomeSpec(Specification):
            pass

        SomeSpec()._compare('a', 'b', 'some_name')
        compare_mock.return_value.compare.assert_called_with('a', 'b', 'some_name')

    @mock.patch('nimoy.specification.MockAssertions')
    def test_that_internal_mock_assertion_is_performed(self, mock_assertions_mock):
        mock_assertions_mock.return_value._mock_unsafe = True

        class SomeSpec(Specification):
            pass

        some_mock = mock.Mock()
        args = ['a', 'b']
        SomeSpec()._assert_mock(1, some_mock, 'some_method', args)
        mock_assertions_mock.return_value.assert_mock.assert_called_with(1, some_mock, 'some_method', args)

    @mock.patch('nimoy.specification.ExceptionAssertions')
    def test_that_internal_exception_assertion_is_performed(self, exception_assertions_mock):
        exception_assertions_mock.return_value._mock_unsafe = True

        class SomeSpec(Specification):
            pass

        spec = SomeSpec()
        spec._exception_thrown(ArithmeticError)
        exception_assertions_mock.return_value.assert_exception.assert_called_with(spec.thrown_exceptions,
                                                                                   ArithmeticError)
