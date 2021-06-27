from unittest import mock
from nimoy.specification import Specification


class FeatureBlockRuleEnforcerSpec(Specification):
    def where_function_is_called_before_feature(self):
        with expect:
            class SomeSpec(Specification):
                def test_something(self, where_visited=False):
                    where_visited == True

                def test_something_where(self, data_to_inject):
                    isinstance(data_to_inject, dict) == True
                    data_to_inject['where_visited'] = [True]

            SomeSpec().test_something()

    def normal_feature_is_called(self):
        with expect:
            class SomeSpec(Specification):
                def test_something(self, where_visited=False):
                    where_visited == False

            SomeSpec().test_something()


class InternalSpecificationMethodsSpec(Specification):

    # By default the unittest mock fails when a mocked method begins with the string "assert" or "assret"
    @staticmethod
    def _mark_mock_as_unsafe(m):
        m.return_value._mock_unsafe = True

    def feature_block_context_is_returned(self):
        with given:
            class SomeSpec(Specification):
                pass

            spec = SomeSpec()

        with when:
            feature_block = spec._feature_block_context('jimbob')

        with then:
            feature_block.block_type == 'jimbob'
            feature_block.thrown_exceptions == spec.thrown_exceptions

    @mock.patch('nimoy.specification.Compare')
    def internal_comparison_is_called(self, compare_mock):
        with given:
            class SomeSpec(Specification):
                pass

        with when:
            SomeSpec()._compare('a', 'b', 'some_name')

        with then:
            1 * compare_mock.return_value.compare('a', 'b', 'some_name')

    @mock.patch('nimoy.specification.PowerAssertions')
    def internal_power_assertion_is_called(self, power_assert_mock):
        with given:
            InternalSpecificationMethodsSpec._mark_mock_as_unsafe(power_assert_mock)

            class SomeSpec(Specification):
                pass

        with when:
            SomeSpec()._power_assert({'a': 'b'})

        with then:
            1 * power_assert_mock.return_value.assert_and_raise({'a': 'b'})

    @mock.patch('nimoy.specification.MockAssertions')
    def internal_mock_assertion_is_performed(self, mock_assertions_mock):
        with given:
            InternalSpecificationMethodsSpec._mark_mock_as_unsafe(mock_assertions_mock)

            class SomeSpec(Specification):
                pass

            some_mock = mock.Mock()
            args = ['a', 'b']

        with when:
            SomeSpec()._assert_mock(1, some_mock, 'some_method', args)

        with then:
            1 * mock_assertions_mock.return_value.assert_mock(1, some_mock, 'some_method', args)

    @mock.patch('nimoy.specification.ExceptionAssertions')
    def internal_exception_assertion_is_performed(self, exception_assertions_mock):
        with given:
            InternalSpecificationMethodsSpec._mark_mock_as_unsafe(exception_assertions_mock)

            class SomeSpec(Specification):
                pass

            spec = SomeSpec()

        with when:
            spec._exception_thrown(ArithmeticError)

        with then:
            1 * exception_assertions_mock.return_value.assert_exception(spec.thrown_exceptions, ArithmeticError)
