from io import StringIO

from nimoy.runner.metadata import RunnerContext
from nimoy.runner.spec_finder import Location
from nimoy.runner.unittest_execution_framework import UnitTestExecutionFramework
from nimoy.spec_runner import SpecRunner


def run_spec_contents(spec_contents):
    str_io = StringIO()
    execution_framework = UnitTestExecutionFramework(stream=str_io)
    return SpecRunner._run_on_contents(RunnerContext(), execution_framework,
                                       [(Location('/fake/path.py'), spec_contents)])
