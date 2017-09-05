import unittest
from unittest import mock
from nimoy.runner.spec_reader import SpecReader


class TestSpecReader(unittest.TestCase):
    def test_read(self):
        reader_mock = mock.Mock()
        reader_mock.read.return_value = 'class Jimbob:\n    pass'

        spec_contents = SpecReader(reader_mock).read(['/path/to/spec.py'])
        self.assertEqual(spec_contents[0], ('/path/to/spec.py', 'class Jimbob:\n    pass'))

        reader_mock.read.assert_called_once()
