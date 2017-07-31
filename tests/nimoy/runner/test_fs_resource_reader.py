import tempfile
import unittest

from nimoy.runner import fs_resource_reader


class TestFsResourceReader(unittest.TestCase):
    def test_read_file(self):
        self.temp_file = tempfile.NamedTemporaryFile(suffix='somefile')
        with open(self.temp_file.name, 'w') as f:
            f.write('jimbob')
        text = fs_resource_reader.read(self.temp_file.name)
        self.assertEquals(text, 'jimbob')

    def test_read_non_existing_file(self):
        with self.assertRaises(FileNotFoundError) as context:
            fs_resource_reader.read('/gek')

        self.assertTrue(context.exception)
