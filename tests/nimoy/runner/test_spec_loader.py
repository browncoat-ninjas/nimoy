import unittest
from unittest import mock
from nimoy.runner.spec_loader import SpecLoader


class TestSpecLoader(unittest.TestCase):
    def test_load(self):
        reader_mock = mock.Mock()
        reader_mock.read.return_value = 'class Jimbob:\n    pass'

        ast_chain = mock.Mock()
        metadata = mock.Mock()
        metadata.name = 'Jimbob'
        metadata.key = 'value'
        ast_chain.apply.return_value = [metadata]

        returned_spec_metadata = SpecLoader(reader_mock, ast_chain).load(['/path/to/spec.py'])

        self.assertEqual(returned_spec_metadata[0].name, 'Jimbob')
        self.assertEqual(returned_spec_metadata[0].key, 'value')
        self.assertTrue(returned_spec_metadata[0].module)

        reader_mock.read.assert_called_once_with('/path/to/spec.py')
        ast_chain.apply.assert_called_once()
