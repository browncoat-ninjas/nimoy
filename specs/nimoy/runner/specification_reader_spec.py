from unittest import mock
from nimoy.specification import Specification
from nimoy.runner.spec_reader import SpecReader


class SpecificationReaderSpec(Specification):
    def read(self):
        with given:
            reader_mock = mock.Mock()
            reader_mock.read.return_value = 'class Jimbob:\n    pass'

        with when:
            spec_contents = SpecReader(reader_mock).read(['/path/to/spec.py'])

        with then:
            next(spec_contents) == ('/path/to/spec.py', 'class Jimbob:\n    pass')
            reader_mock.read.assert_called_once()
