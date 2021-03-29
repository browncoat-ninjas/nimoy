from nimoy.assertions.power import PowerAssertions, Variable, ConstantValue
from nimoy.compare.types import Types
from nimoy.specification import Specification


class PowerAssertionsSpec(Specification):

    def render_a_single_level_assertion_with_constant_on_the_right(self):
        with setup:
            left = [Variable('my_var', 2)]
            right = [ConstantValue(3)]
            expected = """Assertion failed:
            my_var == 3
            |      |
            2      false
            """
        with when:
            rendered = PowerAssertions().assert_and_render(left, right, Types.EQUAL)
        with then:
            rendered == expected

    def render_a_single_level_assertion_with_constant_on_the_left(self):
        with setup:
            left = [Variable('my_var', 2)]
            right = [ConstantValue(3)]
            expected = """Assertion failed:
            3 == my_var
              |  |
              |  2
              false
            """
        with when:
            rendered = PowerAssertions().assert_and_render(left, right, Types.EQUAL)
        with then:
            rendered == expected

    def render_a_single_level_assertion(self):
        with setup:
            left = [Variable('my_var', 2)]
            right = [Variable('my_var_2', 3)]
            expected = """Assertion failed:
            my_var == my_var_2
            |      |  |
            |      |  3
            2      false
            """
        with when:
            rendered = PowerAssertions().assert_and_render(left, right, Types.EQUAL)
        with then:
            rendered == expected

    def render_a_multi_level_assertion(self):
        with setup:
            left = [Variable('my_var', {'moo': 'bob'}), Variable('my_field', 2)]
            right = [Variable('my_var_2', {'bob': 'mcbob'}), Variable('my_field_2', 3)]
            expected = """Assertion failed:
            my_var.my_field == my_var_2.my_field_2
            |      |        |  |        |
            |      |        |  |        3
            |      |        |  {bob:mcbob}
            |      2        false
            {moo: bob}  
            """
        with when:
            rendered = PowerAssertions().assert_and_render(left, right, Types.EQUAL)
        with then:
            rendered == expected

    def render_a_multi_level_assertion_with_constant_on_the_right(self):
        with setup:
            left = [Variable('my_var', {'moo': 'bob'}), Variable('my_field', 2)]
            right = [ConstantValue(3)]
            expected = """Assertion failed:
            my_var.my_field == 3
            |      |        |
            |      2        false
            {moo: bob}  
            """
        with when:
            rendered = PowerAssertions().assert_and_render(left, right, Types.EQUAL)
        with then:
            rendered == expected

    def render_a_multi_level_assertion_with_constant_on_the_left(self):
        with setup:
            left = [ConstantValue(3)]
            right = [Variable('my_var', {'moo': 'bob'}), Variable('my_field', 2)]
            expected = """Assertion failed:
            3 == my_var.my_field
              |  |      |
              |  |      2
              |  {moo: bob}
              false
            """
        with when:
            rendered = PowerAssertions().assert_and_render(left, right, Types.EQUAL)
        with then:
            rendered == expected

    def render_a_left_lopsided_assertion(self):
        with setup:
            left = [Variable('my_var', {'moo': 'bob'}), Variable('my_field', 2)]
            right = [Variable('my_var_2', {'bob': 'mcbob'})]
            expected = """Assertion failed:
            my_var.my_field == my_var_2
            |      |        |  |
            |      |        |  {bob:mcbob}
            |      2        false      
            {moo: bob}  
            """
        with when:
            rendered = PowerAssertions().assert_and_render(left, right, Types.EQUAL)
        with then:
            rendered == expected

    def render_a_right_lopsided_assertion(self):
        with setup:
            left = [Variable('my_var', {'moo': 'bob'})]
            right = [Variable('my_var_2', {'bob': 'mcbob'}), Variable('my_field_2', 3)]
            expected = """Assertion failed:
            my_var == my_var_2.my_field_2
            |      |  |        |
            |      |  |        3
            |      |  {bob:mcbob}         
            |      false      
            {moo: bob}  
            """
        with when:
            rendered = PowerAssertions().assert_and_render(left, right, Types.EQUAL)
        with then:
            rendered == expected
