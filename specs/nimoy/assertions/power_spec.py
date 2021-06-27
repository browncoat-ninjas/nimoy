import ast
import _ast
from typing import Dict

from nimoy.assertions.power import PowerAssertions
from nimoy.specification import Specification


def _ast_to_nimoy_expression(ast_object) -> Dict:
    if type(ast_object) is _ast.Name:
        return {'type': 'exp', 'name': ast_object.id, 'value': '', 'column': ast_object.col_offset,
                'end_column': ast_object.end_col_offset - 1}
    elif type(ast_object) is _ast.Constant:
        return {'type': 'exp', 'name': str(ast_object.value), 'value': ast_object.value,
                'column': ast_object.col_offset,
                'end_column': ast_object.end_col_offset - 1, 'constant': True}
    elif type(ast_object) is _ast.Attribute:
        attribute_expression = {'type': 'exp', 'name': ast_object.attr, 'value': '', 'column': ast_object.value.end_col_offset + 1,
                                'end_column': ast_object.end_col_offset - 1}
        parent_expression = _ast_to_nimoy_expression(ast_object.value)
        parent_expression['next'] = attribute_expression
        return parent_expression


def _ast_op_to_nimoy_op(ast_object, assertion_result: bool, latest_column) -> Dict:
    start_column = latest_column + 1
    end_column = start_column + 2
    op = None
    if type(ast_object) is _ast.Eq:
        op = '=='
    return {'type': 'op', 'op': op, 'value': assertion_result, 'column': start_column, 'end_column': end_column}


def _assert_to_nimoy_expression(assert_expression: str, assertion_result: bool) -> Dict:
    node = ast.parse(assert_expression, mode='exec')
    node_value = node.body[0].value
    left = node_value.left
    root_expression = _ast_to_nimoy_expression(left)
    current_expression = root_expression
    while 'next' in current_expression:
        current_expression = current_expression['next']

    current_expression['next'] = _ast_op_to_nimoy_op(node_value.ops[0], assertion_result,
                                                       left.end_col_offset)

    current_expression = current_expression['next']

    right = node_value.comparators[0]
    current_expression['next'] = _ast_to_nimoy_expression(right)

    return root_expression


class PowerAssertionsSpec(Specification):

    def assert_a_correct_expression(self):
        with setup:
            expression = _assert_to_nimoy_expression('True == True', True)
            assertions = PowerAssertions()
        with expect:
            assertions.assert_and_raise(expression)

    def assert_a_wrong_expression(self):
        with setup:
            expression = _assert_to_nimoy_expression('my_var == 3', False)
            expression['value'] = 2

            expected = """Assertion failed:
my_var == 3
|      |
2      False
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.render(expression)
        with then:
            rendered == expected

    def render_a_single_level_assertion_with_constant_on_the_right(self):
        with setup:
            expression = _assert_to_nimoy_expression('my_var == 3', False)
            expression['value'] = 2

            expected = """Assertion failed:
my_var == 3
|      |
2      False
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.render(expression)
        with then:
            rendered == expected

    def render_a_single_level_assertion_with_constant_on_the_right(self):
        with setup:
            expression = _assert_to_nimoy_expression('my_var == 3', False)
            expression['value'] = 2

            expected = """Assertion failed:
my_var == 3
|      |
2      False
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.render(expression)
        with then:
            rendered == expected

    def render_a_single_level_assertion_with_constant_on_the_left(self):
        with setup:
            expression = _assert_to_nimoy_expression('3 == my_var', False)
            expression['next']['next']['value'] = 2

            expected = """Assertion failed:
3 == my_var
  |  |
  |  2
  False
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.render(expression)
        with then:
            rendered == expected

    def render_a_single_level_assertion(self):
        with setup:
            expression = _assert_to_nimoy_expression('my_var == my_var_2', False)
            expression['value'] = 2
            expression['next']['next']['value'] = 3

            expected = """Assertion failed:
my_var == my_var_2
|      |  |
|      |  3
2      False
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.render(expression)
        with then:
            rendered == expected

    def render_a_multi_level_assertion(self):
        with setup:
            expression = _assert_to_nimoy_expression('my_var.my_field == my_var_2.my_field_2', False)
            expression['value'] = {'moo': 'bob'}
            expression['next']['value'] = 2

            expression['next']['next']['next']['value'] = {'bob': 'mcbob'}
            expression['next']['next']['next']['next']['value'] = 3

            expected = """Assertion failed:
my_var.my_field == my_var_2.my_field_2
|      |        |  |        |
|      |        |  |        3
|      |        |  {'bob': 'mcbob'}
|      2        False
{'moo': 'bob'}
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.render(expression)
        with then:
            rendered == expected

    def render_a_multi_level_assertion_with_constant_on_the_right(self):
        with setup:
            expression = _assert_to_nimoy_expression('my_var.my_field == 3', False)
            expression['value'] = {'moo': 'bob'}
            expression['next']['value'] = 2

            expected = """Assertion failed:
my_var.my_field == 3
|      |        |
|      2        False
{'moo': 'bob'}
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.render(expression)
        with then:
            rendered == expected

    def render_a_multi_level_assertion_with_constant_on_the_left(self):
        with setup:
            expression = _assert_to_nimoy_expression('3 == my_var.my_field', False)

            expression['value'] = 3

            expression['next']['next']['value'] = {'moo': 'bob'}
            expression['next']['next']['next']['value'] = 2

            expected = """Assertion failed:
3 == my_var.my_field
  |  |      |
  |  |      2
  |  {'moo': 'bob'}
  False
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.render(expression)
        with then:
            rendered == expected

    def render_a_left_lopsided_assertion(self):
        with setup:
            expression = _assert_to_nimoy_expression('my_var.my_field == my_var_2', False)

            expression['value'] = {'moo': 'bob'}
            expression['next']['value'] = 2

            expression['next']['next']['next']['value'] = {'bob': 'mcbob'}

            expected = """Assertion failed:
my_var.my_field == my_var_2
|      |        |  |
|      |        |  {'bob': 'mcbob'}
|      2        False
{'moo': 'bob'}
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.render(expression)
        with then:
            rendered == expected

    def render_a_right_lopsided_assertion(self):
        with setup:
            expression = _assert_to_nimoy_expression('my_var == my_var_2.my_field_2', False)

            expression['value'] = {'moo': 'bob'}

            expression['next']['next']['value'] = {'bob': 'mcbob'}
            expression['next']['next']['next']['value'] = 3

            expected = """Assertion failed:
my_var == my_var_2.my_field_2
|      |  |        |
|      |  |        3
|      |  {'bob': 'mcbob'}
|      False
{'moo': 'bob'}
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.render(expression)
        with then:
            rendered == expected
