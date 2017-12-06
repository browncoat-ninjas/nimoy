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
            existing_arg_names = [existing_arg.arg for existing_arg in feature_node.args.args]

            for feature_variable in feature_variables:
                if feature_variable in existing_arg_names:
                    continue
                feature_node.args.args.append(_ast.arg(arg=feature_variable))
                feature_node.args.defaults.append(_ast.NameConstant(value=None))

        if self._feature_has_a_where_function(feature_name):
            self._remove_where_function_from_node(feature_name, feature_node)
        return feature_node

    @staticmethod
    def _remove_where_function_from_node(feature_name, feature_node):
        where_function = FeatureRegistrationTransformer._locate_where_function_within_feature(feature_name,
                                                                                              feature_node)
        feature_node.body.remove(where_function)

    def _feature_has_a_where_function(self, feature_name):
        return self.spec_metadata.where_functions.get(feature_name)

    @staticmethod
    def _locate_where_function_within_feature(feature_name, feature_node):
        def _is_a_where_function(body_element):
            return hasattr(body_element, 'name') and body_element.name == feature_name + '_where'

        return next(body_element for body_element in feature_node.body if _is_a_where_function(body_element))
