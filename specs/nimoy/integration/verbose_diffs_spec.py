from nimoy.specification import Specification
from nimoy.spec_runner import SpecRunner


class VerboseDiffsSpec(Specification):
    def string_diffs(self):
        with given:
            spec_contents = """from nimoy.specification import Specification
        
class JimbobSpec(Specification):
    
    def test(self):
        with given:
            a = 'The quick brown fox'
        with expect:
            a == 'The quick frown box'
            """

        with when:
            result = SpecRunner._run_on_contents([('/fake/path.py', spec_contents)])

        with then:
            result.wasSuccessful() == False
            failure_message = result.failures[0][1]
            "\'The quick frown box\'\n     but: was \'The quick brown fox\'" in failure_message
            "- The quick brown fox\n?           ^     ^" in failure_message
            "+ The quick frown box\n?           ^     ^" in failure_message
