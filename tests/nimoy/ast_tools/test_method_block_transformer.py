import unittest
import ast
from unittest import mock
from nimoy.ast_tools.method_block_transformer import MethodBlockTransformer


class MethodBlockTransformerTest(unittest.TestCase):
    @mock.patch('nimoy.ast_tools.method_block_transformer.ComparisonExpressionTransformer')
    def test_that_function_was_added(self, comparison_expression_transformer):
        module_definition = """from nimoy.specification import Specification
class JimbobSpec(Specification):
    def test_it(self):
        with setup:
            pass

        with given:
            pass

        with when:
            pass

        with then:
            pass

        with expect:
            pass
        """
        node = ast.parse(module_definition, mode='exec')

        MethodBlockTransformer().visit(node)

        spec_method_body = node.body[1].body[0].body

        block_types = ['setup', 'given', 'when', 'then', 'expect']
        for index, block_type in enumerate(block_types):
            self.assertEqual(spec_method_body[index].items[0].context_expr.func.attr, '_method_block_context')
            self.assertEqual(spec_method_body[index].items[0].context_expr.args[0].s, block_type)

        self.assertEqual(comparison_expression_transformer.call_count, 2)
        self.assertEqual(comparison_expression_transformer.return_value.visit.call_count, 2)
