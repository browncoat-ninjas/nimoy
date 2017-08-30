from unittest import TestCase
from nimoy.context.method_block_context import MethodBlock


class Specification(TestCase):
    def _method_block_context(self, block_name):
        return MethodBlock(block_name)
