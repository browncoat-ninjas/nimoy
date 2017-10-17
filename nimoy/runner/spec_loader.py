import ast


class SpecLoader:
    def __init__(self, ast_chain) -> None:
        super().__init__()
        self.ast_chain = ast_chain

    def load(self, spec_contents):
        def specs():
            for spec_file_location, text in spec_contents:
                node = ast.parse(text, mode='exec')

                metadata_of_specs_from_node = self.ast_chain.apply(node)
                ast.fix_missing_locations(node)
                compiled = compile(node, spec_file_location, 'exec')

                spec_namespace = {}
                exec(compiled, spec_namespace)

                for spec_metadata in metadata_of_specs_from_node:
                    spec_metadata.set_owning_module(spec_namespace[spec_metadata.name])
                    yield spec_metadata

        return specs()
