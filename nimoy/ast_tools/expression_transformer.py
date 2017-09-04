import ast
import _ast


class ComparisonExpressionTransformer(ast.NodeTransformer):
    def __init__(self) -> None:
        super().__init__()
        self.comparator_methods = {
            _ast.Eq: 'assertEqual',
            _ast.NotEq: 'assertNotEqual',
            _ast.Lt: 'assertLess',
            _ast.LtE: 'assertLessEqual',
            _ast.Gt: 'assertGreater',
            _ast.GtE: 'assertGreaterEqual',
            _ast.Is: 'assertIs',
            _ast.IsNot: 'assertIsNot',
            _ast.In: 'assertIn',
            _ast.NotIn: 'assertNotIn',
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
        unittest_operation = self.comparator_methods[comparison_operation_type]

        expression_node.value = _ast.Call(
            func=_ast.Attribute(
                value=_ast.Name(id='self', ctx=_ast.Load()),
                attr=unittest_operation,
                ctx=_ast.Load()
            ),
            args=[value.left, value.comparators[0]],
            keywords=[]
        )
        return expression_node
