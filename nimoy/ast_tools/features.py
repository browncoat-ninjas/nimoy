import ast
import _ast
from nimoy.ast_tools.feature_blocks import FeatureBlockTransformer
from nimoy.ast_tools.feature_blocks import FeatureBlockRuleEnforcer


class FeatureRegistrationTransformer(ast.NodeTransformer):
    def __init__(self, spec_metadata) -> None:
        super().__init__()
        self.spec_metadata = spec_metadata

    def visit_FunctionDef(self, feature_node):
        feature_name = feature_node.name
        if not feature_name.startswith('_'):
            self.spec_metadata.add_feature(feature_name)
            FeatureBlockTransformer(self.spec_metadata, feature_name).visit(feature_node)
            FeatureBlockRuleEnforcer(self.spec_metadata, feature_name, feature_node).enforce_tail_end_rules()

        feature_variables = self.spec_metadata.feature_variables.get(feature_name)
        if feature_variables:
            for feature_variable in feature_variables:
                feature_node.args.args.append(_ast.arg(arg=feature_variable))
                feature_node.args.defaults.append(_ast.NameConstant(value=None))
        return feature_node
