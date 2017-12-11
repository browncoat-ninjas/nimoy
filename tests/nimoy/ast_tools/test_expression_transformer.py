import unittest
import ast
import _ast
from nimoy.ast_tools.expression_transformer import ComparisonExpressionTransformer, ThrownExpressionTransformer


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

        self.assertEqual(body_elements[0].value.func.attr, '_compare')
        self.assertEqual(body_elements[1].value.func.attr, '_compare')
        self.assertEqual(body_elements[2].value.func.attr, '_compare')
        self.assertEqual(body_elements[3].value.func.attr, '_compare')
        self.assertEqual(body_elements[4].value.func.attr, '_compare')
        self.assertEqual(body_elements[5].value.func.attr, '_compare')
        self.assertEqual(body_elements[6].value.func.attr, '_compare')
        self.assertEqual(body_elements[7].value.func.attr, '_compare')
        self.assertEqual(body_elements[8].value.func.attr, '_compare')
        self.assertEqual(body_elements[9].value.func.attr, '_compare')

    def test_if_nested_equality_transforms(self):
        module_definition = """
if True:
    1 == 2
        """

        node = ast.parse(module_definition, mode='exec')
        ComparisonExpressionTransformer().visit(node)

        body_expression = node.body[0]
        self.assertTrue(isinstance(body_expression, _ast.If))
        self.assertTrue(isinstance(body_expression.body[0].value, _ast.Call))
        self.assertEqual(body_expression.body[0].value.func.attr, '_compare')

    def test_for_nested_equality_transforms(self):
        module_definition = """
for x in [1, 2]:
    1 == 2
        """

        node = ast.parse(module_definition, mode='exec')
        ComparisonExpressionTransformer().visit(node)

        body_expression = node.body[0]
        self.assertTrue(isinstance(body_expression, _ast.For))
        self.assertTrue(isinstance(body_expression.body[0].value, _ast.Call))
        self.assertEqual(body_expression.body[0].value.func.attr, '_compare')


class TestThrownExpressionTransformer(unittest.TestCase):

    def test_single_thrown_call_is_transformed(self):
        module_definition = "thrown(ArithmeticError)"

        node = ast.parse(module_definition, mode='exec')
        ThrownExpressionTransformer().visit(node)

        thrown_expression = node.body[0].value
        self.assertTrue(isinstance(thrown_expression, _ast.Call))
        self.assertEqual(thrown_expression.func.attr, '_exception_thrown')
        self.assertEqual(thrown_expression.args[0].id, 'ArithmeticError')

    def test_assigned_thrown_call_is_transformed(self):
        module_definition = "ex = thrown(ArithmeticError)"

        node = ast.parse(module_definition, mode='exec')
        ThrownExpressionTransformer().visit(node)

        thrown_expression = node.body[0].value
        self.assertTrue(isinstance(thrown_expression, _ast.Call))
        self.assertEqual(thrown_expression.func.attr, '_exception_thrown')
        self.assertEqual(thrown_expression.args[0].id, 'ArithmeticError')
