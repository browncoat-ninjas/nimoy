import unittest
import ast
import _ast
from nimoy.ast_tools.module_transformer import ModuleTransformer


class TestModuleTransformer(unittest.TestCase):
    def test_unittest_module_is_imported_if_missing(self):
        module_definition = 'class JimbobSpec:\n    pass\n\n'
        node = ast.parse(module_definition, mode='exec')

        ModuleTransformer().visit(node)
        self.assertEqual(len(node.body), 3)
        self.assertTrue(isinstance(node.body[0], _ast.ClassDef))

        self.assertTrue(isinstance(node.body[1], _ast.Import))
        self.assertEqual(node.body[1].names[0].name, 'unittest')

        self.assertTrue(isinstance(node.body[2], _ast.Import))
        self.assertEqual(node.body[2].names[0].name, 'nimoy')

    def test_unittest_module_is_not_re_imported_if_already_exists(self):
        module_definition = 'import unittest\nimport nimoy\n\nclass JimbobSpec:\n    pass\n\n'
        node = ast.parse(module_definition, mode='exec')

        ModuleTransformer().visit(node)
        self.assertEqual(len(node.body), 3)
        self.assertTrue(isinstance(node.body[0], _ast.Import))
        self.assertEqual(node.body[0].names[0].name, 'unittest')

        self.assertTrue(isinstance(node.body[1], _ast.Import))
        self.assertEqual(node.body[1].names[0].name, 'nimoy')

        self.assertTrue(isinstance(node.body[2], _ast.ClassDef))
