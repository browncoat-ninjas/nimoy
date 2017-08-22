import unittest
from nimoy.ast_tools.ast_metadata import SpecMetadata


class TestSpecMetadata(unittest.TestCase):
    def test_setters(self):
        spec_metadata = SpecMetadata('spec_name')
        spec_metadata.set_owning_module('the_module')

        self.assertEqual(spec_metadata.name, 'spec_name')
        self.assertEqual(spec_metadata.owning_module, 'the_module')
