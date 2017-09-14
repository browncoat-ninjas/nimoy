import ast
import _ast
from nimoy.ast_tools.expression_transformer import ComparisonExpressionTransformer
from nimoy.runner.exceptions import InvalidFeatureBlockException

SETUP = 'setup'
GIVEN = 'given'
WHEN = 'when'
THEN = 'then'
EXPECT = 'expect'
WHERE = 'where'
BLOCK_NAMES = [SETUP, GIVEN, WHEN, THEN, EXPECT, WHERE]


class WhereBlockVariables:
    def __init__(self, spec_metadata, feature_name) -> None:
        super().__init__()
        self.spec_metadata = spec_metadata
        self.feature_name = feature_name

    def register_variables(self, block_ast_node):
        block_body = block_ast_node.body
        first_expression = block_body[0]
        if isinstance(first_expression, _ast.Assign):
            self._register_list_form_variables(block_body)
        elif hasattr(first_expression, 'value') and isinstance(first_expression.value, _ast.BinOp):
            self._register_matrix_form_variables(block_body)

    def _register_list_form_variables(self, block_body):
        for assignment_expression in block_body:
            variable_name = assignment_expression.targets[0].id
            variable_values = assignment_expression.value.elts
            self.spec_metadata.add_feature_variable_values(self.feature_name, variable_name, variable_values)

    def _register_matrix_form_variables(self, block_body):
        variable_names_row = block_body[0].value
        variable_names = []
        self._collect_variable_names_recursively(variable_names_row, variable_names)

        for values_row in block_body[1:]:
            variable_values = []
            self._collect_variable_values_recursively(values_row.value, variable_values)
            for index, value in enumerate(variable_values):
                self.spec_metadata.add_feature_variable_value(self.feature_name, variable_names[index], value)

    def _collect_variable_names_recursively(self, binary_op_node, variable_names):
        if isinstance(binary_op_node.left, _ast.BinOp):
            self._collect_variable_names_recursively(binary_op_node.left, variable_names)
        else:
            variable_names.append(binary_op_node.left.id)
        variable_names.append(binary_op_node.right.id)

    def _collect_variable_values_recursively(self, binary_op_node, variable_values):
        if isinstance(binary_op_node.left, _ast.BinOp):
            self._collect_variable_values_recursively(binary_op_node.left, variable_values)
        else:
            variable_values.append(binary_op_node.left)
        variable_values.append(binary_op_node.right)


class FeatureBlockRuleEnforcer:
    def __init__(self, spec_metadata, feature_name, block_ast_node) -> None:
        super().__init__()
        self.spec_metadata = spec_metadata
        self.feature_name = feature_name
        self.block_ast_node = block_ast_node

    def enforce_addition_rules(self, block_type):
        existing_blocks = self.spec_metadata.feature_blocks.get(self.feature_name)

        if block_type in [SETUP, GIVEN]:
            if existing_blocks:
                if any([(existing_block in [SETUP, GIVEN]) for existing_block in existing_blocks]):
                    raise InvalidFeatureBlockException(self.spec_metadata, self.feature_name, self.block_ast_node,
                                                       'Each feature may only have a single setup/given block')

                raise InvalidFeatureBlockException(self.spec_metadata, self.feature_name, self.block_ast_node,
                                                   'setup/given blocks may only appear at the start of the feature')

        if block_type == THEN:
            if (existing_blocks and existing_blocks[-1] != WHEN) or not existing_blocks:
                raise InvalidFeatureBlockException(self.spec_metadata, self.feature_name, self.block_ast_node,
                                                   'when blocks may only succeed then blocks')

        if block_type != THEN:
            if existing_blocks:
                if existing_blocks[-1] == WHEN:
                    raise InvalidFeatureBlockException(self.spec_metadata, self.feature_name, self.block_ast_node,
                                                       'when blocks may be succeeded only by then blocks')

        if existing_blocks:
            if existing_blocks[-1] == WHERE:
                raise InvalidFeatureBlockException(self.spec_metadata, self.feature_name, self.block_ast_node,
                                                   'No blocks may succeeded where blocks')

    def enforce_tail_end_rules(self):
        existing_blocks = self.spec_metadata.feature_blocks.get(self.feature_name)
        if existing_blocks:
            if existing_blocks[-1] == WHEN:
                raise InvalidFeatureBlockException(self.spec_metadata, self.feature_name, self.block_ast_node,
                                                   'when blocks must be succeeded by a then block')
            if existing_blocks[-1] in [SETUP, GIVEN]:
                raise InvalidFeatureBlockException(self.spec_metadata, self.feature_name, self.block_ast_node,
                                                   'Features cannot end with a setup or a given block')


class FeatureBlockTransformer(ast.NodeTransformer):
    def __init__(self, spec_metadata, feature_name) -> None:
        super().__init__()
        self.spec_metadata = spec_metadata
        self.feature_name = feature_name

    def visit_With(self, with_node):

        if FeatureBlockTransformer._is_feature_block(with_node):
            block_type = with_node.items[0].context_expr.id
            FeatureBlockRuleEnforcer(self.spec_metadata, self.feature_name, with_node).enforce_addition_rules(block_type)
            FeatureBlockTransformer._replace_with_block_context(with_node, block_type)
            self.spec_metadata.add_feature_block(self.feature_name, block_type)

            if block_type in [THEN, EXPECT]:
                ComparisonExpressionTransformer().visit(with_node)

            if block_type == WHERE:
                WhereBlockVariables(self.spec_metadata, self.feature_name).register_variables(with_node)

        return with_node

    @staticmethod
    def _is_feature_block(with_node):
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
            func=_ast.Attribute(value=_ast.Name(id='self', ctx=_ast.Load()), attr='_feature_block_context',
                                ctx=_ast.Load()), args=[_ast.Str(s=block_type)], keywords=[])
