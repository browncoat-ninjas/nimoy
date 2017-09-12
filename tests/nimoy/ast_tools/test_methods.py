import unittest
from unittest import mock
import ast
from nimoy.ast_tools.methods import MethodRegistrationTransformer
from nimoy.ast_tools.ast_metadata import SpecMetadata


class MethodRegistrationTransformerTest(unittest.TestCase):
    @mock.patch('nimoy.ast_tools.methods.MethodBlockRuleEnforcer')
    @mock.patch('nimoy.ast_tools.methods.MethodBlockTransformer')
    def test_that_function_was_added(self, method_block_transformer, method_block_rule_enforcer):
        module_definition = 'class JSpec:\n    def test_jim(self):\n        pass\n    def _jim(self):\n        pass\n\n'
        node = ast.parse(module_definition, mode='exec')

        metadata = SpecMetadata('jim')
        MethodRegistrationTransformer(metadata).visit(node)
        self.assertEqual(len(metadata.methods), 1)
        self.assertEqual(metadata.methods[0], 'test_jim')

        method_block_transformer.assert_called_once_with(metadata, 'test_jim')
        method_block_transformer.return_value.visit.assert_called_once_with(node.body[0].body[0])

        method_block_rule_enforcer.assert_called_once_with(metadata, 'test_jim', node.body[0].body[0])
        method_block_rule_enforcer.return_value.enforce_tail_end_rules.assert_called_once()
