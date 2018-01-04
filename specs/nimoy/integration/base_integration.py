from nimoy.specification import Specification
from nimoy.spec_runner import SpecRunner


class BaseIntegration(Specification):

    def _run_spec_contents(self, spec_contents):
        return SpecRunner._run_on_contents([('/fake/path.py', spec_contents)])
