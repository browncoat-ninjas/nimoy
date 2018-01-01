from nimoy.assertions.exceptions import ExceptionAssertions
from nimoy.specification import Specification


class ExceptionAssertionsSpec(Specification):

    def no_exceptions_were_even_thrown(self):
        with when:
            ExceptionAssertions().assert_exception([], ArithmeticError)
        with then:
            thrown(AssertionError)

    def different_exception_was_thrown(self):
        with when:
            ExceptionAssertions().assert_exception([(Exception, Exception(), None)], ArithmeticError)
        with then:
            thrown(AssertionError)

    def successful_exception_assertion(self):
        with when:
            asserted = ExceptionAssertions().assert_exception([(thrown_type, thrown_type(), None)],
                                                              expected_type)
        with then:
            asserted[0] == thrown_type

        with where:
            thrown_type     | expected_type
            ArithmeticError | ArithmeticError
            ArithmeticError | Exception