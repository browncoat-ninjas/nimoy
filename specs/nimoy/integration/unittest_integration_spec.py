from nimoy.spec_runner import SpecRunner
from nimoy.specification import Specification


class MockAssertionsSpec(Specification):
    def skipped_spec_is_not_reported(self):
        with given:
            spec_contents = """import unittest
from nimoy.specification import Specification

class JimbobSpec(Specification):
    def test(self):
        with expect:
            1 == 1
    
    @unittest.skip        
    def test2(self):
        with expect:
            1 == 2
"""

        with when:
            result = self._run_spec_contents(spec_contents)
        with then:
            result.wasSuccessful() == True
            len(result.skipped) == 1

    def _run_spec_contents(self, spec_contents):
        return SpecRunner._run_on_contents([('/fake/path.py', spec_contents)])
