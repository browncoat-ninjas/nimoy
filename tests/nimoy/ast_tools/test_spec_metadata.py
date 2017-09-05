import unittest
from nimoy.ast_tools.ast_metadata import SpecMetadata


class TestSpecMetadata(unittest.TestCase):
    def test_setters(self):
        spec_metadata = SpecMetadata('spec_name')
        spec_metadata.set_owning_module('the_module')
        spec_metadata.add_test_method('the_method')
        spec_metadata.add_method_block('the_method', 'block_type')

        self.assertEqual(spec_metadata.name, 'spec_name')
        self.assertEqual(spec_metadata.owning_module, 'the_module')
        self.assertEqual(spec_metadata.methods[0], 'the_method')
        self.assertEqual(spec_metadata.method_blocks['the_method'][0], 'block_type')
