from unittest import TestCase
from nimoy.context.feature_block_context import FeatureBlock
from nimoy.compare.internal import Compare


class Specification(TestCase):
    def _feature_block_context(self, block_name):
        return FeatureBlock(block_name)

    def _compare(self, left, right, comparison_type_name):
        Compare().compare(left, right, comparison_type_name)
