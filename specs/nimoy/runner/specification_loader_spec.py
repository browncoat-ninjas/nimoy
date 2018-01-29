from unittest import mock
from nimoy.specification import Specification
from nimoy.runner.spec_loader import SpecLoader
from nimoy.ast_tools.ast_metadata import SpecMetadata


class SpecificationLoaderSpec(Specification):
    def load(self):
        with given:
            ast_chain = mock.Mock()

            metadata = SpecMetadata('Jimbob')
            ast_chain.apply.return_value = [metadata]

        with when:
            returned_spec_metadata = SpecLoader(ast_chain).load([('/path/to/spec.py', 'class Jimbob:\n    pass')])

        with then:
            spec_metadata = next(returned_spec_metadata)
            spec_metadata.name == 'Jimbob'
            spec_metadata.owning_module != None

            ast_chain.apply.assert_called_once()
