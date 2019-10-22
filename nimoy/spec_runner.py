import argparse
import os

from nimoy.ast_tools import ast_chain
from nimoy.runner import fs_resource_reader
from nimoy.runner.spec_executor import SpecExecutor
from nimoy.runner.spec_finder import SpecFinder
from nimoy.runner.spec_loader import SpecLoader
from nimoy.runner.spec_reader import SpecReader


class SpecRunner:
    def run(self, execution_framework):
        spec_locations = SpecRunner._find_specs()
        spec_locations_and_contents = SpecRunner._read_specs(spec_locations)
        return SpecRunner._run_on_contents(execution_framework, spec_locations_and_contents)

    @staticmethod
    def _run_on_contents(execution_framework, spec_locations_and_contents):
        specs = SpecRunner._load_specs(spec_locations_and_contents)
        return SpecRunner._execute_specs(execution_framework, specs)

    @staticmethod
    def _find_specs():
        parser = argparse.ArgumentParser(prog='nimoy', description='Run a suite of Nimoy specs.')
        parser.add_argument('specs', metavar='S', type=str, nargs='*',
                            help="""A path to a spec file to execute or a directory to scan for spec files.
                            When naming a file it is possible to select which spec or feature to run. some_spec.py[::SpecName[::feature_name]]
                            """)
        args = parser.parse_args()
        suggested_locations = args.specs
        return SpecFinder(os.getcwd()).find(suggested_locations)

    @staticmethod
    def _read_specs(spec_locations):
        return SpecReader(fs_resource_reader).read(spec_locations)

    @staticmethod
    def _load_specs(spec_locations_and_contents):
        return SpecLoader(ast_chain).load(spec_locations_and_contents)

    @staticmethod
    def _execute_specs(execution_framework, specs):
        return SpecExecutor(execution_framework).execute(specs)
