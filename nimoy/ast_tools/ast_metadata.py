import copy


class SpecMetadata:
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
        self.owning_module = None
        self.features = []
        self.feature_blocks = {}
        self.feature_variables = {}

    def set_owning_module(self, owning_module):
        self.owning_module = owning_module

    def add_feature(self, feature_name):
        self.features.append(feature_name)
        self.feature_blocks[feature_name] = []
        self.feature_variables[feature_name] = {}

    def add_feature_block(self, feature_name, block_type):
        self.feature_blocks[feature_name].append(block_type)

    def add_feature_variable_values(self, feature_name, variable_name, values):
        if not self.feature_variables[feature_name].get(variable_name):
            self.feature_variables[feature_name][variable_name] = []
        self.feature_variables[feature_name][variable_name].extend(values)

    def add_feature_variable_value(self, feature_name, variable_name, value):
        if not self.feature_variables[feature_name].get(variable_name):
            self.feature_variables[feature_name][variable_name] = []
        self.feature_variables[feature_name][variable_name].append(value)

    def clone_feature(self, original_feature_name, cloned_feature_name):
        self.features.append(cloned_feature_name)
        self.feature_blocks[cloned_feature_name] = copy.deepcopy(self.feature_blocks[original_feature_name])
