import unittest
from unittest import mock
from nimoy.runner.spec_loader import SpecLoader
from nimoy.ast_tools.ast_metadata import SpecMetadata


class TestSpecLoader(unittest.TestCase):
    def test_load(self):
        reader_mock = mock.Mock()
        reader_mock.read.return_value = 'class Jimbob:\n    pass'

        ast_chain = mock.Mock()

        metadata = SpecMetadata('Jimbob')
        ast_chain.apply.return_value = [metadata]

        returned_spec_metadata = SpecLoader(reader_mock, ast_chain).load(['/path/to/spec.py'])

        self.assertEqual(returned_spec_metadata[0].name, 'Jimbob')
        self.assertTrue(returned_spec_metadata[0].owning_module)

        reader_mock.read.assert_called_once_with('/path/to/spec.py')
        ast_chain.apply.assert_called_once()
