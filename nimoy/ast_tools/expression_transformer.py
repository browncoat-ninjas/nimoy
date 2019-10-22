import _ast
import ast

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
