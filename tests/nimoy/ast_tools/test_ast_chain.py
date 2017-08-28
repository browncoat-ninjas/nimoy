import unittest
from unittest import mock
from nimoy.ast_tools import ast_chain


class TestAstChain(unittest.TestCase):
    @mock.patch('nimoy.ast_tools.ast_chain.SpecTransformer')
    @mock.patch('nimoy.ast_tools.ast_chain.ModuleTransformer')
    def test_apply(self, spec_transformer_mock, module_transformer_mock):
        node = {}

        spec_metadata = ast_chain.apply(node)
        self.assertTrue(isinstance(spec_metadata, list))

        spec_transformer_mock.assert_called_once()
        spec_transformer_mock.return_value.visit.assert_called_once_with(node)

        module_transformer_mock.assert_called_once()
        module_transformer_mock.return_value.visit.assert_called_once_with(node)
