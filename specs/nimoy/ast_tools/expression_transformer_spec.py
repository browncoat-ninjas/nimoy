import ast
import _ast
from nimoy.specification import Specification
from nimoy.ast_tools.expression_transformer import ComparisonExpressionTransformer, ThrownExpressionTransformer


class ComparisonExpressionTransformerSpec(Specification):

    def equality_expressions_are_transformed(self):
        with setup:
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
'The quick brown fox' @ '.+brown.+'
            """
            node = ast.parse(module_definition, mode='exec')

        with when:
            ComparisonExpressionTransformer().visit(node)

        with then:
            body_elements = node.body
            all([isinstance(body_element.value, _ast.Call) for body_element in body_elements]) == True
            all([body_element.value.func.attr == '_compare' for body_element in body_elements]) == True

    def nested_if_equality_is_transformed(self):
        with setup:
            module_definition = """
if True:
    1 == 2
        """
            node = ast.parse(module_definition, mode='exec')

        with when:
            ComparisonExpressionTransformer().visit(node)

        with then:
            body_expression = node.body[0]
            isinstance(body_expression, _ast.If) == True
            isinstance(body_expression.body[0].value, _ast.Call) == True
            body_expression.body[0].value.func.attr == '_compare'

    def nested_for_equality_is_transformed(self):
        with setup:
            module_definition = """
for x in [1, 2]:
    1 == 2
            """
            node = ast.parse(module_definition, mode='exec')

        with when:
            ComparisonExpressionTransformer().visit(node)

        with then:
            body_expression = node.body[0]
            isinstance(body_expression, _ast.For) == True
            isinstance(body_expression.body[0].value, _ast.Call) == True
            body_expression.body[0].value.func.attr == '_compare'


class ThrownExpressionTransformerSpec(Specification):

    def single_thrown_call_is_transformed(self):
        with setup:
            module_definition = "thrown(ArithmeticError)"
            node = ast.parse(module_definition, mode='exec')

        with when:
            ThrownExpressionTransformer().visit(node)

        with then:
            thrown_expression = node.body[0].value
            isinstance(thrown_expression, _ast.Call) == True
            thrown_expression.func.attr == '_exception_thrown'
            thrown_expression.args[0].id == 'ArithmeticError'

    def assigned_thrown_call_is_transformed(self):
        with setup:
            module_definition = "ex = thrown(ArithmeticError)"
            node = ast.parse(module_definition, mode='exec')

        with when:
            ThrownExpressionTransformer().visit(node)

        with then:
            thrown_expression = node.body[0].value
            isinstance(thrown_expression, _ast.Call) == True
            thrown_expression.func.attr == '_exception_thrown'
            thrown_expression.args[0].id == 'ArithmeticError'
