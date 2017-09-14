import unittest
from unittest import mock
import ast
from nimoy.ast_tools.features import FeatureRegistrationTransformer
from nimoy.ast_tools.ast_metadata import SpecMetadata


class FeatureRegistrationTransformerTest(unittest.TestCase):
    @mock.patch('nimoy.ast_tools.features.FeatureBlockRuleEnforcer')
    @mock.patch('nimoy.ast_tools.features.FeatureBlockTransformer')
    def test_that_feature_was_added(self, feature_block_transformer, feature_block_rule_enforcer):
        module_definition = 'class JSpec:\n    def test_jim(self):\n        pass\n    def _jim(self):\n        pass\n\n'
        node = ast.parse(module_definition, mode='exec')

        metadata = SpecMetadata('jim')
        FeatureRegistrationTransformer(metadata).visit(node)
        self.assertEqual(len(metadata.features), 1)
        self.assertEqual(metadata.features[0], 'test_jim')

        feature_block_transformer.assert_called_once_with(metadata, 'test_jim')
        feature_block_transformer.return_value.visit.assert_called_once_with(node.body[0].body[0])

        feature_block_rule_enforcer.assert_called_once_with(metadata, 'test_jim', node.body[0].body[0])
        feature_block_rule_enforcer.return_value.enforce_tail_end_rules.assert_called_once()
