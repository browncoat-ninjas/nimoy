import unittest

from nimoy.assertions.exceptions import ExceptionAssertions


class TestExceptionAssertions(unittest.TestCase):

    def test_no_exceptions_were_ever_thrown(self):
        with self.assertRaises(AssertionError):
            ExceptionAssertions().assert_exception([], ArithmeticError)

    def test_different_type_of_exception_was_thrown(self):
        with self.assertRaises(AssertionError):
            thrown = (Exception, Exception(), None)
            ExceptionAssertions().assert_exception([thrown], ArithmeticError)

    def test_successful_exception_assertion(self):
        thrown = (ArithmeticError, ArithmeticError(), None)
        returned_exception = ExceptionAssertions().assert_exception([thrown], ArithmeticError)
        self.assertEqual(returned_exception, thrown)

    def test_successful_derived_exception_assertion(self):
        thrown = (ArithmeticError, ArithmeticError(), None)
        returned_exception = ExceptionAssertions().assert_exception([thrown], Exception)
        self.assertEqual(returned_exception, thrown)
