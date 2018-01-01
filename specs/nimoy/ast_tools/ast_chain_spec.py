from unittest import mock
from nimoy.specification import Specification
from nimoy.ast_tools import ast_chain


class AstChainSpec(Specification):

    @mock.patch('nimoy.ast_tools.ast_chain.SpecTransformer')
    def apply_chain(self, spec_transformer_mock):
        with given:
            node = {}
        with when:
            spec_metadata = ast_chain.apply(node)
        with then:
            isinstance(spec_metadata, list) == True
            1 * spec_transformer_mock.return_value.visit(node)