import unittest
import ast
from nimoy.ast_tools.method_registration_transformer import MethodRegistrationTransformer
from nimoy.ast_tools.ast_metadata import SpecMetadata


class MethodRegistrationTransformerTest(unittest.TestCase):

    def test_that_function_was_added(self):
        module_definition = 'class JSpec:\n    def test_jim(self):\n        pass\n    def _jim(self):\n        pass\n\n'
        node = ast.parse(module_definition, mode='exec')

        metadata = SpecMetadata('jim')
        MethodRegistrationTransformer(metadata).visit(node)
        self.assertEqual(len(metadata.methods), 1)
        self.assertEqual(metadata.methods[0], 'test_jim')

