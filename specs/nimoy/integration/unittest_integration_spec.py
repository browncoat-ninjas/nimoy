import re

from nimoy.specification import Specification
from specs.nimoy.runner_helper import run_spec_contents


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
            result = run_spec_contents(spec_contents)
        with then:
            result.wasSuccessful() == True
            result_output = result.stream.getvalue()
            result_output @ re.compile('Ran 1 test', re.MULTILINE)
