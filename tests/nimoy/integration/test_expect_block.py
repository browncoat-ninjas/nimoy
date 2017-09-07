import unittest
from nimoy.spec_runner import SpecRunner
from nimoy.runner.exceptions import InvalidMethodBlockException


class TestExpectBlocks(unittest.TestCase):
    def test_successful_given(self):
        spec_contents = """from nimoy.specification import Specification
        
class JimbobSpec(Specification):
    
    def test(self):
        with given:
            a = 3
        with expect:
            a != 4
        """

        result = self.run_spec_contents(spec_contents)
        self.assertTrue(result.wasSuccessful())

    def test_successful_setup(self):
        spec_contents = """from nimoy.specification import Specification
        
class JimbobSpec(Specification):
    
    def test(self):
        with setup:
            a = 3
        with expect:
            a != 4
        """

        result = self.run_spec_contents(spec_contents)
        self.assertTrue(result.wasSuccessful())

    def test_dangling_setup(self):
        spec_contents = """from nimoy.specification import Specification
        
class JimbobSpec(Specification):
    
    def test(self):
        with setup:
            a = 3
        """

        with self.assertRaises(InvalidMethodBlockException):
            self.run_spec_contents(spec_contents)

    def test_dangling_given(self):
        spec_contents = """from nimoy.specification import Specification
        
class JimbobSpec(Specification):
    
    def test(self):
        with given:
            a = 3
        """
        with self.assertRaises(InvalidMethodBlockException):
            self.run_spec_contents(spec_contents)

    def test_successful_when_then(self):
        spec_contents = """from nimoy.specification import Specification
        
class JimbobSpec(Specification):
    
    def test(self):
        with when:
            a = 3
        with then:
            a != 4
        """

        result = self.run_spec_contents(spec_contents)
        self.assertTrue(result.wasSuccessful())

    def test_failing_when_then(self):
        spec_contents = """from nimoy.specification import Specification
        
class JimbobSpec(Specification):
    
    def test(self):
        with when:
            a = 3
        with then:
            a == 4
        """

        result = self.run_spec_contents(spec_contents)
        self.assertFalse(result.wasSuccessful())

    def test_dangling_when(self):
        spec_contents = """from nimoy.specification import Specification
        
class JimbobSpec(Specification):
    
    def test(self):
        with setup:
            a = 3
        with when:
            b = 4
        """

        with self.assertRaises(InvalidMethodBlockException):
            self.run_spec_contents(spec_contents)

    def test_dangling_then(self):
        spec_contents = """from nimoy.specification import Specification
        
class JimbobSpec(Specification):
    
    def test(self):
        with setup:
            a = 3
        with then:
            a == 4
        """

        with self.assertRaises(InvalidMethodBlockException):
            self.run_spec_contents(spec_contents)

    def test_successful_expectation(self):
        spec_contents = """from nimoy.specification import Specification
        
class JimbobSpec(Specification):
    
    def test(self):
        with expect:
            a = 3
            a != 4
        """

        result = self.run_spec_contents(spec_contents)
        self.assertTrue(result.wasSuccessful())

    def test_failing_expectation(self):
        spec_contents = """from nimoy.specification import Specification
        
class JimbobSpec(Specification):
    
    def test(self):
        with expect:
            a = 3
            a == 4
        """

        result = self.run_spec_contents(spec_contents)
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

        result = self.run_spec_contents(spec_contents)
        self.assertTrue(result.wasSuccessful())

    def test_expect_after_where(self):
        spec_contents = """from nimoy.specification import Specification
        
class JimbobSpec(Specification):
    
    def test(self):
        with where:
            pass
        
        with expect:
            2 != 1
        """

        with self.assertRaises(InvalidMethodBlockException):
            self.run_spec_contents(spec_contents)


    def test_double_where(self):
        spec_contents = """from nimoy.specification import Specification
        
class JimbobSpec(Specification):
    
    def test(self):
        with where:
            pass
        
        with where:
            pass
        """

        with self.assertRaises(InvalidMethodBlockException):
            self.run_spec_contents(spec_contents)

    def run_spec_contents(self, spec_contents):
        return SpecRunner._run_on_contents([('/fake/path.py', spec_contents)])
