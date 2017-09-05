import unittest
from nimoy.spec_runner import SpecRunner


class TestExpectBlocks(unittest.TestCase):
    def test_successful_expectation(self):
        spec_contents = """from nimoy.specification import Specification
        
class JimbobSpec(Specification):
    
    def test(self):
        with expect:
            a = 3
            a != 4
        """

        result = SpecRunner._run_on_contents([('/fake/path.py', spec_contents)])
        self.assertTrue(result.wasSuccessful())

    def test_failing_expectation(self):
        spec_contents = """from nimoy.specification import Specification
        
class JimbobSpec(Specification):
    
    def test(self):
        with expect:
            a = 3
            a == 4
        """

        result = SpecRunner._run_on_contents([('/fake/path.py', spec_contents)])
        self.assertFalse(result.wasSuccessful())

    def test_multiple_expectation(self):
        spec_contents = """from nimoy.specification import Specification
        
class JimbobSpec(Specification):
    
    def test(self):
        with expect:
            a = 3
            a != 4
        
        with expect:
            a = [1, 2, 3]
            2 in a
        """

        result = SpecRunner._run_on_contents([('/fake/path.py', spec_contents)])
        self.assertTrue(result.wasSuccessful())
