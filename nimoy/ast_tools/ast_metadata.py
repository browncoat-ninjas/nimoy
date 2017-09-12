import copy


class SpecMetadata:
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
        self.owning_module = None
        self.methods = []
        self.method_blocks = {}
        self.method_variables = {}

    def set_owning_module(self, owning_module):
        self.owning_module = owning_module

    def add_test_method(self, test_method):
        self.methods.append(test_method)
        self.method_blocks[test_method] = []
        self.method_variables[test_method] = {}

    def add_method_block(self, test_method, block_type):
        self.method_blocks[test_method].append(block_type)

    def add_method_variable_values(self, test_method, variable_name, values):
        if not self.method_variables[test_method].get(variable_name):
            self.method_variables[test_method][variable_name] = []
        self.method_variables[test_method][variable_name].extend(values)

    def add_method_variable_value(self, test_method, variable_name, value):
        if not self.method_variables[test_method].get(variable_name):
            self.method_variables[test_method][variable_name] = []
        self.method_variables[test_method][variable_name].append(value)

    def clone_method(self, original_method_name, cloned_method_name):
        self.methods.append(cloned_method_name)
        self.method_blocks[cloned_method_name] = copy.deepcopy(self.method_blocks[original_method_name])
