import ast
from unittest import mock
from nimoy.specification import Specification
from nimoy.ast_tools.specs import SpecTransformer


class SpecTransformerSpec(Specification):

    @mock.patch('nimoy.ast_tools.specs.FeatureRegistrationTransformer')
    def find_specs_in_module(self, feature_registration_transformer):
        with setup:
            spec_definition = """from nimoy.specification import Specification

class JimbobSpec(Specification):
    pass

class JonesSpec(Specification):
    pass

class Bobson:
    pass
            """

        node = ast.parse(spec_definition, mode='exec')
        found_metadata = []

        with when:
            SpecTransformer(found_metadata).visit(node)

        with then:
            len(found_metadata) == 2
            found_metadata[0].name == 'JimbobSpec'
            found_metadata[1].name == 'JonesSpec'

            feature_registration_transformer.expect_called_once()
            2 * feature_registration_transformer.return_value.visit()
