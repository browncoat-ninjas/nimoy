import ast
from unittest import mock
import _ast
from nimoy.specification import Specification
from nimoy.ast_tools.feature_blocks import FeatureBlockTransformer
from nimoy.ast_tools.feature_blocks import FeatureBlockRuleEnforcer
from nimoy.ast_tools.ast_metadata import SpecMetadata
from nimoy.runner.exceptions import InvalidFeatureBlockException


class FeatureBlockRuleEnforcerSpec(Specification):

    def add_setup_and_given_as_first_blocks(self):
        with setup:
            spec_metadata = get_basic_spec_metadata()
            enforcer = FeatureBlockRuleEnforcer(spec_metadata, 'test_it', {})

        with expect:
            enforcer.enforce_addition_rules('given')
            enforcer.enforce_addition_rules('setup')

    def only_one_given_is_allowed(self):
        with setup:
            spec_metadata = get_basic_spec_metadata()
            spec_metadata.add_feature_block('test_it', 'given')
            enforcer = FeatureBlockRuleEnforcer(spec_metadata, 'test_it', {})

        with when:
            enforcer.enforce_addition_rules(block_to_add)

        with then:
            thrown(InvalidFeatureBlockException)

        with where:
            block_to_add = ['given', 'setup']

    def only_one_setup_is_allowed(self):
        with setup:
            spec_metadata = get_basic_spec_metadata()
            spec_metadata.add_feature_block('test_it', 'setup')
            enforcer = FeatureBlockRuleEnforcer(spec_metadata, 'test_it', {})

        with when:
            enforcer.enforce_addition_rules(block_to_add)

        with then:
            thrown(InvalidFeatureBlockException)

        with where:
            block_to_add = ['given', 'setup']

    def setup_and_given_are_allowed_only_in_the_beginning(self):
        with setup:
            spec_metadata = get_basic_spec_metadata()
            spec_metadata.add_feature_block('test_it', 'expect')
            enforcer = FeatureBlockRuleEnforcer(spec_metadata, 'test_it', {})

        with when:
            enforcer.enforce_addition_rules(block_to_add)

        with then:
            thrown(InvalidFeatureBlockException)

        with where:
            block_to_add = ['given', 'setup']

    def test_setup_and_given_cant_dangle(self):
        with setup:
            spec_metadata = get_basic_spec_metadata()
            spec_metadata.add_feature_block('test_it', dangling_block)
            enforcer = FeatureBlockRuleEnforcer(spec_metadata, 'test_it', {})

        with when:
            enforcer.enforce_tail_end_rules()

        with then:
            thrown(InvalidFeatureBlockException)

        with where:
            dangling_block = ['given', 'setup']

    def then_cant_precede_when(self):
        with setup:
            spec_metadata = get_basic_spec_metadata()
            enforcer = FeatureBlockRuleEnforcer(spec_metadata, 'test_it', {})

        with when:
            enforcer.enforce_addition_rules('then')

        with then:
            thrown(InvalidFeatureBlockException)

    def when_cant_dangle(self):
        with setup:
            spec_metadata = get_basic_spec_metadata()
            spec_metadata.add_feature_block('test_it', 'when')
            enforcer = FeatureBlockRuleEnforcer(spec_metadata, 'test_it', {})

        with when:
            enforcer.enforce_tail_end_rules()

        with then:
            thrown(InvalidFeatureBlockException)

    def when_cant_be_followed_by_expect(self):
        with setup:
            spec_metadata = get_basic_spec_metadata()
            spec_metadata.add_feature_block('test_it', 'when')
            enforcer = FeatureBlockRuleEnforcer(spec_metadata, 'test_it', {})

        with when:
            enforcer.enforce_addition_rules('expect')

        with then:
            thrown(InvalidFeatureBlockException)

    def then_after_when(self):
        with setup:
            spec_metadata = get_basic_spec_metadata()
            spec_metadata.add_feature_block('test_it', 'when')
            enforcer = FeatureBlockRuleEnforcer(spec_metadata, 'test_it', {})

        with expect:
            enforcer.enforce_addition_rules('then')

    def block_cant_succeed_where(self):
        with setup:
            spec_metadata = get_basic_spec_metadata()
            spec_metadata.add_feature_block('test_it', 'where')
            enforcer = FeatureBlockRuleEnforcer(spec_metadata, 'test_it', {})

        with when:
            enforcer.enforce_addition_rules('expect')

        with then:
            thrown(InvalidFeatureBlockException)

    def cant_add_more_than_one_where(self):
        with setup:
            spec_metadata = get_basic_spec_metadata()
            spec_metadata.add_feature_block('test_it', 'where')
            enforcer = FeatureBlockRuleEnforcer(spec_metadata, 'test_it', {})

        with when:
            enforcer.enforce_addition_rules('where')

        with then:
            thrown(InvalidFeatureBlockException)


class FeatureBlockTransformerSpec(Specification):

    @mock.patch('nimoy.ast_tools.feature_blocks.ComparisonExpressionTransformer')
    def feature_was_added(self, comparison_expression_transformer):
        with setup:
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

        with when:
            FeatureBlockTransformer(spec_metadata, 'test_it').visit(node)

        with then:
            spec_feature_body = node.body[1].body[0].body

            block_types = ['setup', 'when', 'then', 'expect', 'where']
            for index, block_type in enumerate(block_types[:-1]):
                spec_feature_body[index].items[0].context_expr.func.attr == '_feature_block_context'
                spec_feature_body[index].items[0].context_expr.args[0].s == block_type

                type(spec_feature_body[4]) == _ast.FunctionDef
                spec_feature_body[4].name == 'test_it_where'

                comparison_expression_transformer.call_count == 2
                comparison_expression_transformer.return_value.visit.call_count == 2
                spec_metadata.feature_blocks['test_it'] == block_types


def get_basic_spec_metadata():
    spec_metadata = SpecMetadata('spec_name')
    spec_metadata.set_owning_module('JimbobSpec')
    spec_metadata.add_feature('test_it')
    return spec_metadata
