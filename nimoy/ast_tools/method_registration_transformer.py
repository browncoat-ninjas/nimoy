import ast


class MethodRegistrationTransformer(ast.NodeVisitor):
    def __init__(self, spec_metadata) -> None:
        super().__init__()
        self.spec_metadata = spec_metadata

    def visit_FunctionDef(self, function_node):
        if not function_node.name.startswith('_'):
            self.spec_metadata.add_test_method(function_node.name)
