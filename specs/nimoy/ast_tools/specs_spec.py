import ast
from unittest import mock

from nimoy.ast_tools.specs import SpecTransformer
from nimoy.runner.metadata import RunnerContext
from nimoy.runner.spec_finder import Location
from nimoy.specification import Specification


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
            SpecTransformer(RunnerContext(), Location('some_spec.py'), found_metadata).visit(node)

        with then:
            len(found_metadata) == 2
            found_metadata[0].name == 'JimbobSpec'
            found_metadata[1].name == 'JonesSpec'

            feature_registration_transformer.expect_called_once()
            2 * feature_registration_transformer.return_value.visit()

    @mock.patch('nimoy.ast_tools.specs.FeatureRegistrationTransformer')
    def find_explicit_spec_in_module(self, feature_registration_transformer):
        with setup:
            spec_definition = """from nimoy.specification import Specification

class JimbobSpec(Specification):
    pass

class JonesSpec(Specification):
    pass
            """

        node = ast.parse(spec_definition, mode='exec')
        found_metadata = []

        with when:
            SpecTransformer(RunnerContext(), Location('some_spec.py::JonesSpec'), found_metadata).visit(node)

        with then:
            len(found_metadata) == 1
            found_metadata[0].name == 'JonesSpec'

            feature_registration_transformer.expect_called_once()
            1 * feature_registration_transformer.return_value.visit()
