import ast
import copy
import _ast

from nimoy.runner.metadata import RunnerContext
from nimoy.ast_tools.ast_metadata import SpecMetadata
from nimoy.ast_tools.expression_transformer import ComparisonExpressionTransformer, MockAssertionTransformer, \
    ThrownExpressionTransformer, MockBehaviorExpressionTransformer, PowerAssertionTransformer
from nimoy.runner.exceptions import InvalidFeatureBlockException

SETUP = 'setup'
GIVEN = 'given'
WHEN = 'when'
THEN = 'then'
EXPECT = 'expect'
WHERE = 'where'
BLOCK_NAMES = [SETUP, GIVEN, WHEN, THEN, EXPECT, WHERE]


class WhereBlockFunctions:
    def __init__(self, spec_metadata, feature_name) -> None:
        super().__init__()
        self.spec_metadata = spec_metadata
        self.feature_name = feature_name

    def assign_variables_to_the_context(self, where_function_ast_node):
        block_body = where_function_ast_node.body
        first_expression = block_body[0]
        if isinstance(first_expression, _ast.Assign):
            self._assign_list_form_variables(where_function_ast_node)
        elif hasattr(first_expression, 'value') and isinstance(first_expression.value, _ast.BinOp):
            self._assign_matrix_form_variables(where_function_ast_node)

    def _assign_list_form_variables(self, where_function_ast_node):
        copy_of_body = copy.deepcopy(where_function_ast_node.body)
        where_function_ast_node.body = []
        for assignment_expression in copy_of_body:
            variable_name = assignment_expression.targets[0].id
            self.spec_metadata.add_feature_variable(self.feature_name, variable_name)
            variable_values = assignment_expression.value
            where_function_ast_node.body.append(
                _ast.Assign(
                    targets=[
                        _ast.Subscript(
                            value=_ast.Name(id='injectable_values', ctx=_ast.Load()),
                            slice=ast.Str(s=variable_name),
                            ctx=_ast.Store()
                        )
                    ],
                    value=variable_values
                ))

    def _assign_matrix_form_variables(self, where_function_ast_node):
        copy_of_body = copy.deepcopy(where_function_ast_node.body)
        where_function_ast_node.body = []

        variables_and_values = WhereBlockFunctions._get_variables_and_values(copy_of_body)

        # We might be screwing with line numbers here
        for variable_name, variable_values in variables_and_values.items():
            self.spec_metadata.add_feature_variable(self.feature_name, variable_name)
            where_function_ast_node.body.append(
                _ast.Assign(
                    targets=[
                        _ast.Subscript(
                            value=_ast.Name(id='injectable_values', ctx=_ast.Load()),
                            slice=ast.Str(s=variable_name),
                            ctx=_ast.Store()
                        )
                    ],
                    value=_ast.List(elts=variable_values, ctx=_ast.Load())
                ))

    @staticmethod
    def _get_variables_and_values(copy_of_body):
        variable_names_row = copy_of_body[0].value
        variable_names = []
        WhereBlockFunctions._collect_variable_names_recursively(variable_names_row, variable_names)
        variables_and_values = {variable_names[i]: [] for i in range(len(variable_names))}
        for values_row in copy_of_body[1:]:
            variable_values = []
            WhereBlockFunctions._collect_variable_values_recursively(values_row.value, variable_values)
            for index, value in enumerate(variable_values):
                variables_and_values[variable_names[index]].append(value)
        return variables_and_values

    @staticmethod
    def _collect_variable_names_recursively(binary_op_node, variable_names):
        if isinstance(binary_op_node.left, _ast.BinOp):
            WhereBlockFunctions._collect_variable_names_recursively(binary_op_node.left, variable_names)
        else:
            variable_names.append(WhereBlockFunctions._get_variable_name(binary_op_node.left))
        variable_names.append(WhereBlockFunctions._get_variable_name(binary_op_node.right))

    @staticmethod
    def _get_variable_name(variable_object):
        if hasattr(variable_object, 's'):
            return variable_object.s
        return variable_object.id

    @staticmethod
    def _collect_variable_values_recursively(binary_op_node, variable_values):
        if isinstance(binary_op_node.left, _ast.BinOp):
            WhereBlockFunctions._collect_variable_values_recursively(binary_op_node.left, variable_values)
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
                if any((existing_block in [SETUP, GIVEN]) for existing_block in existing_blocks):
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
    def __init__(self, runner_context: RunnerContext, spec_metadata: SpecMetadata, feature_name: str) -> None:
        super().__init__()
        self.runner_context = runner_context
        self.spec_metadata = spec_metadata
        self.feature_name = feature_name

    def visit_With(self, with_node):

        if FeatureBlockTransformer._is_feature_block(with_node):
            block_type = with_node.items[0].context_expr.id
            FeatureBlockRuleEnforcer(self.spec_metadata, self.feature_name, with_node).enforce_addition_rules(
                block_type)
            self.spec_metadata.add_feature_block(self.feature_name, block_type)

            if block_type != WHERE:
                FeatureBlockTransformer._replace_with_block_context(with_node, block_type)
                if block_type == WHEN:
                    MockBehaviorExpressionTransformer().visit(with_node)

                if block_type in [THEN, EXPECT]:
                    if self.runner_context.use_power_assertions:
                        PowerAssertionTransformer().visit(with_node)
                    else:
                        ComparisonExpressionTransformer().visit(with_node)

                if block_type == THEN:
                    MockAssertionTransformer().visit(with_node)
                    ThrownExpressionTransformer().visit(with_node)
                return with_node

            where_function = self._replace_where_block_with_function(with_node)
            WhereBlockFunctions(self.spec_metadata, self.feature_name).assign_variables_to_the_context(where_function)
            self.spec_metadata.add_where_function(self.feature_name, copy.deepcopy(where_function))
            return where_function

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
                                ctx=_ast.Load()), args=[ast.Str(s=block_type)], keywords=[])

    def _replace_where_block_with_function(self, with_node):
        return _ast.FunctionDef(name=self.feature_name + '_where',
                                args=_ast.arguments(
                                    args=[_ast.arg(arg='self'), _ast.arg(arg='injectable_values')],
                                    posonlyargs=[],
                                    kwonlyargs=[],
                                    kw_defaults=[],
                                    defaults=[]),
                                body=copy.deepcopy(with_node.body),
                                decorator_list=[],
                                returns=None)
