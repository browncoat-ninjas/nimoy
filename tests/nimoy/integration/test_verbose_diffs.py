from tests.nimoy.integration.base_integration_test import BaseIntegrationTest


class TestVerboseDiffs(BaseIntegrationTest):
    def test_string_diffs(self):
        spec_contents = """from nimoy.specification import Specification
        
class JimbobSpec(Specification):
    
    def test(self):
        with given:
            a = 'The quick brown fox'
        with expect:
            a == 'The quick frown box'
        """

        result = self._run_spec_contents(spec_contents)
        self.assertFalse(result.wasSuccessful())
        failure_message = result.failures[0][1]
        self.assertIn("\'The quick frown box\'\n     but: was \'The quick brown fox\'", failure_message)
        self.assertIn("- The quick brown fox\n?           ^     ^", failure_message)
        self.assertIn("+ The quick frown box\n?           ^     ^", failure_message)
