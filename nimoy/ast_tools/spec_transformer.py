import ast
import _ast
from nimoy.ast_tools.ast_metadata import SpecMetadata
from nimoy.ast_tools.method_registration_transformer import MethodRegistrationTransformer


class SpecTransformer(ast.NodeTransformer):
    def __init__(self, spec_metadata) -> None:
        super().__init__()
        self.spec_metadata = spec_metadata

    def visit_ClassDef(self, class_node):
        if class_node.name.endswith('Spec'):
            SpecTransformer.extend_spec_from_test_case(class_node)

            metadata = SpecMetadata(class_node.name)
            self._register_spec(metadata)
            MethodRegistrationTransformer(metadata).visit(class_node)

        return class_node

    @staticmethod
    def extend_spec_from_test_case(class_node):
        class_node.bases.append(_ast.Attribute(
            value=_ast.Name(id='unittest', ctx=_ast.Load()),
            attr='TestCase',
            ctx=_ast.Load()
        ))

    def _register_spec(self, metadata):
        self.spec_metadata.append(metadata)
