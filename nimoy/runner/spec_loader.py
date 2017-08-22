import ast


class SpecLoader:
    def __init__(self, resource_reader, ast_chain) -> None:
        super().__init__()
        self.ast_chain = ast_chain
        self.resource_reader = resource_reader

    def load(self, spec_locations):
        specs = []

        for spec_file_location in spec_locations:
            text = self.resource_reader.read(spec_file_location)
            node = ast.parse(text, mode='exec')

            metadata_of_specs_from_node = self.ast_chain.apply(node)
            ast.fix_missing_locations(node)
            compiled = compile(node, spec_file_location, 'exec')

            spec_namespace = {}
            exec(compiled, spec_namespace)

            for spec_metadata in metadata_of_specs_from_node:
                spec_metadata.set_owning_module(spec_namespace[spec_metadata.name])
                specs.append(spec_metadata)

        return specs
