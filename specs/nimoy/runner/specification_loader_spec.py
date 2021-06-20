from unittest import mock

from nimoy.ast_tools.ast_metadata import SpecMetadata
from nimoy.runner.metadata import RunnerContext
from nimoy.runner.spec_finder import Location
from nimoy.runner.spec_loader import SpecLoader
from nimoy.specification import Specification


class SpecificationLoaderSpec(Specification):
    def load(self):
        with given:
            ast_chain = mock.Mock()

            metadata = SpecMetadata('Jimbob')
            ast_chain.apply.return_value = [metadata]

        with when:
            returned_spec_metadata = SpecLoader(RunnerContext(), ast_chain).load(
                [(Location('/path/to/spec.py'), 'class Jimbob:\n    pass')])

        with then:
            spec_metadata = next(returned_spec_metadata)
            spec_metadata.name == 'Jimbob'
            spec_metadata.owning_module != None

            ast_chain.apply.assert_called_once()
