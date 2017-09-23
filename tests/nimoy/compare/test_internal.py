import unittest
from nimoy.compare.internal import Compare
from nimoy.compare.types import Types


class TestInternalComparator(unittest.TestCase):
    def test_compare_method(self):
        c = Compare()
        c.compare(1, 1, Types.EQUAL.name)
        c.compare(2, 1, Types.NOT_EQUAL.name)
        c.compare(1, 2, Types.LESS_THAN.name)
        c.compare(1, 2, Types.LESS_THAN_EQUAL.name)
        c.compare(2, 2, Types.LESS_THAN_EQUAL.name)
        c.compare(2, 1, Types.GREATER_THAN.name)
        c.compare(2, 2, Types.GREATER_THAN_EQUAL.name)
        c.compare(True, True, Types.IS.name)
        c.compare(True, False, Types.IS_NOT.name)
        c.compare(1, [1, 2], Types.IN.name)
        c.compare(1, [3, 2], Types.NOT_IN.name)
