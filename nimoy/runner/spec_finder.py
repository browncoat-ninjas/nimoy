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

            if normalized_suggested_location.endswith('spec.py'):
                self.spec_locations.append(normalized_suggested_location)
            else:
                self._find_specs_in_directory(normalized_suggested_location)

    def _normalize_suggested_location(self, suggested_location):

        if os.path.isabs(suggested_location):
            return suggested_location
        return os.path.join(self.working_directory, suggested_location)

    def _find_specs_in_directory(self, directory):
        for root, dir_names, file_names in os.walk(directory):
            for filename in fnmatch.filter(file_names, '*spec.py'):
                self.spec_locations.append(os.path.join(root, filename))
