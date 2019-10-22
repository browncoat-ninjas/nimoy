from nimoy.ast_tools.specs import SpecTransformer


def apply(spec_location, node):
    spec_metadata = []

    SpecTransformer(spec_location, spec_metadata).visit(node)
    return spec_metadata
