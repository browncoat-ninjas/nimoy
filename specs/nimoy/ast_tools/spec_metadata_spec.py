from nimoy.specification import Specification
from nimoy.ast_tools.ast_metadata import SpecMetadata


class SpecMetadataSpec(Specification):
    def setters(self):
        with given:
            spec_metadata = SpecMetadata('spec_name')
            spec_metadata.set_owning_module('the_module')
            spec_metadata.add_feature('the_feature')
            spec_metadata.add_feature('the_feature2')
            spec_metadata.add_feature_block('the_feature', 'block_type')
            spec_metadata.add_feature_variable('the_feature', 'var_a')
            spec_metadata.add_feature_variable('the_feature2', 'var_b')
            spec_metadata.add_where_function('the_where', {})

        with expect:
            spec_metadata.name == 'spec_name'
            spec_metadata.owning_module == 'the_module'
            spec_metadata.features[0] == 'the_feature'
            spec_metadata.features[1] == 'the_feature2'
            spec_metadata.feature_blocks['the_feature'][0] == 'block_type'
            spec_metadata.feature_variables['the_feature'] == ['var_a']
            spec_metadata.feature_variables['the_feature2'] == ['var_b']
            spec_metadata.where_functions['the_where'] == {}
