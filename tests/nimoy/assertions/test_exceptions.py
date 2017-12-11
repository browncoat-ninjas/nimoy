import unittest

from nimoy.assertions.exceptions import ExceptionAssertions


class TestExceptionAssertions(unittest.TestCase):

    def test_no_exceptions_were_ever_thrown(self):
        with self.assertRaises(AssertionError):
            ExceptionAssertions().assert_exception([], ArithmeticError)

    def test_different_type_of_exception_was_thrown(self):
        with self.assertRaises(AssertionError):
            ExceptionAssertions().assert_exception([(Exception, None, None)], ArithmeticError)

    def test_successful_exception_assertion(self):
        thrown = (ArithmeticError, None, None)
        returned_exception = ExceptionAssertions().assert_exception([thrown], ArithmeticError)
        self.assertEqual(returned_exception, thrown)
