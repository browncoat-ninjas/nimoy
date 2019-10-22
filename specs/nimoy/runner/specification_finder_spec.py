import os
import tempfile

from nimoy.runner.spec_finder import Location
from nimoy.runner.spec_finder import SpecFinder
from nimoy.specification import Specification

temp_spec = tempfile.NamedTemporaryFile(suffix='_spec.py')


class SpecificationFinderSpec(Specification):

    def implicit_location(self):
        with when:
            spec_locations = SpecFinder(os.path.dirname(temp_spec.name)).find([])

        with then:
            len(spec_locations) == 1
            spec_locations[0].spec_path @ temp_spec.name

    def explicit_spec_path(self):
        with when:
            spec_locations = SpecFinder('/some/working/dir').find([temp_spec.name])
        with then:
            len(spec_locations) == 1
            spec_locations[0].spec_path @ temp_spec.name

    def explicit_spec_directory(self):
        with when:
            spec_locations = SpecFinder('/some/working/dir').find([os.path.dirname(temp_spec.name)])
        with then:
            len(spec_locations) == 1
            spec_locations[0].spec_path @ temp_spec.name

    def relative_spec_path(self):
        with when:
            spec_locations = SpecFinder('/some/working/dir').find(['jim_spec.py'])
        with then:
            len(spec_locations) == 1
            spec_locations[0].spec_path @ '/some/working/dir/jim_spec.py'

    def full_path(self):
        with when:
            spec_locations = SpecFinder('/some/working/dir').find(['jim_spec.py::SpecName::feature_name'])
        with then:
            len(spec_locations) == 1
            spec_locations[0].spec_path @ '/some/working/dir/jim_spec.py'
            spec_locations[0].spec_name == 'SpecName'
            spec_locations[0].feature_name == 'feature_name'


class SpecificationLocationSpec(Specification):

    def spec_path(self):
        with when:
            location = Location('some_spec.py')

        with then:
            location.spec_path == 'some_spec.py'
            hasattr(location, 'spec_name') == False
            hasattr(location, 'feature_name') == False

    def spec_path_and_name(self):
        with when:
            location = Location('some_spec.py::SpecName')

        with then:
            location.spec_path == 'some_spec.py'
            location.spec_name == 'SpecName'
            hasattr(location, 'feature_name') == False

    def spec_path_and_feature_name(self):
        with when:
            location = Location('some_spec.py::feature_name')

        with then:
            location.spec_path == 'some_spec.py'
            hasattr(location, 'spec_name') == False
            location.feature_name == 'feature_name'

    def spec_path_and_spec_name_and_feature_name(self):
        with when:
            location = Location('some_spec.py::SpecName::feature_name')

        with then:
            location.spec_path == 'some_spec.py'
            location.spec_name == 'SpecName'
            location.feature_name == 'feature_name'
