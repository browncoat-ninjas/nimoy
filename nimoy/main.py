import sys

from nimoy.runner.unittest_execution_framework import UnitTestExecutionFramework
from nimoy.spec_runner import SpecRunner


def main():
    execution_framework = UnitTestExecutionFramework()
    result = SpecRunner().run(execution_framework)
    sys.exit(not result.wasSuccessful())


if __name__ == '__main__':
    main()
