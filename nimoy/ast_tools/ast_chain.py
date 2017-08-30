from nimoy.ast_tools.spec_transformer import SpecTransformer
from nimoy.ast_tools.method_block_transformer import MethodBlockTransformer


def apply(node):
    spec_metadata = []

    SpecTransformer(spec_metadata).visit(node)
    MethodBlockTransformer().visit(node)
    return spec_metadata
