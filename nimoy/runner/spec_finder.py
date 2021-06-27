import fnmatch
import os


class SpecFinder:
    def __init__(self, working_directory) -> None:
        super().__init__()
        self.working_directory = working_directory
        self.spec_locations = []

    def find(self, suggested_locations):
        if not suggested_locations:
            suggested_locations.append(self.working_directory)
        self._find_specs_in_suggested_locations(suggested_locations)

        return self.spec_locations

    def _find_specs_in_suggested_locations(self, suggested_locations):

        for suggested_location in suggested_locations:
            normalized_suggested_location = self._normalize_suggested_location(suggested_location)

            if 'spec.py' in normalized_suggested_location:
                self.spec_locations.append(Location(normalized_suggested_location))
            else:
                self._find_specs_in_directory(normalized_suggested_location)

    def _normalize_suggested_location(self, suggested_location):

        if os.path.isabs(suggested_location):
            return suggested_location
        return os.path.join(self.working_directory, suggested_location)

    def _find_specs_in_directory(self, directory):
        for root, _, file_names in os.walk(directory):
            for filename in fnmatch.filter(file_names, '*spec.py'):
                self.spec_locations.append(Location(os.path.join(root, filename)))


class Location:
    def __init__(self, suggested_location):

        # Format may be:
        # - some_spec.py
        # - some_spec.py::SpecName
        # - some_spec.py::feature_name
        # - some_spec.py::SpecName::feature_name
        split_suggested_location = suggested_location.split("::")

        # some_spec.py
        if len(split_suggested_location) == 1:
            self.spec_path = split_suggested_location[0]

        # some_spec.py::SpecName or some_spec.py::feature_name
        if len(split_suggested_location) == 2:
            self.spec_path = split_suggested_location[0]

            # some_spec.py::SpecName
            if split_suggested_location[1][0].isupper():
                self.spec_name = split_suggested_location[1]

            # some_spec.py::feature_name
            else:
                self.feature_name = split_suggested_location[1]

        # some_spec.py::SpecName::feature_name
        if len(split_suggested_location) == 3:
            self.spec_path = split_suggested_location[0]
            self.spec_name = split_suggested_location[1]
            self.feature_name = split_suggested_location[2]
