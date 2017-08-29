import ast
import _ast
from nimoy.ast_tools.ast_metadata import SpecMetadata


class SpecTransformer(ast.NodeTransformer):
    def __init__(self, spec_metadata) -> None:
        super().__init__()
        self.spec_metadata = spec_metadata

    def visit_ClassDef(self, class_node):
        if class_node.name.endswith('Spec'):
            self._register_spec(class_node)
            class_node.bases.append(_ast.Attribute(
                value=_ast.Name(id='unittest', ctx=_ast.Load()),
                attr='TestCase',
                ctx=_ast.Load()
            ))
        return class_node

    def _register_spec(self, class_node):
        self.spec_metadata.append(SpecMetadata(class_node.name))
