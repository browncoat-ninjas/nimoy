from hamcrest import assert_that
from hamcrest import equal_to
from hamcrest import is_not
from hamcrest import less_than
from hamcrest import less_than_or_equal_to
from hamcrest import greater_than
from hamcrest import greater_than_or_equal_to
from hamcrest import is_
from hamcrest import is_in
from nimoy.compare.types import Types


class Compare:
    def compare(self, left, right, comparison_type_name):
        comparison_type = Types[comparison_type_name]
        self._select_comparison_method(left, right, comparison_type)

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
        else:
            raise Exception()
