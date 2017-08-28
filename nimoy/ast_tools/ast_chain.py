from nimoy.ast_tools.spec_transformer import SpecTransformer
from nimoy.ast_tools.module_transformer import ModuleTransformer


def apply(node):
    spec_metadata = []

    SpecTransformer(spec_metadata).visit(node)
    ModuleTransformer().visit(node)
    return spec_metadata
