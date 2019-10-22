from unittest import mock

from nimoy.runner.spec_finder import Location
from nimoy.runner.spec_reader import SpecReader
from nimoy.specification import Specification


class SpecificationReaderSpec(Specification):
    def read(self):
        with given:
            location = Location('/path/to/spec.py')
            reader_mock = mock.Mock()
            reader_mock.read.return_value = 'class Jimbob:\n    pass'

        with when:
            spec_contents = SpecReader(reader_mock).read([location])

        with then:
            (location, contents) = next(spec_contents)
            location.spec_path == '/path/to/spec.py'
            contents == 'class Jimbob:\n    pass'
            reader_mock.read.assert_called_once()
