from io import StringIO

from nimoy.runner.unittest_execution_framework import UnitTestExecutionFramework
from nimoy.spec_runner import SpecRunner


def run_spec_contents(spec_contents):
    str_io = StringIO()
    execution_framework = UnitTestExecutionFramework(stream=str_io)
    return SpecRunner._run_on_contents(execution_framework, [('/fake/path.py', spec_contents)])
