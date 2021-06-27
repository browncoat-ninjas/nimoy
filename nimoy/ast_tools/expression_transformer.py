import ast
import _ast
from _ast import Dict, Constant

import astor

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
            args=[left_value, right_value, ast.Str(s=internal_comparison_type.name)],
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

    @staticmethod
    def _append_expression_keys(d: Dict):
        d.keys.extend([Constant(value='type', kind=None), Constant(value='name', kind=None),
                       Constant(value='value', kind=None), Constant(value='column', kind=None),
                       Constant(value='end_column', kind=None), Constant(value='constant', kind=None)])

    @staticmethod
    def _append_name_as_expression_values(root_expression_offset: int, ast_object: _ast.Name, d: Dict):
        d.values.extend([Constant(value='exp', kind=None), Constant(value=ast_object.id, kind=None), ast_object,
                         Constant(value=ast_object.col_offset - root_expression_offset, kind=None),
                         Constant(value=ast_object.end_col_offset - root_expression_offset - 1, kind=None),
                         Constant(value=False, kind=None)])

    @staticmethod
    def _append_constant_as_expression_values(root_expression_offset: int, ast_object: _ast.Constant, d: Dict):
        d.values.extend([Constant(value='exp', kind=None), Constant(value=str(ast_object.value), kind=None), ast_object,
                         Constant(value=ast_object.col_offset - root_expression_offset, kind=None),
                         Constant(value=ast_object.end_col_offset - root_expression_offset - 1, kind=None),
                         Constant(value=True, kind=None)])

    @staticmethod
    def _append_attribute_as_expression_values(root_expression_offset: int, ast_object: _ast.Attribute, d: Dict):
        d.values.extend([Constant(value='exp', kind=None), Constant(value=str(ast_object.attr), kind=None), ast_object,
                         Constant(value=ast_object.value.end_col_offset - root_expression_offset + 1, kind=None),
                         Constant(value=ast_object.end_col_offset - root_expression_offset - 1, kind=None),
                         Constant(value=False, kind=None)])

    @staticmethod
    def _append_call_as_expression_values(root_expression_offset: int, ast_object: _ast.Call, d: Dict):

        if isinstance(ast_object.func, _ast.Name):
            name = astor.to_source(ast_object).strip()
            column = ast_object.col_offset - root_expression_offset
        elif isinstance(ast_object.func, _ast.Attribute):
            name = astor.to_source(ast_object).strip()[
                   ast_object.func.value.end_col_offset - ast_object.func.value.col_offset + 1:]
            column = ast_object.func.value.end_col_offset - root_expression_offset + 1
        else:
            raise Exception(f"{type(ast_object.func)} is unsupported")

        d.values.extend([Constant(value='exp', kind=None), Constant(value=name, kind=None), ast_object,
                         Constant(value=column, kind=None),
                         Constant(value=ast_object.end_col_offset - root_expression_offset - 1, kind=None),
                         Constant(value=False, kind=None)])

    @staticmethod
    def _append_subscript_as_expression_values(root_expression_offset: int, root_subscript: _ast.Subscript,
                                               subscript_target, d: Dict):

        if isinstance(subscript_target, _ast.Name):
            name = astor.to_source(root_subscript).strip()
            column = subscript_target.col_offset - root_expression_offset
        elif isinstance(subscript_target, _ast.Attribute):
            name = astor.to_source(root_subscript).strip()[
                   subscript_target.value.end_col_offset - subscript_target.value.col_offset + 1:]
            column = subscript_target.value.end_col_offset - root_expression_offset + 1
        else:
            raise Exception(f"{type(root_subscript.value)} is unsupported")

        d.values.extend([Constant(value='exp', kind=None), Constant(value=name, kind=None), root_subscript,
                         Constant(value=column, kind=None),
                         Constant(value=root_subscript.end_col_offset - root_expression_offset - 1, kind=None),
                         Constant(value=False, kind=None)])

    @staticmethod
    def _append_struct_literal_as_expression_values(root_expression_offset: int, ast_object, d: Dict):
        d.values.extend(
            [Constant(value='exp', kind=None), Constant(value=astor.to_source(ast_object).strip(), kind=None),
             ast_object, Constant(value=ast_object.col_offset - root_expression_offset, kind=None),
             Constant(value=ast_object.end_col_offset - root_expression_offset - 1, kind=None),
             Constant(value=True, kind=None)])

    # Transform the expression node AST to a linked dictionary structure AST. Supported nodes are Name,
    # Constant and Attribute. Recursion occurs on every attribute node.
    # The method always returns the root link
    @staticmethod
    def expression_node_ast_to_nimoy_expression_ast(root_expression_offset: int, ast_object) -> Dict:

        dict_to_return: Dict = None

        while ast_object is not None:
            d = Dict(keys=[], values=[])
            if isinstance(ast_object, _ast.Name):
                PowerAssertionTransformer._append_expression_keys(d)
                PowerAssertionTransformer._append_name_as_expression_values(root_expression_offset, ast_object, d)
                if dict_to_return is not None:
                    d.keys.append(Constant(value='next', kind=None))
                    d.values.append(dict_to_return)
                dict_to_return = d
                ast_object = None
            elif isinstance(ast_object, _ast.Constant):
                PowerAssertionTransformer._append_expression_keys(d)
                PowerAssertionTransformer._append_constant_as_expression_values(root_expression_offset, ast_object, d)
                if dict_to_return is not None:
                    d.keys.append(Constant(value='next', kind=None))
                    d.values.append(dict_to_return)
                dict_to_return = d
                ast_object = None
            elif isinstance(ast_object, _ast.Attribute):
                PowerAssertionTransformer._append_expression_keys(d)
                PowerAssertionTransformer._append_attribute_as_expression_values(root_expression_offset, ast_object, d)
                if dict_to_return is not None:
                    d.keys.append(Constant(value='next', kind=None))
                    d.values.append(dict_to_return)
                dict_to_return = d
                ast_object = ast_object.value
            elif isinstance(ast_object, _ast.Call):
                PowerAssertionTransformer._append_expression_keys(d)
                PowerAssertionTransformer._append_call_as_expression_values(root_expression_offset, ast_object, d)
                if dict_to_return is not None:
                    d.keys.append(Constant(value='next', kind=None))
                    d.values.append(dict_to_return)
                dict_to_return = d
                if isinstance(ast_object.func, _ast.Attribute):
                    ast_object = ast_object.func.value
                else:
                    ast_object = None
            elif isinstance(ast_object, _ast.Subscript):
                PowerAssertionTransformer._append_expression_keys(d)

                target = ast_object.value
                while isinstance(target, _ast.Subscript):
                    target = target.value

                PowerAssertionTransformer._append_subscript_as_expression_values(root_expression_offset, ast_object,
                                                                                 target, d)
                if dict_to_return is not None:
                    d.keys.append(Constant(value='next', kind=None))
                    d.values.append(dict_to_return)
                dict_to_return = d
                if isinstance(target, _ast.Attribute):
                    ast_object = target.value
                else:
                    ast_object = None
            elif type(ast_object) in [_ast.List, _ast.Dict]:
                PowerAssertionTransformer._append_expression_keys(d)
                PowerAssertionTransformer._append_struct_literal_as_expression_values(root_expression_offset,
                                                                                      ast_object, d)
                if dict_to_return is not None:
                    d.keys.append(Constant(value='next', kind=None))
                    d.values.append(dict_to_return)
                dict_to_return = d
                ast_object = None
            else:
                raise Exception(
                    f"AST object of type {type(ast_object)} ({astor.to_source(ast_object).strip()}) is unsupported")

        return dict_to_return

    # Fetches the last link from the linked dictionaries
    @staticmethod
    def get_last_dictionary(d: Dict) -> Dict:
        dict_to_return = None

        rightmost_dict = d
        while dict_to_return is None:

            next_found_in_iteration = False
            for i, key in enumerate(rightmost_dict.keys):
                if not isinstance(key, Constant):
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
        if isinstance(ast_object, _ast.Eq):
            op = '=='
        op_dict.values.append(Constant(value=op, kind=None))

        op_dict.keys.append(Constant(value='column', kind=None))
        op_dict.values.append(Constant(value=ast_object_col_offset, kind=None))

        return op_dict

    # Breaks the expression into a linked dictionary structure, where every evaluable node in the expression is a node
    # in the structure
    @staticmethod
    def assert_ast_to_nimoy_expression_ast(root_expression_offset: int, node_value) -> Dict:

        # Transform the left side of the assertion into linked dictionaries
        left = node_value.left
        root_dict = PowerAssertionTransformer.expression_node_ast_to_nimoy_expression_ast(root_expression_offset, left)

        # Fetch the last dictionary. expression_node_ast_to_nimoy_expression_ast is a recursive operation and always
        # returns the root node. We iterate until we find the last node to which we can then append the next node
        last_dict = PowerAssertionTransformer.get_last_dictionary(root_dict)

        # Transform the operation node to an op dictionary
        op_dict = PowerAssertionTransformer.op_ast_to_nimoy_op_ast(node_value.ops[0],
                                                                   left.end_col_offset - root_expression_offset + 1,
                                                                   node_value)

        # Append the operation dictionary to the linked dictionaries
        last_dict.keys.append(Constant(value='next', kind=None))
        last_dict.values.append(op_dict)

        # Transform the right side of the assertion into linked dictionaries
        right = node_value.comparators[0]
        right_dict = PowerAssertionTransformer.expression_node_ast_to_nimoy_expression_ast(root_expression_offset,
                                                                                           right)

        # Append the right nodes to the operation
        op_dict.keys.append(Constant(value='next', kind=None))
        op_dict.values.append(right_dict)

        return root_dict

    # Transforms the comparison expression to a power assert method call
    def visit_Expr(self, expression_node):
        root_expression_offset = expression_node.col_offset
        value = expression_node.value

        if isinstance(value, _ast.BinOp):
            if hasattr(value, 'op') and isinstance(value.op, _ast.MatMult):
                return ComparisonExpressionTransformer().visit_Expr(expression_node)

        # If the given node isn't a binary comparison operation, return it as is. We only translated expression like
        # jim == bob
        if not isinstance(value, _ast.Compare):
            return expression_node

        # Break down the expression into a linked dictionaries made of vanilla dictionaries
        power_assertion_dict = PowerAssertionTransformer.assert_ast_to_nimoy_expression_ast(root_expression_offset,
                                                                                            value)

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
        if not isinstance(value, _ast.BinOp) or not isinstance(value.op, (_ast.RShift, _ast.LShift)):
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
            number_of_invocations = ast.Num(n=-1)
        target_mock = value.right.func.value
        target_method = ast.Str(s=value.right.func.attr)

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
            return ast.Str(s='__nimoy_argument_wildcard')

        return arg
