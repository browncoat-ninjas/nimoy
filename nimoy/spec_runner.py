import argparse
import os
from nimoy.runner.spec_finder import SpecFinder
from nimoy.runner.spec_loader import SpecLoader
from nimoy.runner.spec_executor import SpecExecutor
from nimoy.runner import unittest_execution_framework
from nimoy.runner import fs_resource_reader
from nimoy.ast_tools import ast_chain


class SpecRunner:
    def run(self):
        spec_locations = self._find_specs()
        specs = self._load_specs(spec_locations)
        self._execute_specs(specs)

    def _find_specs(self):
        parser = argparse.ArgumentParser(description='Run a suite of Nimoy specs.')
        parser.add_argument('specs', metavar='S', type=str, nargs='*',
                            help='A path to a spec file to execute or a directory to scan for spec files')
        args = parser.parse_args()
        suggested_locations = args.specs
        return SpecFinder(os.getcwd()).find(suggested_locations)

    def _load_specs(self, spec_locations):
        return SpecLoader(fs_resource_reader, ast_chain).load(spec_locations)

    def _execute_specs(self, specs):
        SpecExecutor(unittest_execution_framework).execute(specs)


if __name__ == '__main__':
    SpecRunner().run()
