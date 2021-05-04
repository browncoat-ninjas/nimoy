import ast
import _ast

from nimoy.assertions.power import PowerAssertions, Expression, Op
from nimoy.specification import Specification


def _ast_to_nimoy_expression(ast_object) -> Expression:
    if type(ast_object) is _ast.Name:
        return Expression(ast_object.id, '', ast_object.col_offset, ast_object.end_col_offset - 1)
    elif type(ast_object) is _ast.Constant:
        return Expression(str(ast_object.value), ast_object.value, ast_object.col_offset, ast_object.end_col_offset - 1,
                          constant=True)
    elif type(ast_object) is _ast.Attribute:
        attribute_expression = Expression(ast_object.attr, '', ast_object.end_col_offset - len(ast_object.attr),
                                          ast_object.end_col_offset - 1)
        parent_expression = _ast_to_nimoy_expression(ast_object.value)
        parent_expression.next_node = attribute_expression
        return parent_expression


def _ast_op_to_nimoy_op(ast_object, assertion_result, latest_column) -> Op:
    op = None
    if type(ast_object) is _ast.Eq:
        op = '=='
    return Op(assertion_result, op, latest_column + 2)


def _assert_to_nimoy_expression(assert_expression: str, assertion_result: str) -> Expression:
    node = ast.parse(assert_expression, mode='exec')
    node_value = node.body[0].value
    left = node_value.left
    root_expression = _ast_to_nimoy_expression(left)
    current_expression = root_expression
    while current_expression.next_node:
        current_expression = current_expression.next_node

    current_expression.next_node = _ast_op_to_nimoy_op(node_value.ops[0], assertion_result,
                                                       current_expression.end_column)

    current_expression = current_expression.next_node

    right = node_value.comparators[0]
    current_expression.next_node = _ast_to_nimoy_expression(right)

    return root_expression


class PowerAssertionsSpec(Specification):

    def render_a_single_level_assertion_with_constant_on_the_right(self):
        with setup:
            expression = _assert_to_nimoy_expression('my_var == 3', 'false')
            expression.value = 2

            expected = """Assertion failed:
my_var == 3
|      |
2      false
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.assert_and_render(expression)
        with then:
            rendered == expected

    def render_a_single_level_assertion_with_constant_on_the_left(self):
        with setup:
            expression = _assert_to_nimoy_expression('3 == my_var', 'false')
            expression.next_node.next_node.value = 2

            expected = """Assertion failed:
3 == my_var
  |  |
  |  2
  false
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.assert_and_render(expression)
        with then:
            rendered == expected

    def render_a_single_level_assertion(self):
        with setup:
            expression = _assert_to_nimoy_expression('my_var == my_var_2', 'false')
            expression.value = 2
            expression.next_node.next_node.value = 3

            expected = """Assertion failed:
my_var == my_var_2
|      |  |
|      |  3
2      false
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.assert_and_render(expression)
        with then:
            rendered == expected

    def render_a_multi_level_assertion(self):
        with setup:
            expression = _assert_to_nimoy_expression('my_var.my_field == my_var_2.my_field_2', 'false')
            expression.value = {'moo': 'bob'}
            expression.next_node.value = 2

            expression.next_node.next_node.next_node.value = {'bob': 'mcbob'}
            expression.next_node.next_node.next_node.next_node.value = 3

            expected = """Assertion failed:
my_var.my_field == my_var_2.my_field_2
|      |        |  |        |
|      |        |  |        3
|      |        |  {'bob': 'mcbob'}
|      2        false
{'moo': 'bob'}
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.assert_and_render(expression)
        with then:
            rendered == expected

    def render_a_multi_level_assertion_with_constant_on_the_right(self):
        with setup:
            expression = _assert_to_nimoy_expression('my_var.my_field == 3', 'false')
            expression.value = {'moo': 'bob'}
            expression.next_node.value = 2

            expected = """Assertion failed:
my_var.my_field == 3
|      |        |
|      2        false
{'moo': 'bob'}
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.assert_and_render(expression)
        with then:
            rendered == expected

    def render_a_multi_level_assertion_with_constant_on_the_left(self):
        with setup:
            expression = _assert_to_nimoy_expression('3 == my_var.my_field', 'false')

            expression.value = 3

            expression.next_node.next_node.value = {'moo': 'bob'}
            expression.next_node.next_node.next_node.value = 2

            expected = """Assertion failed:
3 == my_var.my_field
  |  |      |
  |  |      2
  |  {'moo': 'bob'}
  false
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.assert_and_render(expression)
        with then:
            rendered == expected

    def render_a_left_lopsided_assertion(self):
        with setup:
            expression = _assert_to_nimoy_expression('my_var.my_field == my_var_2', 'false')

            expression.value = {'moo': 'bob'}
            expression.next_node.value = 2

            expression.next_node.next_node.next_node.value = {'bob': 'mcbob'}

            expected = """Assertion failed:
my_var.my_field == my_var_2
|      |        |  |
|      |        |  {'bob': 'mcbob'}
|      2        false
{'moo': 'bob'}
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.assert_and_render(expression)
        with then:
            rendered == expected

    def render_a_right_lopsided_assertion(self):
        with setup:
            expression = _assert_to_nimoy_expression('my_var == my_var_2.my_field_2', 'false')

            expression.value = {'moo': 'bob'}

            expression.next_node.next_node.value = {'bob': 'mcbob'}
            expression.next_node.next_node.next_node.value = 3

            expected = """Assertion failed:
my_var == my_var_2.my_field_2
|      |  |        |
|      |  |        3
|      |  {'bob': 'mcbob'}
|      false
{'moo': 'bob'}
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.assert_and_render(expression)
        with then:
            rendered == expected
