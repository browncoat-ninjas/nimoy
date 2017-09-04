import ast
import _ast
from nimoy.ast_tools.expression_transformer import ComparisonExpressionTransformer

THEN = 'then'
EXPECT = 'expect'
BLOCK_NAMES = ['setup', 'given', 'when', THEN, EXPECT]


class MethodBlockTransformer(ast.NodeTransformer):
    def visit_With(self, with_node):

        if MethodBlockTransformer._is_method_block(with_node):
            block_type = with_node.items[0].context_expr.id
            MethodBlockTransformer._replace_with_block_context(with_node, block_type)

            if block_type in [THEN, EXPECT]:
                ComparisonExpressionTransformer().visit(with_node)

        return with_node

    @staticmethod
    def _is_method_block(with_node):
        if len(with_node.items) != 1:
            return False

        items = with_node.items[0]
        if not items.context_expr:
            return False

        if not items.context_expr.id:
            return False

        return items.context_expr.id in BLOCK_NAMES

    @staticmethod
    def _replace_with_block_context(with_node, block_type):
        with_node.items[0].context_expr = _ast.Call(
            func=_ast.Attribute(value=_ast.Name(id='self', ctx=_ast.Load()), attr='_method_block_context',
                                ctx=_ast.Load()), args=[_ast.Str(s=block_type)], keywords=[])
