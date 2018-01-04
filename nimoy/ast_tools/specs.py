import ast
import _ast
from nimoy.ast_tools.ast_metadata import SpecMetadata
from nimoy.ast_tools.features import FeatureRegistrationTransformer


class SpecTransformer(ast.NodeTransformer):
    def __init__(self, spec_metadata) -> None:
        super().__init__()
        self.spec_metadata = spec_metadata

    def visit_ClassDef(self, class_node):

        class_is_spec = class_node.name.endswith('Spec')

        if class_is_spec:
            metadata = SpecMetadata(class_node.name)
            self._register_spec(metadata)
            FeatureRegistrationTransformer(metadata).visit(class_node)

            for feature_name in metadata.where_functions:
                feature = next(
                    feature for feature in class_node.body if hasattr(feature, 'name') and feature_name == feature.name)
                index_of_feature = class_node.body.index(feature)

                index_to_insert_where = index_of_feature + 1
                where_function_to_insert = metadata.where_functions[feature_name]

                if (index_to_insert_where + 1) > len(class_node.body):
                    class_node.body.append(where_function_to_insert)
                else:
                    class_node.body.insert(index_to_insert_where, where_function_to_insert)

        return class_node

    def _register_spec(self, metadata):
        self.spec_metadata.append(metadata)
