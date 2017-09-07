import ast
import _ast
from nimoy.ast_tools.expression_transformer import ComparisonExpressionTransformer
from nimoy.runner.exceptions import InvalidMethodBlockException

SETUP = 'setup'
GIVEN = 'given'
WHEN = 'when'
THEN = 'then'
EXPECT = 'expect'
WHERE = 'where'
BLOCK_NAMES = [SETUP, GIVEN, WHEN, THEN, EXPECT, WHERE]


class MethodBlockRuleEnforcer:
    def __init__(self, spec_metadata, method_name, block_ast_node) -> None:
        super().__init__()
        self.spec_metadata = spec_metadata
        self.method_name = method_name
        self.block_ast_node = block_ast_node

    def enforce_addition_rules(self, block_type):
        existing_blocks = self.spec_metadata.method_blocks.get(self.method_name)

        if block_type in [SETUP, GIVEN]:
            if existing_blocks:
                if any([(existing_block in [SETUP, GIVEN]) for existing_block in existing_blocks]):
                    raise InvalidMethodBlockException(self.spec_metadata, self.method_name, self.block_ast_node,
                                                      'Each feature method may only have a single setup/given block')

                raise InvalidMethodBlockException(self.spec_metadata, self.method_name, self.block_ast_node,
                                                  'setup/given blocks may only appear at the start of the feature')

        if block_type == THEN:
            if (existing_blocks and existing_blocks[-1] != WHEN) or not existing_blocks:
                raise InvalidMethodBlockException(self.spec_metadata, self.method_name, self.block_ast_node,
                                                  'when blocks may only succeed then blocks')

        if block_type != THEN:
            if existing_blocks:
                if existing_blocks[-1] == WHEN:
                    raise InvalidMethodBlockException(self.spec_metadata, self.method_name, self.block_ast_node,
                                                      'when blocks may be succeeded only by then blocks')

        if existing_blocks:
            if existing_blocks[-1] == WHERE:
                raise InvalidMethodBlockException(self.spec_metadata, self.method_name, self.block_ast_node,
                                                  'No blocks may succeeded where blocks')

    def enforce_tail_end_rules(self):
        existing_blocks = self.spec_metadata.method_blocks.get(self.method_name)
        if existing_blocks:
            if existing_blocks[-1] == WHEN:
                raise InvalidMethodBlockException(self.spec_metadata, self.method_name, self.block_ast_node,
                                                  'when blocks must be succeeded by a then block')
            if existing_blocks[-1] in [SETUP, GIVEN]:
                raise InvalidMethodBlockException(self.spec_metadata, self.method_name, self.block_ast_node,
                                                  'Feature methods cannot end with a setup or a given block')


class MethodBlockTransformer(ast.NodeTransformer):
    def __init__(self, spec_metadata, method_name) -> None:
        super().__init__()
        self.spec_metadata = spec_metadata
        self.method_name = method_name

    def visit_With(self, with_node):

        if MethodBlockTransformer._is_method_block(with_node):
            block_type = with_node.items[0].context_expr.id
            MethodBlockRuleEnforcer(self.spec_metadata, self.method_name, with_node).enforce_addition_rules(block_type)
            MethodBlockTransformer._replace_with_block_context(with_node, block_type)
            self.spec_metadata.add_method_block(self.method_name, block_type)

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
