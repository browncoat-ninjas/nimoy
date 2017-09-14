import ast
from nimoy.ast_tools.feature_blocks import FeatureBlockTransformer
from nimoy.ast_tools.feature_blocks import FeatureBlockRuleEnforcer


class FeatureRegistrationTransformer(ast.NodeVisitor):
    def __init__(self, spec_metadata) -> None:
        super().__init__()
        self.spec_metadata = spec_metadata

    def visit_FunctionDef(self, feature_node):
        feature_name = feature_node.name
        if not feature_name.startswith('_'):
            self.spec_metadata.add_feature(feature_name)
            FeatureBlockTransformer(self.spec_metadata, feature_name).visit(feature_node)
            FeatureBlockRuleEnforcer(self.spec_metadata, feature_name, feature_node).enforce_tail_end_rules()
