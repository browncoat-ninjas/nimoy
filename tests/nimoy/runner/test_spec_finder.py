import os
import tempfile
import unittest

from nimoy.runner.spec_finder import SpecFinder


class TestSpecFinder(unittest.TestCase):
    def setUp(self):
        self.temp_spec = tempfile.NamedTemporaryFile(suffix='_spec.py')

    def test_implicit_location(self):
        spec_locations = SpecFinder(os.path.dirname(self.temp_spec.name)).find([])
        self.assertEqual(len(spec_locations), 1)
        self.assertRegex(spec_locations[0], self.temp_spec.name)

    def test_explicit_spec_path(self):
        spec_locations = SpecFinder('/some/working/dir').find([self.temp_spec.name])
        self.assertEqual(len(spec_locations), 1)
        self.assertRegex(spec_locations[0], self.temp_spec.name)

    def test_explicit_spec_directory(self):
        spec_locations = SpecFinder('/some/working/dir').find([os.path.dirname(self.temp_spec.name)])
        self.assertEqual(len(spec_locations), 1)
        self.assertRegex(spec_locations[0], self.temp_spec.name)

    def test_relative_spec_path(self):
        spec_locations = SpecFinder('/some/working/dir').find(['jim_spec.py'])
        self.assertEqual(len(spec_locations), 1)
        self.assertRegex(spec_locations[0], '/some/working/dir/jim_spec.py')
