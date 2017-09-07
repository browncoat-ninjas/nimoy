import unittest
import ast
from unittest import mock
from nimoy.ast_tools.method_blocks import MethodBlockTransformer
from nimoy.ast_tools.method_blocks import MethodBlockRuleEnforcer
from nimoy.ast_tools.ast_metadata import SpecMetadata
from nimoy.runner.exceptions import InvalidMethodBlockException


class MethodBlockRuleEnforcerTest(unittest.TestCase):
    def test_add_setup_and_given_as_first_blocks(self):
        spec_metadata = get_basic_spec_metadata()
        enforcer = MethodBlockRuleEnforcer(spec_metadata, 'test_it', {})

        enforcer.enforce_addition_rules('given')
        enforcer.enforce_addition_rules('setup')

    def test_only_one_setup_and_given_are_allowed(self):
        spec_metadata = get_basic_spec_metadata()
        spec_metadata.add_method_block('test_it', 'given')
        enforcer = MethodBlockRuleEnforcer(spec_metadata, 'test_it', {})

        with self.assertRaises(InvalidMethodBlockException):
            enforcer.enforce_addition_rules('given')

        with self.assertRaises(InvalidMethodBlockException):
            enforcer.enforce_addition_rules('setup')

        spec_metadata = get_basic_spec_metadata()
        spec_metadata.add_method_block('test_it', 'setup')
        enforcer = MethodBlockRuleEnforcer(spec_metadata, 'test_it', {})

        with self.assertRaises(InvalidMethodBlockException):
            enforcer.enforce_addition_rules('given')

        with self.assertRaises(InvalidMethodBlockException):
            enforcer.enforce_addition_rules('setup')

    def test_setup_and_given_are_allowed_only_in_the_beginning(self):
        spec_metadata = get_basic_spec_metadata()
        spec_metadata.add_method_block('test_it', 'expect')
        enforcer = MethodBlockRuleEnforcer(spec_metadata, 'test_it', {})

        with self.assertRaises(InvalidMethodBlockException):
            enforcer.enforce_addition_rules('given')

        with self.assertRaises(InvalidMethodBlockException):
            enforcer.enforce_addition_rules('setup')

    def test_setup_and_given_cant_dangle(self):
        spec_metadata = get_basic_spec_metadata()
        spec_metadata.add_method_block('test_it', 'given')
        enforcer = MethodBlockRuleEnforcer(spec_metadata, 'test_it', {})
        with self.assertRaises(InvalidMethodBlockException):
            enforcer.enforce_tail_end_rules()

        spec_metadata = get_basic_spec_metadata()
        spec_metadata.add_method_block('test_it', 'setup')
        enforcer = MethodBlockRuleEnforcer(spec_metadata, 'test_it', {})
        with self.assertRaises(InvalidMethodBlockException):
            enforcer.enforce_tail_end_rules()

    def test_then_cant_precede_when(self):
        spec_metadata = get_basic_spec_metadata()

        enforcer = MethodBlockRuleEnforcer(spec_metadata, 'test_it', {})

        with self.assertRaises(InvalidMethodBlockException):
            enforcer.enforce_addition_rules('then')

        spec_metadata.add_method_block('test_it', 'expect')

        with self.assertRaises(InvalidMethodBlockException):
            enforcer.enforce_addition_rules('then')

    def test_when_cant_dangle(self):
        spec_metadata = get_basic_spec_metadata()
        spec_metadata.add_method_block('test_it', 'when')

        enforcer = MethodBlockRuleEnforcer(spec_metadata, 'test_it', {})

        with self.assertRaises(InvalidMethodBlockException):
            enforcer.enforce_addition_rules('expect')

        with self.assertRaises(InvalidMethodBlockException):
            enforcer.enforce_tail_end_rules()

    def test_then_after_when(self):
        spec_metadata = get_basic_spec_metadata()
        spec_metadata.add_method_block('test_it', 'when')

        enforcer = MethodBlockRuleEnforcer(spec_metadata, 'test_it', {})
        enforcer.enforce_addition_rules('then')

    def test_block_cant_succeed_where(self):
        spec_metadata = get_basic_spec_metadata()
        spec_metadata.add_method_block('test_it', 'where')

        enforcer = MethodBlockRuleEnforcer(spec_metadata, 'test_it', {})

        with self.assertRaises(InvalidMethodBlockException):
            enforcer.enforce_addition_rules('expect')

    def test_cant_add_more_than_one_where(self):
        spec_metadata = get_basic_spec_metadata()
        spec_metadata.add_method_block('test_it', 'where')

        enforcer = MethodBlockRuleEnforcer(spec_metadata, 'test_it', {})

        with self.assertRaises(InvalidMethodBlockException):
            enforcer.enforce_addition_rules('where')


class MethodBlockTransformerTest(unittest.TestCase):
    @mock.patch('nimoy.ast_tools.method_blocks.ComparisonExpressionTransformer')
    def test_that_function_was_added(self, comparison_expression_transformer):
        module_definition = """from nimoy.specification import Specification
class JimbobSpec(Specification):
    def test_it(self):
        with setup:
            pass

        with when:
            pass

        with then:
            pass

        with expect:
            pass

        with where:
            pass
        """
        node = ast.parse(module_definition, mode='exec')

        spec_metadata = get_basic_spec_metadata()
        MethodBlockTransformer(spec_metadata, 'test_it').visit(node)

        spec_method_body = node.body[1].body[0].body

        block_types = ['setup', 'when', 'then', 'expect', 'where']
        for index, block_type in enumerate(block_types):
            self.assertEqual(spec_method_body[index].items[0].context_expr.func.attr, '_method_block_context')
            self.assertEqual(spec_method_body[index].items[0].context_expr.args[0].s, block_type)

        self.assertEqual(comparison_expression_transformer.call_count, 2)
        self.assertEqual(comparison_expression_transformer.return_value.visit.call_count, 2)
        self.assertEqual(spec_metadata.method_blocks['test_it'], block_types)


def get_basic_spec_metadata():
    spec_metadata = SpecMetadata('spec_name')
    spec_metadata.set_owning_module('JimbobSpec')
    spec_metadata.add_test_method('test_it')
    return spec_metadata
