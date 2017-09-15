import collections
import copy
import ast
import _ast
from nimoy.ast_tools.ast_metadata import SpecMetadata
from nimoy.ast_tools.features import FeatureRegistrationTransformer


class FeatureVariables:
    def __init__(self, spec_metadata) -> None:
        super().__init__()
        self.spec_metadata = spec_metadata

    def inject(self, spec_ast_node):
        features_that_require_injection = [feature_definition for feature_definition in spec_ast_node.body if
                                           (isinstance(feature_definition, _ast.FunctionDef) and
                                            self.spec_metadata.feature_variables[feature_definition.name])]

        for feature_that_requires_injection in features_that_require_injection:
            self._inject_feature_variables(spec_ast_node, feature_that_requires_injection)

    def _inject_feature_variables(self, specification_node, feature_that_requires_injection):
        feature_name = feature_that_requires_injection.name

        feature_variables = self.spec_metadata.feature_variables[feature_name]
        feature_variable_names = list(feature_variables.keys())

        tupled_feature_variables = FeatureVariables._get_feature_variables_as_tuples(feature_variable_names,
                                                                                     feature_variables)

        first_feature_index = specification_node.body.index(feature_that_requires_injection)
        if len(tupled_feature_variables) > 1:
            for index, variable_set in enumerate(tupled_feature_variables[1:]):
                feature_copy = copy.deepcopy(feature_that_requires_injection)
                feature_copy.name = "%s_%s" % (feature_name, str(index + 1))
                FeatureVariables._inject_features(feature_copy, feature_variable_names, variable_set)
                specification_node.body.insert(first_feature_index, feature_copy)
                self.spec_metadata.clone_feature(feature_name, feature_copy.name)

        first_feature_set = tupled_feature_variables[0]
        FeatureVariables._inject_features(feature_that_requires_injection, feature_variable_names, first_feature_set)

    @staticmethod
    def _get_feature_variables_as_tuples(feature_variable_names, feature_variables):
        iteration_variables = collections.namedtuple('iteration_variables', feature_variable_names)
        tupled_feature_variables = [iteration_variables(*t) for t in zip(
            *(feature_variables[feature_variable_name] for feature_variable_name in feature_variable_names))]
        return tupled_feature_variables

    @staticmethod
    def _inject_features(feature_copy, feature_variable_names, variable_set):
        for variable_name in feature_variable_names:
            feature_copy.args.args.append(_ast.arg(arg=variable_name))
            feature_copy.args.defaults.append(getattr(variable_set, variable_name))


class SpecTransformer(ast.NodeTransformer):
    def __init__(self, spec_metadata) -> None:
        super().__init__()
        self.spec_metadata = spec_metadata

    def visit_ClassDef(self, class_node):

        class_extends_spec = any(SpecTransformer._extends_spec(class_base) for class_base in class_node.bases)

        if class_extends_spec:
            metadata = SpecMetadata(class_node.name)
            self._register_spec(metadata)
            FeatureRegistrationTransformer(metadata).visit(class_node)
            FeatureVariables(metadata).inject(class_node)

        return class_node

    @staticmethod
    def _extends_spec(class_base):
        if not isinstance(class_base, _ast.Name):
            return False

        return class_base.id == 'Specification'

    def _register_spec(self, metadata):
        self.spec_metadata.append(metadata)
