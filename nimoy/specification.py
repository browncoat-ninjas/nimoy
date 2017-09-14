from unittest import TestCase
from nimoy.context.feature_block_context import FeatureBlock


class Specification(TestCase):
    def _feature_block_context(self, block_name):
        return FeatureBlock(block_name)
