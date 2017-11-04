import ast
import _ast
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
        }

    def visit_Expr(self, expression_node):
        value = expression_node.value
        if not isinstance(value, _ast.Compare):
            return expression_node

        # TODO: Support multiple comparators (1 < 2 < 3). This may be tricky because one expression of multiple
        # comparators will translate to multiple unittest assert expressions, which will cause a difference in line
        # numbers
        comparison_operation = value.ops[0]
        comparison_operation_type = type(comparison_operation)
        internal_comparison_type = self.comparator_methods[comparison_operation_type]

        expression_node.value = _ast.Call(
            func=_ast.Attribute(
                value=_ast.Name(id='self', ctx=_ast.Load()),
                attr='_compare',
                ctx=_ast.Load()
            ),
            args=[value.left, value.comparators[0], _ast.Str(s=internal_comparison_type.name)],
            keywords=[]
        )
        return expression_node


class MockAssertionTransformer(ast.NodeTransformer):
    def visit_Expr(self, expression_node):
        value = expression_node.value
        if not isinstance(value, _ast.BinOp) or not isinstance(value.op, _ast.Mult) or not isinstance(value.right,
                                                                                                      _ast.Call):
            return expression_node

        number_of_invocations = value.left
        if MockAssertionTransformer._value_is_a_wildcard(number_of_invocations):
            number_of_invocations = _ast.Num(n=-1)
        target_mock = value.right.func.value
        target_method = _ast.Str(s=value.right.func.attr)

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
            return _ast.Str(s='__nimoy_argument_wildcard')

        return arg
