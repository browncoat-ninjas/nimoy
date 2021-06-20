from nimoy.ast_tools.specs import SpecTransformer
from nimoy.runner.metadata import RunnerContext


def apply(runner_context: RunnerContext, spec_location, node):
    spec_metadata = []

    SpecTransformer(runner_context, spec_location, spec_metadata).visit(node)
    return spec_metadata
