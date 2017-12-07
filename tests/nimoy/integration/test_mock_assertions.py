import unittest
from tests.nimoy.integration.base_integration_test import BaseIntegrationTest


class TestMockAssertions(BaseIntegrationTest):
    def test_successful_assertion(self):
        spec_contents = """from unittest import mock
from nimoy.specification import Specification


class JimbobSpec(Specification):
    def test(self):
        with setup:
            the_mock = mock.Mock()
        with when:
            the_mock.some_method()
        with then:
            1 * the_mock.some_method()
        """

        result = self._run_spec_contents(spec_contents)
        self.assertTrue(result.wasSuccessful())

    def test_successful_chained_mock_assertion(self):
        spec_contents = """from unittest import mock
from nimoy.specification import Specification


class JimbobSpec(Specification):
    def test(self):
        with setup:
            the_mock = mock.Mock()
        with when:
            the_mock.some_method().then_do_something().or_another()
        with then:
            1 * the_mock.some_method()
            1 * the_mock.some_method.return_value.then_do_something()
            1 * the_mock.some_method.return_value.then_do_something.return_value.or_another()
        """

        result = self._run_spec_contents(spec_contents)
        self.assertTrue(result.wasSuccessful())

    def test_successful_chained_mock_assertion_with_arguments(self):
        spec_contents = """from unittest import mock
from nimoy.specification import Specification


class JimbobSpec(Specification):
    def test(self):
        with setup:
            the_mock = mock.Mock()
        with when:
            the_mock.some_method(1).then_do_something("a").or_another(True)
        with then:
            1 * the_mock.some_method(1)
            1 * the_mock.some_method.return_value.then_do_something("a")
            1 * the_mock.some_method.return_value.then_do_something.return_value.or_another(True)
        """

        result = self._run_spec_contents(spec_contents)
        self.assertTrue(result.wasSuccessful())

    def test_failed_chained_mock_assertion_with_arguments(self):
        spec_contents = """from unittest import mock
from nimoy.specification import Specification


class JimbobSpec(Specification):
    def test(self):
        with setup:
            the_mock = mock.Mock()
        with when:
            the_mock.some_method(1).then_do_something("a").or_another(True)
        with then:
            1 * the_mock.some_method(1)
            1 * the_mock.some_method.return_value.then_do_something("b")
            1 * the_mock.some_method.return_value.then_do_something.return_value.or_another(True)
        """

        result = self._run_spec_contents(spec_contents)
        self.assertFalse(result.wasSuccessful())

    def test_failed_invocation_count_assertion(self):
        spec_contents = """from unittest import mock
from nimoy.specification import Specification


class JimbobSpec(Specification):
    def test(self):
        with setup:
            the_mock = mock.Mock()
        with when:
            the_mock.some_method()
        with then:
            0 * the_mock.some_method()
        """

        result = self._run_spec_contents(spec_contents)
        self.assertFalse(result.wasSuccessful())

    def test_successful_assertion_with_arguments(self):
        spec_contents = """from unittest import mock
from nimoy.specification import Specification


class JimbobSpec(Specification):
    def test(self):
        with setup:
            the_mock = mock.Mock()
        with when:
            the_mock.some_method('abcd', True)
        with then:
            1 * the_mock.some_method('abcd', True)
        """

        result = self._run_spec_contents(spec_contents)
        self.assertTrue(result.wasSuccessful())

    @unittest.skip("TODO: Implement spread mock assertions")
    def test_successful_spread_assertion_with_arguments(self):
        spec_contents = """from unittest import mock
from nimoy.specification import Specification


class JimbobSpec(Specification):
    def test(self):
        with setup:
            the_mock = mock.Mock()
        with when:
            the_mock.some_method('abcd', True)
            the_mock.some_method('efgh', False)
            the_mock.some_method('abcd', True)
        with then:
            1 * the_mock.some_method('abcd', True)
            1 * the_mock.some_method('efgh', False)
            1 * the_mock.some_method('abcd', True)
        """

        result = self._run_spec_contents(spec_contents)
        self.assertTrue(result.wasSuccessful())

    def test_failed_invocation_count_assertion_with_arguments(self):
        spec_contents = """from unittest import mock
from nimoy.specification import Specification


class JimbobSpec(Specification):
    def test(self):
        with setup:
            the_mock = mock.Mock()
        with when:
            the_mock.some_method('abcd', True)
        with then:
            0 * the_mock.some_method('abcd', False)
        """

        result = self._run_spec_contents(spec_contents)
        self.assertFalse(result.wasSuccessful())

    def test_failed_argument_assertion(self):
        spec_contents = """from unittest import mock
from nimoy.specification import Specification


class JimbobSpec(Specification):
    def test(self):
        with setup:
            the_mock = mock.Mock()
        with when:
            the_mock.some_method('abcd', True)
        with then:
            1 * the_mock.some_method('abcd', False)
        """

        result = self._run_spec_contents(spec_contents)
        self.assertFalse(result.wasSuccessful())

    def test_failed_argument_assertion_with_wildcard(self):
        spec_contents = """from unittest import mock
from nimoy.specification import Specification


class JimbobSpec(Specification):
    def test(self):
        with setup:
            the_mock = mock.Mock()
        with when:
            the_mock.some_method('abcd', True)
        with then:
            1 * the_mock.some_method(_, False)
        """

        result = self._run_spec_contents(spec_contents)
        self.assertFalse(result.wasSuccessful())

    def test_successful_assertion_with_wild_card_invocation_count(self):
        spec_contents = """from unittest import mock
from nimoy.specification import Specification


class JimbobSpec(Specification):
    def test(self):
        with setup:
            the_mock = mock.Mock()
        with when:
            the_mock.some_method('abcd', True)
        with then:
            _ * the_mock.some_method('abcd', True)
        """

        result = self._run_spec_contents(spec_contents)
        self.assertTrue(result.wasSuccessful())

    def test_successful_assertion_with_wild_card_argument(self):
        spec_contents = """from unittest import mock
from nimoy.specification import Specification


class JimbobSpec(Specification):
    def test(self):
        with setup:
            the_mock = mock.Mock()
        with when:
            the_mock.some_method('abcd', True)
        with then:
            1 * the_mock.some_method(_, True)
        """

        result = self._run_spec_contents(spec_contents)
        self.assertTrue(result.wasSuccessful())

    def test_successful_assertion_with_reference_argument(self):
        spec_contents = """from unittest import mock
from nimoy.specification import Specification


class JimbobSpec(Specification):
    def test(self):
        with setup:
            a = 3
            the_mock = mock.Mock()
        with when:
            the_mock.some_method(3, True)
        with then:
            1 * the_mock.some_method(a, True)
        """

        result = self._run_spec_contents(spec_contents)
        self.assertTrue(result.wasSuccessful())
