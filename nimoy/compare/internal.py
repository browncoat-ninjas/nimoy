import difflib
from hamcrest import assert_that
from hamcrest import equal_to
from hamcrest import is_not
from hamcrest import less_than
from hamcrest import less_than_or_equal_to
from hamcrest import greater_than
from hamcrest import greater_than_or_equal_to
from hamcrest import is_
from hamcrest import is_in
from hamcrest import matches_regexp
from nimoy.compare.types import Types


class Compare:
    def compare(self, left, right, comparison_type_name):
        comparison_type = Types[comparison_type_name]
        try:
            self._select_comparison_method(left, right, comparison_type)
        except AssertionError as assertion_error:
            error_message = Compare.__reformat_error_message(assertion_error, left, right)
            raise AssertionError(error_message) from None

    def _select_comparison_method(self, left, right, comparison_type):
        if comparison_type == Types.EQUAL:
            assert_that(left, equal_to(right))
        elif comparison_type == Types.NOT_EQUAL:
            assert_that(left, is_not(equal_to(right)))
        elif comparison_type == Types.LESS_THAN:
            assert_that(left, less_than(right))
        elif comparison_type == Types.LESS_THAN_EQUAL:
            assert_that(left, less_than_or_equal_to(right))
        elif comparison_type == Types.GREATER_THAN:
            assert_that(left, greater_than(right))
        elif comparison_type == Types.GREATER_THAN_EQUAL:
            assert_that(left, greater_than_or_equal_to(right))
        elif comparison_type == Types.IS:
            assert_that(left, is_(right))
        elif comparison_type == Types.IS_NOT:
            assert_that(left, is_not(right))
        elif comparison_type == Types.IN:
            assert_that(left, is_in(right))
        elif comparison_type == Types.NOT_IN:
            assert_that(left, is_not(is_in(right)))
        elif comparison_type == Types.MATCHES_REGEXP:
            assert_that(left, matches_regexp(right))
        else:
            raise Exception()

    @staticmethod
    def __reformat_error_message(assertion_error, left, right):
        error_message = str(assertion_error)
        if Compare.__is_string(left) and Compare.__is_string(right):
            differ = difflib.Differ()
            diff = differ.compare(left.split('\n'), right.split('\n'))
            error_message = "%sHint:\n%s" % (error_message, '\n'.join(diff))
        return error_message

    @staticmethod
    def __is_string(value):
        return isinstance(value, str)

    @staticmethod
    def __is_list(value):
        return isinstance(value, list)
