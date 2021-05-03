import ast
import _ast

from nimoy.assertions.power import PowerAssertions, Expression, Assertion, Op
from nimoy.compare.types import Types
from nimoy.specification import Specification


def assert_to_assertion(assert_expression: str) -> Assertion:
    node = ast.parse(assert_expression, mode='exec')
    node_value = node.body[0].value
    left = node_value.left
    if type(left) is _ast.Name:
        left_expression = Expression(left.id, '', left.col_offset)
    elif type(left) is _ast.Constant:
        left_expression = Expression(str(left.value), left.value, left.col_offset, constant=True)

    right = node_value.comparators[0]
    if type(right) is _ast.Constant:
        right_expression = Expression(str(right.value), right.value, right.col_offset, constant=True)
    elif type(right) is _ast.Name:
        right_expression = Expression(right.id, '', right.col_offset)

    return Assertion(left_expression, right_expression, Op('==', Types.EQUAL))


class PowerAssertionsSpec(Specification):

    def render_a_single_level_assertion_with_constant_on_the_right(self):
        with setup:
            assertion = assert_to_assertion('my_var == 3')
            assertion.left.value = 2

            assertion.op.value = 'false'
            expected = """Assertion failed:
my_var == 3
|      |
2      false
"""
        with when:
            rendered = PowerAssertions().assert_and_render(assertion)
        with then:
            rendered == expected

    def render_a_single_level_assertion_with_constant_on_the_left(self):
        with setup:
            assertion = assert_to_assertion('3 == my_var')
            assertion.right.value = 2

            assertion.op.value = 'false'
            expected = """Assertion failed:
3 == my_var
  |  |
  |  2
  false
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.assert_and_render(assertion)
        with then:
            rendered == expected

    def render_a_single_level_assertion(self):
        with setup:
            left = Expression('my_var', 2)
            right = Expression('my_var_2', 3)
            assertion = Assertion(left, right, Op('==', Types.EQUAL))
            expected = """Assertion failed:
my_var == my_var_2
|      |  |
|      |  3
2      false
"""
            assertions = PowerAssertions()
        with when:
            rendered = assertions.assert_and_render(assertion)
        with then:
            rendered == expected

    def render_a_multi_level_assertion(self):
        with setup:
            left = Expression('my_var', {'moo': 'bob'}, next_node=Expression('my_field', 2))
            right = Expression('my_var_2', {'bob': 'mcbob'}, next_node=Expression('my_field_2', 3))
            assertion = Assertion(left, right, Op('==', Types.EQUAL))
            expected = """Assertion failed:
my_var.my_field == my_var_2.my_field_2
|      |        |  |        |
|      |        |  |        3
|      |        |  {bob:mcbob}
|      2        false
{moo: bob}  
"""
        with when:
            rendered = PowerAssertions().assert_and_render(assertion)
        with then:
            rendered == expected

    def render_a_multi_level_assertion_with_constant_on_the_right(self):
        with setup:
            left = Expression('my_var', {'moo': 'bob'}, next_node=Expression('my_field', 2))
            right = Expression('3', 3)
            assertion = Assertion(left, right, Op('==', Types.EQUAL))
            expected = """Assertion failed:
my_var.my_field == 3
|      |        |
|      2        false
{moo: bob}  
"""
        with when:
            rendered = PowerAssertions().assert_and_render(assertion)
        with then:
            rendered == expected

    def render_a_multi_level_assertion_with_constant_on_the_left(self):
        with setup:
            left = Expression('3', 3)
            right = Expression('my_var', {'moo': 'bob'}, next_node=Expression('my_field', 2))
            assertion = Assertion(left, right, Op('==', Types.EQUAL))
            expected = """Assertion failed:
3 == my_var.my_field
  |  |      |
  |  |      2
  |  {moo: bob}
  false
"""
        with when:
            rendered = PowerAssertions().assert_and_render(assertion)
        with then:
            rendered == expected

    def render_a_left_lopsided_assertion(self):
        with setup:
            left = Expression('my_var', {'moo': 'bob'}, next_node=Expression('my_field', 2))
            right = Expression('my_var_2', {'bob': 'mcbob'})
            assertion = Assertion(left, right, Op('==', Types.EQUAL))
            expected = """Assertion failed:
my_var.my_field == my_var_2
|      |        |  |
|      |        |  {bob:mcbob}
|      2        false      
{moo: bob}  
"""
        with when:
            rendered = PowerAssertions().assert_and_render(assertion)
        with then:
            rendered == expected

    def render_a_right_lopsided_assertion(self):
        with setup:
            left = Expression('my_var', {'moo': 'bob'})
            right = Expression('my_var_2', {'bob': 'mcbob'}, next_node=Expression('my_field_2', 3))
            assertion = Assertion(left, right, Op('==', Types.EQUAL))
            expected = """Assertion failed:
my_var == my_var_2.my_field_2
|      |  |        |
|      |  |        3
|      |  {bob:mcbob}         
|      false      
{moo: bob}  
"""
        with when:
            rendered = PowerAssertions().assert_and_render(assertion)
        with then:
            rendered == expected
