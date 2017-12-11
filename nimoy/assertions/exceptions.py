class ExceptionAssertions:
    def assert_exception(self, thrown_exceptions, expected_exception_type):
        if not thrown_exceptions:
            raise AssertionError("Expected an exception of type '%s' to be thrown" % expected_exception_type.__name__)

        thrown_exception = thrown_exceptions.pop()
        if thrown_exception[0] is not expected_exception_type:
            raise AssertionError("Expected an exception of type '%s' but found '%s'" % (
                expected_exception_type.__name__, thrown_exception[0].__name__))

        return thrown_exception
