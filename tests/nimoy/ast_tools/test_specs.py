import unittest
import ast
from unittest import mock
from nimoy.ast_tools.specs import SpecTransformer


class TestSpecTransformer(unittest.TestCase):
    @mock.patch('nimoy.ast_tools.specs.FeatureRegistrationTransformer')
    def test_find_specs_in_module(self, feature_registration_transformer):
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
        SpecTransformer(found_metadata).visit(node)

        self.assertEqual(len(found_metadata), 2)
        self.assertEqual(found_metadata[0].name, 'JimbobSpec')
        self.assertEqual(found_metadata[1].name, 'JonesSpec')

        feature_registration_transformer.expect_called_once()
        feature_registration_transformer.return_value.visit.expect_called_once()
