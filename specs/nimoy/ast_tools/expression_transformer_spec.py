import ast
import _ast
from _ast import Dict, Constant, Name, Attribute

import astor

from nimoy.specification import Specification
from nimoy.ast_tools.expression_transformer import ComparisonExpressionTransformer, ThrownExpressionTransformer, \
    MockBehaviorExpressionTransformer, PowerAssertionTransformer


class PowerAssertionTransformerSpec(Specification):

    def regex_assertions_are_delegated_to_compare(self):
        with given:
            expression = """'asd' @ '.+'"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().visit_Expr(node.body[0])
            node.body[0] = transformed
        with expect:
            astor.to_source(node) != None  # sanity check to make sure that the produced node is valid AST
            transformed.value.func.attr == '_compare'

    def assertion_expressions_are_transformed(self):
        with given:
            expression = """True == 2"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().visit_Expr(node.body[0])
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

    def method_assertion_expressions_are_transformed(self):
        with given:
            expression = """get_a_value() == 2"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().visit_Expr(node.body[0])
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
            left_values[1].value == 'get_a_value()'
            type(left_values[2]) == _ast.Call
            left_values[3].value == 0
            left_values[4].value == 12
            left_values[5].value == False

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
            op_values[3].value == 14

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
            right_values[3].value == 17
            right_values[4].value == 17
            right_values[5].value == True

    def array_access_assertion_expressions_are_transformed(self):
        with given:
            expression = """some_array[1] == 2"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().visit_Expr(node.body[0])
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
            left_values[1].value == 'some_array[1]'
            type(left_values[2]) == _ast.Subscript
            left_values[3].value == 0
            left_values[4].value == 12
            left_values[5].value == False

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
            op_values[3].value == 14

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
            right_values[3].value == 17
            right_values[4].value == 17
            right_values[5].value == True

    def literal_list_assertion_expressions_are_transformed(self):
        with given:
            expression = """some_obj.some_att['key'] == ['var_a']"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().visit_Expr(node.body[0])
            node.body[0] = transformed
            transformed_values = transformed.value.args[0].values
        with expect:
            astor.to_source(node) != None  # sanity check to make sure that the produced node is valid AST
            transformed_values[1].value == 'some_obj'
            transformed_values[6].values[1].value == """some_att['key']"""
            transformed_values[6].values[6].values[2].value == "=="
            transformed_values[6].values[6].values[4].values[1].value == """[\'var_a\']"""

    def literal_dict_assertion_expressions_are_transformed(self):
        with given:
            expression = """some_obj.some_att['key'] == {'key': 'value'}"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().visit_Expr(node.body[0])
            node.body[0] = transformed
            transformed_values = transformed.value.args[0].values
        with expect:
            astor.to_source(node) != None  # sanity check to make sure that the produced node is valid AST
            transformed_values[1].value == 'some_obj'
            transformed_values[6].values[1].value == """some_att['key']"""
            transformed_values[6].values[6].values[2].value == "=="
            transformed_values[6].values[6].values[4].values[1].value == """{'key': 'value'}"""

    def non_zero_offset_assertion_expressions_are_transformed(self):
        with given:
            expression = """
if True:
    transformed_values[6].values[6].values[4].values[1].value == 'ley'
"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().visit_Expr(node.body[0].body[0])
            node.body[0] = transformed
            transformed_values = transformed.value.args[0].values
        with expect:
            astor.to_source(node) != None  # sanity check to make sure that the produced node is valid AST
            transformed_values[1].value == 'transformed_values[6]'
            transformed_values[3].value == 0

            transformed_values[6].values[1].value == 'values[6]'
            transformed_values[6].values[3].value == 22

            transformed_values[6].values[6].values[1].value == 'values[4]'
            transformed_values[6].values[6].values[3].value == 32

            transformed_values[6].values[6].values[6].values[1].value == 'values[1]'
            transformed_values[6].values[6].values[6].values[3].value == 42

            transformed_values[6].values[6].values[6].values[6].values[1].value == 'value'
            transformed_values[6].values[6].values[6].values[6].values[3].value == 52

            transformed_values[6].values[6].values[6].values[6].values[6].values[2].value == '=='
            transformed_values[6].values[6].values[6].values[6].values[6].values[3].value == 58

            transformed_values[6].values[6].values[6].values[6].values[6].values[4].values[1].value == 'ley'
            transformed_values[6].values[6].values[6].values[6].values[6].values[4].values[3].value == 61

    def convert_assertion_ast_to_nimoy_expression_ast(self):
        with given:
            expression = """True == 2"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().assert_ast_to_nimoy_expression_ast(0, node.body[0].value)
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
            transformed = PowerAssertionTransformer().expression_node_ast_to_nimoy_expression_ast(0, name_expression)
            transformed_keys = transformed.keys
            transformed_values = transformed.values
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
            transformed = PowerAssertionTransformer().expression_node_ast_to_nimoy_expression_ast(0,
                                                                                                  constant_expression)
            transformed_keys = transformed.keys
            transformed_values = transformed.values
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

    def function_call_node_ast_to_nimoy_expression_ast(self):
        with given:
            expression = """some_func_call()"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().expression_node_ast_to_nimoy_expression_ast(0, node.body[0].value)
            transformed_keys = transformed.keys
            transformed_values = transformed.values
        with expect:
            transformed_keys[0].value == 'type'
            transformed_keys[1].value == 'name'
            transformed_keys[2].value == 'value'
            transformed_keys[3].value == 'column'
            transformed_keys[4].value == 'end_column'
            transformed_keys[5].value == 'constant'

            transformed_values[0].value == 'exp'
            transformed_values[1].value == 'some_func_call()'
            type(transformed_values[2]) == _ast.Call
            transformed_values[3].value == 0
            transformed_values[4].value == 15
            transformed_values[5].value == False

    def attribute_from_function_call_node_ast_to_nimoy_expression_ast(self):
        with given:
            expression = """some_func_call().jimbob"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().expression_node_ast_to_nimoy_expression_ast(0, node.body[0].value)
            transformed_keys = transformed.keys
            transformed_values = transformed.values
        with expect:
            transformed_keys[0].value == 'type'
            transformed_keys[1].value == 'name'
            transformed_keys[2].value == 'value'
            transformed_keys[3].value == 'column'
            transformed_keys[4].value == 'end_column'
            transformed_keys[5].value == 'constant'
            transformed_keys[6].value == 'next'

            transformed_values[0].value == 'exp'
            transformed_values[1].value == 'some_func_call()'
            type(transformed_values[2]) == _ast.Call
            transformed_values[3].value == 0
            transformed_values[4].value == 15
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
            attribute_values[1].value == 'jimbob'
            type(attribute_values[2]) == _ast.Attribute
            attribute_values[3].value == 17
            attribute_values[4].value == 22
            attribute_values[5].value == False

    def subscript_from_function_call_node_ast_to_nimoy_expression_ast(self):
        with given:
            expression = """some_func_call().jimbob[1]"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().expression_node_ast_to_nimoy_expression_ast(0, node.body[0].value)
            transformed_keys = transformed.keys
            transformed_values = transformed.values
        with expect:
            transformed_keys[0].value == 'type'
            transformed_keys[1].value == 'name'
            transformed_keys[2].value == 'value'
            transformed_keys[3].value == 'column'
            transformed_keys[4].value == 'end_column'
            transformed_keys[5].value == 'constant'
            transformed_keys[6].value == 'next'

            transformed_values[0].value == 'exp'
            transformed_values[1].value == 'some_func_call()'
            type(transformed_values[2]) == _ast.Call
            transformed_values[3].value == 0
            transformed_values[4].value == 15
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
            attribute_values[1].value == 'jimbob[1]'
            type(attribute_values[2]) == _ast.Subscript
            attribute_values[3].value == 17
            attribute_values[4].value == 25
            attribute_values[5].value == False

    def chain_function_call_node_ast_to_nimoy_expression_ast(self):
        with given:
            expression = """some_func_call().jimbob()"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().expression_node_ast_to_nimoy_expression_ast(0, node.body[0].value)
            transformed_keys = transformed.keys
            transformed_values = transformed.values
        with expect:
            transformed_keys[0].value == 'type'
            transformed_keys[1].value == 'name'
            transformed_keys[2].value == 'value'
            transformed_keys[3].value == 'column'
            transformed_keys[4].value == 'end_column'
            transformed_keys[5].value == 'constant'
            transformed_keys[6].value == 'next'

            transformed_values[0].value == 'exp'
            transformed_values[1].value == 'some_func_call()'
            type(transformed_values[2]) == _ast.Call
            transformed_values[3].value == 0
            transformed_values[4].value == 15
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
            attribute_values[1].value == 'jimbob()'
            type(attribute_values[2]) == _ast.Call
            attribute_values[3].value == 17
            attribute_values[4].value == 24
            attribute_values[5].value == False

    def multi_level_attribute_node_ast_to_nimoy_expression_ast(self):
        with given:
            expression = """some_att.another_att.yet_another_att.and_another"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().expression_node_ast_to_nimoy_expression_ast(0, node.body[0].value)
            transformed_values = transformed.values
        with expect:
            transformed_values[2].id == 'some_att'
            transformed_values[6].values[2].attr == 'another_att'
            transformed_values[6].values[6].values[2].attr == 'yet_another_att'
            transformed_values[6].values[6].values[6].values[2].attr == 'and_another'

    def subscript_node_ast_to_nimoy_expression_ast(self):
        with given:
            expression = """some_list[1]"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().expression_node_ast_to_nimoy_expression_ast(0, node.body[0].value)
            transformed_keys = transformed.keys
            transformed_values = transformed.values
        with expect:
            transformed_keys[0].value == 'type'
            transformed_keys[1].value == 'name'
            transformed_keys[2].value == 'value'
            transformed_keys[3].value == 'column'
            transformed_keys[4].value == 'end_column'
            transformed_keys[5].value == 'constant'

            transformed_values[0].value == 'exp'
            transformed_values[1].value == 'some_list[1]'
            type(transformed_values[2]) == _ast.Subscript
            transformed_values[3].value == 0
            transformed_values[4].value == 11
            transformed_values[5].value == False

    def chained_subscript_attributes_node_ast_to_nimoy_expression_ast(self):
        with given:
            expression = """some_list[1].other_list[2]"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().expression_node_ast_to_nimoy_expression_ast(0, node.body[0].value)
            transformed_values = transformed.values
        with expect:
            transformed_values[1].value == 'some_list[1]'
            type(transformed_values[2]) == _ast.Subscript
            transformed_values[6].values[1].value == 'other_list[2]'
            type(transformed_values[6].values[2]) == _ast.Subscript

    def chained_subscript_node_ast_to_nimoy_expression_ast(self):
        with given:
            expression = """some_list[1][2][3]"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().expression_node_ast_to_nimoy_expression_ast(0, node.body[0].value)
            transformed_values = transformed.values
        with expect:
            transformed_values[0].value == 'exp'
            transformed_values[1].value == 'some_list[1][2][3]'
            type(transformed_values[2]) == _ast.Subscript
            transformed_values[3].value == 0
            transformed_values[4].value == 17
            transformed_values[5].value == False

    def chained_string_and_numeric_subscript_node_ast_to_nimoy_expression_ast(self):
        with given:
            expression = """some_obj.some_att['key'][0]"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().expression_node_ast_to_nimoy_expression_ast(0, node.body[0].value)
            transformed_values = transformed.values
        with expect:
            transformed_values[1].value == 'some_obj'
            type(transformed_values[2]) == _ast.Name
            att_values = transformed_values[6].values
            att_values[1].value == """some_att['key'][0]"""

    def chained_subscript_attribute_node_ast_to_nimoy_expression_ast(self):
        with given:
            expression = """some_obj.some_list[1][2][3]"""
            node = ast.parse(expression, mode='exec')
            transformed = PowerAssertionTransformer().expression_node_ast_to_nimoy_expression_ast(0, node.body[0].value)
            transformed_values = transformed.values
        with expect:
            transformed_values[0].value == 'exp'
            transformed_values[1].value == 'some_obj'
            type(transformed_values[2]) == _ast.Name
            transformed_values[3].value == 0
            transformed_values[4].value == 7

            subscript_values = transformed_values[6].values
            subscript_values[1].value == 'some_list[1][2][3]'
            type(subscript_values[2]) == _ast.Subscript
            subscript_values[3].value == 9
            subscript_values[4].value == 26

    def attribute_node_ast_to_nimoy_expression_ast(self):
        with given:
            name_expression = Name(id='bob', col_offset=0, end_col_offset=3)
            attribute_expression = Attribute(attr='mcbob', col_offset=4, end_col_offset=10, value=name_expression)
            transformed = PowerAssertionTransformer().expression_node_ast_to_nimoy_expression_ast(0,
                                                                                                  attribute_expression)
            transformed_keys = transformed.keys
            transformed_values = transformed.values
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
