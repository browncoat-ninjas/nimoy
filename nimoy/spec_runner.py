import argparse
import os
from nimoy.runner.spec_finder import SpecFinder
from nimoy.runner.spec_reader import SpecReader
from nimoy.runner.spec_loader import SpecLoader
from nimoy.runner.spec_executor import SpecExecutor
from nimoy.runner import unittest_execution_framework
from nimoy.runner import fs_resource_reader
from nimoy.ast_tools import ast_chain


class SpecRunner:
    def run(self):
        spec_locations = SpecRunner._find_specs()
        spec_contents = SpecRunner._read_specs(spec_locations)
        return SpecRunner._run_on_contents(spec_contents)

    @staticmethod
    def _run_on_contents(spec_contents):
        specs = SpecRunner._load_specs(spec_contents)
        return SpecRunner._execute_specs(specs)

    @staticmethod
    def _find_specs():
        parser = argparse.ArgumentParser(prog='nimoy', description='Run a suite of Nimoy specs.')
        parser.add_argument('specs', metavar='S', type=str, nargs='*',
                            help='A path to a spec file to execute or a directory to scan for spec files')
        args = parser.parse_args()
        suggested_locations = args.specs
        return SpecFinder(os.getcwd()).find(suggested_locations)

    @staticmethod
    def _read_specs(spec_locations):
        return SpecReader(fs_resource_reader).read(spec_locations)

    @staticmethod
    def _load_specs(spec_contents):
        return SpecLoader(ast_chain).load(spec_contents)

    @staticmethod
    def _execute_specs(specs):
        return SpecExecutor(unittest_execution_framework).execute(specs)
