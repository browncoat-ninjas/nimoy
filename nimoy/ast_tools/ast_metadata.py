class SpecMetadata:
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
        self.owning_module = None
        self.methods = []
        self.method_blocks = {}

    def set_owning_module(self, owning_module):
        self.owning_module = owning_module

    def add_test_method(self, test_method):
        self.methods.append(test_method)
        self.method_blocks[test_method] = []

    def add_method_block(self, test_method, block_type):
        self.method_blocks[test_method].append(block_type)
