import unittest
import ast
import _ast
from nimoy.ast_tools.expression_transformer import ComparisonExpressionTransformer


class TestComparisonExpressionTransformer(unittest.TestCase):
    def test_equality_transforms(self):

        module_definition = """1 == 2
1 != 2
1 < 2
1 <= 2
1 > 2
1 >= 2
1 is 2
1 is not 2
1 in 2
1 not in 2
        """

        node = ast.parse(module_definition, mode='exec')
        ComparisonExpressionTransformer().visit(node)

        body_elements = node.body
        self.assertTrue(all([isinstance(body_element.value, _ast.Call) for body_element in body_elements]))
        self.assertTrue(all([body_element.value.args[0].n == 1 for body_element in body_elements]))
        self.assertTrue(all([body_element.value.args[1].n == 2 for body_element in body_elements]))

        self.assertEqual(body_elements[0].value.func.attr, 'assertEqual')
        self.assertEqual(body_elements[1].value.func.attr, 'assertNotEqual')
        self.assertEqual(body_elements[2].value.func.attr, 'assertLess')
        self.assertEqual(body_elements[3].value.func.attr, 'assertLessEqual')
        self.assertEqual(body_elements[4].value.func.attr, 'assertGreater')
        self.assertEqual(body_elements[5].value.func.attr, 'assertGreaterEqual')
        self.assertEqual(body_elements[6].value.func.attr, 'assertIs')
        self.assertEqual(body_elements[7].value.func.attr, 'assertIsNot')
        self.assertEqual(body_elements[8].value.func.attr, 'assertIn')
        self.assertEqual(body_elements[9].value.func.attr, 'assertNotIn')
