import _ast
import ast
from _ast import Dict, Constant
from typing import Tuple

from nimoy.ast_tools import ast_proxy
from nimoy.compare.types import Types


class ComparisonExpressionTransformer(ast.NodeTransformer):
    def __init__(self) -> None:
        super().__init__()
        self.comparator_methods = {
            _ast.Eq: Types.EQUAL,
            _ast.NotEq: Types.NOT_EQUAL,
            _ast.Lt: Types.LESS_THAN,
            _ast.LtE: Types.LESS_THAN_EQUAL,
            _ast.Gt: Types.GREATER_THAN,
            _ast.GtE: Types.GREATER_THAN_EQUAL,
            _ast.Is: Types.IS,
            _ast.IsNot: Types.IS_NOT,
            _ast.In: Types.IN,
            _ast.NotIn: Types.NOT_IN,
            _ast.MatMult: Types.MATCHES_REGEXP,
        }

    def visit_Expr(self, expression_node):
        value = expression_node.value
        if not isinstance(value, _ast.Compare):
            if isinstance(value, _ast.BinOp):
                if hasattr(value, 'op') and not isinstance(value.op, _ast.MatMult):
                    return expression_node
            else:
                return expression_node

        left_value = value.left

        # TODO: Support multiple comparators (1 < 2 < 3). This may be tricky because one expression of multiple
        if hasattr(value, 'op'):
            comparison_operation = value.op
            right_value = value.right
        else:
            comparison_operation = value.ops[0]
            right_value = value.comparators[0]
        comparison_operation_type = type(comparison_operation)
        internal_comparison_type = self.comparator_methods[comparison_operation_type]

        expression_node.value = _ast.Call(
            func=_ast.Attribute(
                value=_ast.Name(id='self', ctx=_ast.Load()),
                attr='_compare',
                ctx=_ast.Load()
            ),
            args=[left_value, right_value, ast_proxy.ast_str(s=internal_comparison_type.name)],
            keywords=[]
        )
        return expression_node


# Converts assertion expressions to Nimoy power assertions.
# This is done by taking the comparison expression and breaking it into a tree structure, made out of dictionaries,
# where every element in the structure is one evaluable subexpression. The tree is then set as the argument to a
# nimoy.specification.Specification._power_assert method call.
# For example, an expression like:
# jim == bob.mcbob
# Will be transformed to an expression like:
# self._power_assert( { 'name': 'jim', value: original-ast-node, 'next': {
#     'name': '==', 'next': {
#         'name': 'bob', value: original-ast-node, 'next': {
#             'name': 'mcbob', value: original-ast-node
#         }
#     }
# })
#
# The reason this transformed to vanilla dictionaries is that we need a way to pass this information to the
# _power_assert without adding any classes that the user didn't import themselves
class PowerAssertionTransformer(ast.NodeTransformer):

    # Recursively transform the expression node AST to a linked dictionary structure AST. Supported nodes are Name,
    # Constant and Attribute. Recursion occurs on every attribute node.
    # The method always returns the root link
    @staticmethod
    def expression_node_ast_to_nimoy_expression_ast(ast_object) -> Tuple:
        keys = []
        values = []
        if type(ast_object) is _ast.Name:
            keys.append(Constant(value='type', kind=None))
            values.append(Constant(value='exp', kind=None))

            keys.append(Constant(value='name', kind=None))
            values.append(Constant(value=ast_object.id, kind=None))

            keys.append(Constant(value='value', kind=None))
            values.append(ast_object)

            keys.append(Constant(value='column', kind=None))
            values.append(Constant(value=ast_object.col_offset, kind=None))

            keys.append(Constant(value='end_column', kind=None))
            # End col offset represents the next column after the node, assuming a zero based count. Nimoy considers
            # The last character of the node name as the last column, so subtract by 1
            values.append(Constant(value=ast_object.end_col_offset - 1, kind=None))

            keys.append(Constant(value='constant', kind=None))
            values.append(Constant(value=False, kind=None))
        elif type(ast_object) is _ast.Constant:
            keys.append(Constant(value='type', kind=None))
            values.append(Constant(value='exp', kind=None))

            keys.append(Constant(value='name', kind=None))
            values.append(Constant(value=str(ast_object.value), kind=None))

            keys.append(Constant(value='value', kind=None))
            values.append(ast_object)

            keys.append(Constant(value='column', kind=None))
            values.append(Constant(value=ast_object.col_offset, kind=None))

            keys.append(Constant(value='end_column', kind=None))
            # End col offset represents the next column after the node, assuming a zero based count. Nimoy considers
            # The last character of the node name as the last column, so subtract by 1
            values.append(Constant(value=ast_object.end_col_offset - 1, kind=None))

            keys.append(Constant(value='constant', kind=None))
            values.append(Constant(value=True, kind=None))
        elif type(ast_object) is _ast.Attribute:
            next_dict = Dict(keys=[], values=[])

            next_dict.keys.append(Constant(value='type', kind=None))
            next_dict.values.append(Constant(value='exp', kind=None))

            next_dict.keys.append(Constant(value='name', kind=None))
            next_dict.values.append(Constant(value=ast_object.attr, kind=None))

            next_dict.keys.append(Constant(value='value', kind=None))
            next_dict.values.append(ast_object)

            next_dict.keys.append(Constant(value='column', kind=None))
            # Because attributes are separated by a period, the attributes start column can be calculated by adding 1
            # to the end col offset of the attribute's parent
            next_dict.values.append(Constant(value=ast_object.value.end_col_offset + 1, kind=None))

            next_dict.keys.append(Constant(value='end_column', kind=None))
            # End col offset represents the next column after the node, assuming a zero based count. Nimoy considers
            # The last character of the node name as the last column, so subtract by 1
            next_dict.values.append(Constant(value=ast_object.end_col_offset - 1, kind=None))

            next_dict.keys.append(Constant(value='constant', kind=None))
            next_dict.values.append(Constant(value=False, kind=None))

            parent_keys, parent_values = PowerAssertionTransformer.expression_node_ast_to_nimoy_expression_ast(
                ast_object.value)

            parent_keys.append(Constant(value='next', kind=None))
            parent_values.append(next_dict)

            keys.extend(parent_keys)
            values.extend(parent_values)

        return keys, values

    # Fetches the last link from the linked dictionaries
    @staticmethod
    def get_last_dictionary(d: Dict) -> Dict:
        dict_to_return = None

        rightmost_dict = d
        while dict_to_return is None:

            next_found_in_iteration = False
            for i, key in enumerate(rightmost_dict.keys):
                if type(key) != Constant:
                    continue
                if key.value == 'next':
                    next_found_in_iteration = True
                    rightmost_dict = rightmost_dict.values[i]
                    break

            if not next_found_in_iteration:
                dict_to_return = rightmost_dict

        return dict_to_return

    # Transforms the operation AST node into an operation AST dictionary
    @staticmethod
    def op_ast_to_nimoy_op_ast(ast_object, ast_object_col_offset, complete_expression) -> Dict:
        op_dict = Dict(keys=[], values=[])
        op_dict.keys.append(Constant(value='type', kind=None))
        op_dict.values.append(Constant(value='op', kind=None))

        op_dict.keys.append(Constant(value='value', kind=None))
        op_dict.values.append(complete_expression)

        op_dict.keys.append(Constant(value='op', kind=None))
        op = None
        if type(ast_object) is _ast.Eq:
            op = '=='
        op_dict.values.append(Constant(value=op, kind=None))

        op_dict.keys.append(Constant(value='column', kind=None))
        op_dict.values.append(Constant(value=ast_object_col_offset, kind=None))

        return op_dict

    # Breaks the expression into a linked dictionary structure, where every evaluable node in the expression is a node
    # in the structure
    @staticmethod
    def assert_ast_to_nimoy_expression_ast(node_value) -> Dict:
        root_dict = Dict(keys=[], values=[])

        # Transform the left side of the assertion into linked dictionaries
        left = node_value.left
        left_keys_to_append, left_values_to_append = PowerAssertionTransformer.expression_node_ast_to_nimoy_expression_ast(
            left)

        # Append the left nodes to the root
        root_dict.keys.extend(left_keys_to_append)
        root_dict.values.extend(left_values_to_append)

        # Fetch the last dictionary. expression_node_ast_to_nimoy_expression_ast is a recursive operation and always
        # returns the root node. We iterate until we find the last node to which we can then append the next node
        last_dict = PowerAssertionTransformer.get_last_dictionary(root_dict)

        # Transform the operation node to an op dictionary
        op_dict = PowerAssertionTransformer.op_ast_to_nimoy_op_ast(node_value.ops[0], left.end_col_offset + 1,
                                                                   node_value)

        # Append the operation dictionary to the linked dictionaries
        last_dict.keys.append(Constant(value='next', kind=None))
        last_dict.values.append(op_dict)

        # Transform the right side of the assertion into linked dictionaries
        right_dict = Dict(keys=[], values=[])
        right = node_value.comparators[0]
        right_keys_to_append, right_values_to_append = PowerAssertionTransformer.expression_node_ast_to_nimoy_expression_ast(
            right)
        right_dict.keys.extend(right_keys_to_append)
        right_dict.values.extend(right_values_to_append)

        # Append the right nodes to the operation
        op_dict.keys.append(Constant(value='next', kind=None))
        op_dict.values.append(right_dict)

        return root_dict

    # Transforms the comparison expression to a power assert method call
    def visit_Call(self, expression_node):
        value = expression_node.value

        # If the given node isn't a binary comparison operation, return it as is. We only translated expression like
        # jim == bob
        if not isinstance(value, _ast.Compare):
            if isinstance(value, _ast.BinOp):
                if hasattr(value, 'op') and not isinstance(value.op, _ast.MatMult):
                    return expression_node
            else:
                return expression_node

        # Break down the expression into a linked dictionaries made of vanilla dictionaries
        power_assertion_dict = PowerAssertionTransformer.assert_ast_to_nimoy_expression_ast(value)

        # Insert a power assert method call instead of the expression and set the linked dictionaries as an argument
        expression_node.value = _ast.Call(
            func=_ast.Attribute(
                value=_ast.Name(id='self', ctx=_ast.Load()),
                attr='_power_assert',
                ctx=_ast.Load()
            ),
            args=[power_assertion_dict],
            keywords=[]
        )

        return expression_node


class ThrownExpressionTransformer(ast.NodeTransformer):

    def visit_Call(self, expression_node):
        if isinstance(expression_node, _ast.Call):
            if hasattr(expression_node.func, 'id') and expression_node.func.id == 'thrown':
                expected_exception = expression_node.args[0]
                expression_node = _ast.Call(
                    func=_ast.Attribute(
                        value=_ast.Name(id='self', ctx=_ast.Load()),
                        attr='_exception_thrown',
                        ctx=_ast.Load()
                    ),
                    args=[expected_exception],
                    keywords=[]
                )
        return expression_node


class MockBehaviorExpressionTransformer(ast.NodeTransformer):
    def visit_Expr(self, expression_node):
        value = expression_node.value
        if not isinstance(value, _ast.BinOp) or not (
                isinstance(value.op, _ast.RShift) or isinstance(value.op, _ast.LShift)):
            return expression_node

        mock_attribute = 'return_value'
        if isinstance(value.op, _ast.LShift):
            mock_attribute = 'side_effect'

        return _ast.Assign(
            targets=[
                _ast.Attribute(
                    attr=mock_attribute,
                    ctx=_ast.Store(),
                    value=value.left.func
                )
            ],
            value=value.right
        )


class MockAssertionTransformer(ast.NodeTransformer):
    def visit_Expr(self, expression_node):
        value = expression_node.value
        if not isinstance(value, _ast.BinOp) or not isinstance(value.op, _ast.Mult) or not isinstance(value.right,
                                                                                                      _ast.Call):
            return expression_node

        number_of_invocations = value.left
        if MockAssertionTransformer._value_is_a_wildcard(number_of_invocations):
            number_of_invocations = ast_proxy.ast_num(n=-1)
        target_mock = value.right.func.value
        target_method = ast_proxy.ast_str(s=value.right.func.attr)

        list_of_arguments = [MockAssertionTransformer._transform_arg_if_wildcard(x) for x in value.right.args]
        spread_list_of_arguments = _ast.Starred(value=_ast.List(elts=list_of_arguments, ctx=_ast.Load()),
                                                ctx=_ast.Load())
        expression_node.value = _ast.Call(
            func=_ast.Attribute(
                value=_ast.Name(id='self', ctx=_ast.Load()),
                attr='_assert_mock',
                ctx=_ast.Load()
            ),
            args=[number_of_invocations, target_mock, target_method, spread_list_of_arguments],
            keywords=[]
        )
        return expression_node

    @staticmethod
    def _value_is_a_wildcard(value):
        return isinstance(value, _ast.Name) and value.id == '_'

    @staticmethod
    def _transform_arg_if_wildcard(arg):
        if MockAssertionTransformer._value_is_a_wildcard(arg):
            return ast_proxy.ast_str(s='__nimoy_argument_wildcard')

        return arg
