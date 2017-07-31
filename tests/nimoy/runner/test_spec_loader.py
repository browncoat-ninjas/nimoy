import unittest
from unittest import mock
from nimoy.runner.spec_loader import SpecLoader


class TestSpecLoader(unittest.TestCase):
    def test_load(self):
        reader_mock = mock.Mock()
        reader_mock.read.return_value = 'print(\'bob\')'

        ast_chain = mock.Mock()
        ast_chain.apply.return_value = {'class_name': 'some_class', 'key': 'value'}

        spec_metadata = SpecLoader(reader_mock, ast_chain).load(['/path/to/spec.py'])

        self.assertEqual(spec_metadata.get('some_class').get('key'), 'value')

        reader_mock.read.assert_called_once_with('/path/to/spec.py')
        ast_chain.apply.assert_called_once()
