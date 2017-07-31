import ast


class SpecLoader:
    def __init__(self, resource_reader, ast_chain) -> None:
        super().__init__()
        self.ast_chain = ast_chain
        self.resource_reader = resource_reader

    def load(self, spec_locations):
        spec_metadata = {}

        for spec_location in spec_locations:
            text = self.resource_reader.read(spec_location)
            node = ast.parse(text, mode='exec')

            metadata = self.ast_chain.apply(node)
            ast.fix_missing_locations(node)
            compiled = compile(node, spec_location, mode='exec')
            exec(compiled)

            spec_metadata[metadata.get('class_name')] = metadata

        return spec_metadata
