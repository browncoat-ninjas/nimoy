import ast
from nimoy.ast_tools.method_blocks import MethodBlockTransformer
from nimoy.ast_tools.method_blocks import MethodBlockRuleEnforcer


class MethodRegistrationTransformer(ast.NodeVisitor):
    def __init__(self, spec_metadata) -> None:
        super().__init__()
        self.spec_metadata = spec_metadata

    def visit_FunctionDef(self, function_node):
        method_name = function_node.name
        if not method_name.startswith('_'):
            self.spec_metadata.add_test_method(method_name)
            MethodBlockTransformer(self.spec_metadata, method_name).visit(function_node)
            MethodBlockRuleEnforcer(self.spec_metadata, method_name, function_node).enforce_tail_end_rules()
