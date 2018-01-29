import tempfile

from nimoy.specification import Specification
from nimoy.runner import fs_resource_reader


class FsResourceReaderSpec(Specification):

    def read_file(self):
        with given:
            temp_file = tempfile.NamedTemporaryFile(suffix='somefile')
            with open(temp_file.name, 'w') as open_temp_file:
                open_temp_file.write('jimbob')

        with when:
            text = fs_resource_reader.read(temp_file.name)
        with then:
            text == 'jimbob'

    def read_non_existing_file(self):
        with when:
            fs_resource_reader.read('/gek')

        with then:
            thrown(FileNotFoundError)
