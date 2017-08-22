class SpecMetadata:
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
        self.owning_module = None

    def set_owning_module(self, owning_module):
        self.owning_module = owning_module
