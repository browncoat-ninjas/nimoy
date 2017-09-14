class SpecExecutor:
    def __init__(self, execution_framework) -> None:
        super().__init__()
        self.execution_framework = execution_framework

    def execute(self, specs):
        suite = self.execution_framework.create_suite()

        for spec_metadata in specs:
            spec_class_module = spec_metadata.owning_module

            for spec_feature in spec_metadata.features:
                self.execution_framework.append_test(suite, spec_class_module(spec_feature))

        return self.execution_framework.run(suite)
