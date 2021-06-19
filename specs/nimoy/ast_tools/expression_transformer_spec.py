import ast
import _ast
from _ast import Dict, Constant, Name, Attribute

import astor

from nimoy.specification import Specification
from nimoy.ast_tools.expression_transformer import ComparisonExpressionTransformer, ThrownExpressionTransformer, \
    MockBehaviorExpressionTransformer, PowerAssertionTransformer


class PowerAssertionTransformerSpec(Specification):

    def non_assertion_expressions_are_returned(self):
        with given:
            expression = """jim = 'bob'"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().visit_Call(node.body[0])
        with expect:
            node.body[0] == transformed

    def assertion_expressions_are_transformed(self):
        with given:
            expression = """True == 2"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().visit_Call(node.body[0])
            node.body[0] = transformed
        with expect:
            astor.to_source(node) != None  # sanity check to make sure that the produced node is valid AST
            transformed.value.func.attr == '_power_assert'
            transformed.value.func.value.id == 'self'
            left_keys = transformed.value.args[0].keys
            left_keys[0].value == 'type'
            left_keys[1].value == 'name'
            left_keys[2].value == 'value'
            left_keys[3].value == 'column'
            left_keys[4].value == 'end_column'
            left_keys[5].value == 'constant'
            left_keys[6].value == 'next'

            left_values = transformed.value.args[0].values
            left_values[0].value == 'exp'
            left_values[1].value == 'True'
            left_values[2].value == True
            left_values[3].value == 0
            left_values[4].value == 3
            left_values[5].value == True

            op = left_values[6]
            op_keys = op.keys
            op_keys[0].value == 'type'
            op_keys[1].value == 'value'
            op_keys[2].value == 'op'
            op_keys[3].value == 'column'
            op_keys[4].value == 'next'

            op_values = op.values
            op_values[0].value == 'op'
            type(op_values[1]) == _ast.Compare
            op_values[2].value == '=='
            op_values[3].value == 5

            right_keys = op_values[4].keys
            right_keys[0].value == 'type'
            right_keys[1].value == 'name'
            right_keys[2].value == 'value'
            right_keys[3].value == 'column'
            right_keys[4].value == 'end_column'
            right_keys[5].value == 'constant'

            right_values = op_values[4].values
            right_values[0].value == 'exp'
            right_values[1].value == '2'
            right_values[2].value == 2
            right_values[3].value == 8
            right_values[4].value == 8
            right_values[5].value == True

    def convert_assertion_ast_to_nimoy_expression_ast(self):
        with given:
            expression = """True == 2"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().assert_ast_to_nimoy_expression_ast(node.body[0].value)
        with expect:
            left_keys = transformed.keys
            left_keys[0].value == 'type'
            left_keys[1].value == 'name'
            left_keys[2].value == 'value'
            left_keys[3].value == 'column'
            left_keys[4].value == 'end_column'
            left_keys[5].value == 'constant'
            left_keys[6].value == 'next'

            left_values = transformed.values
            left_values[0].value == 'exp'
            left_values[1].value == 'True'
            left_values[2].value == True
            left_values[3].value == 0
            left_values[4].value == 3
            left_values[5].value == True

            op = left_values[6]
            op_keys = op.keys
            op_keys[0].value == 'type'
            op_keys[1].value == 'value'
            op_keys[2].value == 'op'
            op_keys[3].value == 'column'
            op_keys[4].value == 'next'

            op_values = op.values
            op_values[0].value == 'op'
            type(op_values[1]) == _ast.Compare
            op_values[2].value == '=='
            op_values[3].value == 5

            right_keys = op_values[4].keys
            right_keys[0].value == 'type'
            right_keys[1].value == 'name'
            right_keys[2].value == 'value'
            right_keys[3].value == 'column'
            right_keys[4].value == 'end_column'
            right_keys[5].value == 'constant'

            right_values = op_values[4].values
            right_values[0].value == 'exp'
            right_values[1].value == '2'
            right_values[2].value == 2
            right_values[3].value == 8
            right_values[4].value == 8
            right_values[5].value == True

    def convert_eq_op_ast_to_nimoy_op_ast(self):
        with given:
            expression = """True == 2"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().op_ast_to_nimoy_op_ast(node.body[0].value.ops[0], 5,
                                                                             node.body[0].value)
        with expect:
            op_keys = transformed.keys
            op_keys[0].value == 'type'
            op_keys[1].value == 'value'
            op_keys[2].value == 'op'
            op_keys[3].value == 'column'

            op_values = transformed.values
            op_values[0].value == 'op'
            type(op_values[1]) == _ast.Compare
            op_values[2].value == '=='
            op_values[3].value == 5

    def get_last_dictionary(self):
        with given:
            leaf = Dict(keys=[Constant(value='leaf')], values=[Constant(value='value')])
            branch = Dict(keys=[Constant(value='next')], values=[leaf])
            root = Dict(keys=[Constant(value='next')], values=[branch])
            rightmost = PowerAssertionTransformer().get_last_dictionary(root)
        with expect:
            rightmost.keys[0].value == 'leaf'

    def name_node_ast_to_nimoy_expression_ast(self):
        with given:
            name_expression = Name(id='bob', col_offset=0, end_col_offset=10)
            transformed_keys, transformed_values = PowerAssertionTransformer().expression_node_ast_to_nimoy_expression_ast(
                name_expression)
        with expect:
            transformed_keys[0].value == 'type'
            transformed_keys[1].value == 'name'
            transformed_keys[2].value == 'value'
            transformed_keys[3].value == 'column'
            transformed_keys[4].value == 'end_column'
            transformed_keys[5].value == 'constant'

            transformed_values[0].value == 'exp'
            transformed_values[1].value == 'bob'
            transformed_values[2] == name_expression
            transformed_values[3].value == 0
            transformed_values[4].value == 9
            transformed_values[5].value == False

    def constant_node_ast_to_nimoy_expression_ast(self):
        with given:
            constant_expression = Constant(value='bob', col_offset=0, end_col_offset=10)
            transformed_keys, transformed_values = PowerAssertionTransformer().expression_node_ast_to_nimoy_expression_ast(
                constant_expression)
        with expect:
            transformed_keys[0].value == 'type'
            transformed_keys[1].value == 'name'
            transformed_keys[2].value == 'value'
            transformed_keys[3].value == 'column'
            transformed_keys[4].value == 'end_column'
            transformed_keys[5].value == 'constant'

            transformed_values[0].value == 'exp'
            transformed_values[1].value == 'bob'
            transformed_values[2] == constant_expression
            transformed_values[3].value == 0
            transformed_values[4].value == 9
            transformed_values[5].value == True

    def attribute_node_ast_to_nimoy_expression_ast(self):
        with given:
            name_expression = Name(id='bob', col_offset=0, end_col_offset=3)
            attribute_expression = Attribute(attr='mcbob', col_offset=4, end_col_offset=10, value=name_expression)
            transformed_keys, transformed_values = PowerAssertionTransformer().expression_node_ast_to_nimoy_expression_ast(
                attribute_expression)
        with expect:
            transformed_keys[0].value == 'type'
            transformed_keys[1].value == 'name'
            transformed_keys[2].value == 'value'
            transformed_keys[3].value == 'column'
            transformed_keys[4].value == 'end_column'
            transformed_keys[5].value == 'constant'
            transformed_keys[6].value == 'next'

            transformed_values[0].value == 'exp'
            transformed_values[1].value == 'bob'
            transformed_values[2] == name_expression
            transformed_values[3].value == 0
            transformed_values[4].value == 2
            transformed_values[5].value == False

            attribute_keys = transformed_values[6].keys
            attribute_keys[0].value == 'type'
            attribute_keys[1].value == 'name'
            attribute_keys[2].value == 'value'
            attribute_keys[3].value == 'column'
            attribute_keys[4].value == 'end_column'
            attribute_keys[5].value == 'constant'

            attribute_values = transformed_values[6].values
            attribute_values[0].value == 'exp'
            attribute_values[1].value == 'mcbob'
            attribute_values[2] == attribute_expression
            attribute_values[3].value == 4
            attribute_values[4].value == 9
            attribute_values[5].value == False


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


class MockBehaviorExpressionTransformerSpec(Specification):

    def right_shift_is_transformed_to_return_value(self):
        with setup:
            module_definition = "the_mock.some_method() >> 5"
            node = ast.parse(module_definition, mode='exec')

        with when:
            MockBehaviorExpressionTransformer().visit(node)

        with then:
            body_element = node.body[0]
            isinstance(body_element, _ast.Assign)
            body_element.value.n == 5
            body_element.targets[0].attr == 'return_value'
            isinstance(body_element.targets[0].ctx, _ast.Store)
            body_element.targets[0].value.value.id == 'the_mock'

    def left_shift_is_transformed_to_side_effect(self):
        with setup:
            module_definition = "the_mock.some_method() << [5, 6, 7]"
            node = ast.parse(module_definition, mode='exec')

        with when:
            MockBehaviorExpressionTransformer().visit(node)

        with then:
            body_element = node.body[0]
            isinstance(body_element, _ast.Assign)
            isinstance(body_element.value, _ast.List)
            body_element.value.elts[0].n == 5
            body_element.value.elts[1].n == 6
            body_element.value.elts[2].n == 7
            body_element.targets[0].attr == 'side_effect'
            isinstance(body_element.targets[0].ctx, _ast.Store)
            body_element.targets[0].value.value.id == 'the_mock'
