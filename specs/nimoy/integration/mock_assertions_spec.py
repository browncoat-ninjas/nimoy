from nimoy.specification import Specification
from nimoy.spec_runner import SpecRunner


class MockAssertionsSpec(Specification):
    def successful_assertion(self):
        with given:
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

        with when:
            result = self._run_spec_contents(spec_contents)
        with then:
            result.wasSuccessful() == True

    def successful_chained_mock_assertion(self):
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

        with when:
            result = self._run_spec_contents(spec_contents)
        with then:
            result.wasSuccessful() == True

    def successful_chained_mock_assertion_with_arguments(self):
        with given:
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

        with when:
            result = self._run_spec_contents(spec_contents)
        with then:
            result.wasSuccessful() == True

    def failed_chained_mock_assertion_with_arguments(self):
        with given:
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

        with when:
            result = self._run_spec_contents(spec_contents)
        with then:
            result.wasSuccessful() == False

    def failed_invocation_count_assertion(self):
        with given:
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

        with when:
            result = self._run_spec_contents(spec_contents)
        with then:
            result.wasSuccessful() == False

    def successful_assertion_with_arguments(self):
        with given:
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

        with when:
            result = self._run_spec_contents(spec_contents)
        with then:
            result.wasSuccessful() == True

    # @unittest.skip("TODO: Implement spread mock assertions")
    # def successful_spread_assertion_with_arguments(self):
    #     spec_contents = """from unittest import mock
# from nimoy.specification import Specification
#
#
# class JimbobSpec(Specification):
#     def test(self):
#         with setup:
#             the_mock = mock.Mock()
#         with when:
#             the_mock.some_method('abcd', True)
#             the_mock.some_method('efgh', False)
#             the_mock.some_method('abcd', True)
#         with then:
#             1 * the_mock.some_method('abcd', True)
#             1 * the_mock.some_method('efgh', False)
#             1 * the_mock.some_method('abcd', True)
#         """
#
#         result = self._run_spec_contents(spec_contents)
#         self.assertTrue(result.wasSuccessful())

    def failed_invocation_count_assertion_with_arguments(self):
        with given:
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

        with when:
            result = self._run_spec_contents(spec_contents)
        with then:
            result.wasSuccessful() == False

    def failed_argument_assertion(self):
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

        with when:
            result = self._run_spec_contents(spec_contents)
        with then:
            result.wasSuccessful() == False

    def failed_argument_assertion_with_wildcard(self):
        with given:
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

        with when:
            result = self._run_spec_contents(spec_contents)
        with then:
            result.wasSuccessful() == False

    def successful_assertion_with_wild_card_invocation_count(self):
        with given:
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

        with when:
            result = self._run_spec_contents(spec_contents)
        with then:
            result.wasSuccessful() == True

    def successful_assertion_with_wild_card_argument(self):
        with given:
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

        with when:
            result = self._run_spec_contents(spec_contents)
        with then:
            result.wasSuccessful() == True

    def successful_assertion_with_reference_argument(self):
        with given:
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

        with when:
            result = self._run_spec_contents(spec_contents)
        with then:
            result.wasSuccessful() == True

    def _run_spec_contents(self, spec_contents):
        return SpecRunner._run_on_contents([('/fake/path.py', spec_contents)])
