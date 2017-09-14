import unittest
from nimoy.ast_tools.ast_metadata import SpecMetadata


class TestSpecMetadata(unittest.TestCase):
    def test_setters(self):
        spec_metadata = SpecMetadata('spec_name')
        spec_metadata.set_owning_module('the_module')
        spec_metadata.add_feature('the_feature')
        spec_metadata.add_feature('the_feature2')
        spec_metadata.add_feature_block('the_feature', 'block_type')
        spec_metadata.add_feature_variable_value('the_feature', 'a', 1)
        spec_metadata.add_feature_variable_values('the_feature2', 'b', [1, 2])

        self.assertEqual(spec_metadata.name, 'spec_name')
        self.assertEqual(spec_metadata.owning_module, 'the_module')
        self.assertEqual(spec_metadata.features[0], 'the_feature')
        self.assertEqual(spec_metadata.features[1], 'the_feature2')
        self.assertEqual(spec_metadata.feature_blocks['the_feature'][0], 'block_type')
        self.assertEqual(spec_metadata.feature_variables['the_feature']['a'], [1])
        self.assertEqual(spec_metadata.feature_variables['the_feature2']['b'], [1, 2])
