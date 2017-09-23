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
