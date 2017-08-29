import unittest
import ast
from nimoy.ast_tools.spec_transformer import SpecTransformer


class TestSpecTransformer(unittest.TestCase):
    def test_find_specs_in_module(self):
        spec_definition = 'class JimbobSpec:\n    pass\n\nclass JonesSpec:\n    pass\n\nclass Bobson:\n    pass\n'
        node = ast.parse(spec_definition, mode='exec')

        found_metadata = []
        SpecTransformer(found_metadata).visit(node)

        self.assertEqual(len(found_metadata), 2)
        self.assertEqual(found_metadata[0].name, 'JimbobSpec')
        self.assertEqual(found_metadata[1].name, 'JonesSpec')

        self.assertEqual(node.body[0].bases[0].attr, 'TestCase')
        self.assertEqual(node.body[0].bases[0].value.id, 'unittest')
        self.assertEqual(node.body[1].bases[0].attr, 'TestCase')
        self.assertEqual(node.body[1].bases[0].value.id, 'unittest')
        self.assertEqual(len(node.body[2].bases), 0)
