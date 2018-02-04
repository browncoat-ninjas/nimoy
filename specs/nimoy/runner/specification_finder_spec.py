import os
import tempfile

from nimoy.specification import Specification
from nimoy.runner.spec_finder import SpecFinder

temp_spec = tempfile.NamedTemporaryFile(suffix='_spec.py')


class SpecificationFinderSpec(Specification):

    def implicit_location(self):
        with when:
            spec_locations = SpecFinder(os.path.dirname(temp_spec.name)).find([])

        with then:
            len(spec_locations) == 1
            spec_locations[0] @ temp_spec.name

    def explicit_spec_path(self):
        with when:
            spec_locations = SpecFinder('/some/working/dir').find([temp_spec.name])
        with then:
            len(spec_locations) == 1
            spec_locations[0] @ temp_spec.name

    def explicit_spec_directory(self):
        with when:
            spec_locations = SpecFinder('/some/working/dir').find([os.path.dirname(temp_spec.name)])
        with then:
            len(spec_locations) == 1
            spec_locations[0] @ temp_spec.name

    def relative_spec_path(self):
        with when:
            spec_locations = SpecFinder('/some/working/dir').find(['jim_spec.py'])
        with then:
            len(spec_locations) == 1
            spec_locations[0] @ '/some/working/dir/jim_spec.py'
