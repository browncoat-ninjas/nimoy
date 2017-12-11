class SpecMetadata:
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
        self.owning_module = None
        self.features = []
        self.feature_blocks = {}
        self.feature_variables = {}
        self.where_functions = {}

    def set_owning_module(self, owning_module):
        self.owning_module = owning_module

    def add_feature(self, feature_name):
        self.features.append(feature_name)
        self.feature_blocks[feature_name] = []
        self.feature_variables[feature_name] = {}

    def add_feature_block(self, feature_name, block_type):
        self.feature_blocks[feature_name].append(block_type)

    def add_feature_variable(self, feature_name, variable_name):
        if not self.feature_variables[feature_name]:
            self.feature_variables[feature_name] = []
        self.feature_variables[feature_name].append(variable_name)

    def add_where_function(self, feature_name, where_function):
        self.where_functions[feature_name] = where_function
