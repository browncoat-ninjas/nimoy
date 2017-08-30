import ast
import _ast
from nimoy.ast_tools.ast_metadata import SpecMetadata
from nimoy.ast_tools.method_registration_transformer import MethodRegistrationTransformer


class SpecTransformer(ast.NodeTransformer):
    def __init__(self, spec_metadata) -> None:
        super().__init__()
        self.spec_metadata = spec_metadata

    def visit_ClassDef(self, class_node):

        class_extends_spec = any(SpecTransformer._extends_spec(class_base) for class_base in class_node.bases)

        if class_extends_spec:
            metadata = SpecMetadata(class_node.name)
            self._register_spec(metadata)
            MethodRegistrationTransformer(metadata).visit(class_node)

        return class_node

    @staticmethod
    def _extends_spec(class_base):
        if not isinstance(class_base, _ast.Name):
            return False

        return class_base.id == 'Specification'

    def _register_spec(self, metadata):
        self.spec_metadata.append(metadata)
