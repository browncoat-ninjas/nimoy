class SpecMetadata:
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
        self.owning_module = None
        self.methods = []

    def set_owning_module(self, owning_module):
        self.owning_module = owning_module

    def add_test_method(self, test_method):
        self.methods.append(test_method)
