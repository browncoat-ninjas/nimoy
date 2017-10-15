import ast
import unittest
from nimoy.ast_tools.specs import SpecTransformer


class TestSpecTransformer(unittest.TestCase):
    def test_where_methods_are_extracted_from_features(self):
        spec_definition = """from nimoy.specification import Specification
        
class JimbobSpec(Specification):
    
    def my_feature(self):
        with setup:
            a = value_of_a
        
        with expect:
            a == 5
        
        with where:
            value_of_a = [5]
        
"""
        node = ast.parse(spec_definition, mode='exec')

        found_metadata = []
        SpecTransformer(found_metadata).visit(node)
        self.assertEqual(len(node.body[1].body), 2, 'The where method should have been extracted to class level')
        self.assertEqual(node.body[1].body[1].name, 'my_feature_where')
