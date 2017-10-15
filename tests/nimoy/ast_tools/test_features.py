import unittest
from unittest import mock
import ast
from nimoy.ast_tools.features import FeatureRegistrationTransformer
from nimoy.ast_tools.ast_metadata import SpecMetadata


class FeatureRegistrationTransformerTest(unittest.TestCase):
    @mock.patch('nimoy.ast_tools.features.FeatureBlockRuleEnforcer')
    @mock.patch('nimoy.ast_tools.features.FeatureBlockTransformer')
    def test_that_a_feature_was_added(self, feature_block_transformer, feature_block_rule_enforcer):
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

    @mock.patch('nimoy.ast_tools.features.FeatureBlockRuleEnforcer')
    @mock.patch('nimoy.ast_tools.features.FeatureBlockTransformer')
    def test_that_a_feature_with_where_block_was_added(self, feature_block_transformer, feature_block_rule_enforcer):
        module_definition = 'class JSpec:\n    def test_jim(self):\n        pass\n\n'
        node = ast.parse(module_definition, mode='exec')

        metadata = SpecMetadata('jim')

        def visit(feature_node):
            metadata.add_feature_variable('test_jim', 'var_a')
            metadata.add_where_function('test_jim', {'name': 'test_jim_where'})
            where_function_mock = mock.Mock()
            where_function_mock.name = 'test_jim_where'
            feature_node.body.append(where_function_mock)

        feature_block_transformer.return_value.visit.side_effect = visit

        FeatureRegistrationTransformer(metadata).visit(node)
        self.assertEqual(len(metadata.features), 1)
        self.assertEqual(metadata.features[0], 'test_jim')

        feature_block_transformer.assert_called_once_with(metadata, 'test_jim')
        feature_block_transformer.return_value.visit.assert_called_once_with(node.body[0].body[0])

        feature_block_rule_enforcer.assert_called_once_with(metadata, 'test_jim', node.body[0].body[0])
        feature_block_rule_enforcer.return_value.enforce_tail_end_rules.assert_called_once()

        self.assertEqual(len(node.body[0].body[0].body), 1,
                         'The nested where function that as added should have been removed from the feature')

        self.assertEqual(len(node.body[0].body[0].args.args), 2,
                         'The feature should receive 2 parameters - self and a variable')

        self.assertEqual(node.body[0].body[0].args.args[1].arg, 'var_a')
