import re

from nimoy.specification import Specification
from nimoy.compare.internal import Compare
from nimoy.compare.types import Types


class InternalComparatorSpec(Specification):

    def compare_method(self):
        with given:
            compare = Compare()

        with expect:
            compare.compare(left, right, type_name)

        with where:
            left                  | right               | type_name
            1                     | 1                   | Types.EQUAL.name
            2                     | 1                   | Types.NOT_EQUAL.name
            1                     | 2                   | Types.LESS_THAN.name
            1                     | 2                   | Types.LESS_THAN_EQUAL.name
            2                     | 2                   | Types.LESS_THAN_EQUAL.name
            2                     | 1                   | Types.GREATER_THAN.name
            2                     | 2                   | Types.GREATER_THAN_EQUAL.name
            True                  | True                | Types.IS.name
            True                  | False               | Types.IS_NOT.name
            1                     | [1, 2]              | Types.IN.name
            1                     | [3, 2]              | Types.NOT_IN.name
            'The quick brown fox' | re.compile('brown') | Types.MATCHES_REGEXP.name
