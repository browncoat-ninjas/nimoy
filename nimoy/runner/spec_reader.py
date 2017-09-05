class SpecReader:
    def __init__(self, resource_reader) -> None:
        super().__init__()
        self.resource_reader = resource_reader

    def read(self, spec_locations):
        spec_contents = []

        for spec_file_location in spec_locations:
            text = self.resource_reader.read(spec_file_location)
            spec_contents.append((spec_file_location, text))

        return spec_contents
