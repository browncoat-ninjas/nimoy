from nimoy.ast_tools.spec_transformer import SpecTransformer


def apply(node):
    spec_metadata = []

    SpecTransformer(spec_metadata).visit(node)
    return spec_metadata
