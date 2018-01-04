from nimoy.specification import Specification
from nimoy.spec_runner import SpecRunner
from nimoy.runner.exceptions import InvalidFeatureBlockException


class ExpectBlocks(Specification):
    def successful_given(self):
        with given:
            spec_contents = """from nimoy.specification import Specification

class JimbobSpec(Specification):

    def test(self):
        with given:
            a = 3
        with expect:
            a != 4
            """

        with when:
            result = self._run_spec_contents(spec_contents)

        with then:
            result.wasSuccessful() == True

    def successful_setup(self):
        with given:
            spec_contents = """from nimoy.specification import Specification

class JimbobSpec(Specification):

    def test(self):
        with setup:
            a = 3
        with expect:
            a != 4
            """

        with when:
            result = self._run_spec_contents(spec_contents)

        with then:
            result.wasSuccessful() == True

    def dangling_setup(self):
        with given:
            spec_contents = """from nimoy.specification import Specification

class JimbobSpec(Specification):

    def test(self):
        with setup:
            a = 3
          """

        with when:
            self._run_spec_contents(spec_contents)

        with then:
            thrown(InvalidFeatureBlockException)

    def dangling_given(self):
        with given:
            spec_contents = """from nimoy.specification import Specification

class JimbobSpec(Specification):

    def test(self):
        with given:
            a = 3
            """

        with when:
            self._run_spec_contents(spec_contents)

        with then:
            thrown(InvalidFeatureBlockException)

    def successful_when_then(self):
        with given:
            spec_contents = """from nimoy.specification import Specification

class JimbobSpec(Specification):

    def test(self):
        with when:
            a = 3
        with then:
            a != 4
            """

        with when:
            result = self._run_spec_contents(spec_contents)

        with then:
            result.wasSuccessful() == True

    def failing_when_then(self):
        with given:
            spec_contents = """from nimoy.specification import Specification

class JimbobSpec(Specification):

    def test(self):
        with when:
            a = 3
        with then:
            a == 4
             """

        with when:
            result = self._run_spec_contents(spec_contents)

        with then:
            result.wasSuccessful() == False

    def dangling_when(self):
        with given:
            spec_contents = """from nimoy.specification import Specification

class JimbobSpec(Specification):

    def test(self):
        with setup:
            a = 3
        with when:
            b = 4
            """

        with when:
            self._run_spec_contents(spec_contents)

        with then:
            thrown(InvalidFeatureBlockException)

    def dangling_then(self):
        with given:
            spec_contents = """from nimoy.specification import Specification

class JimbobSpec(Specification):

    def test(self):
        with setup:
            a = 3
        with then:
            a == 4
            """

        with when:
            self._run_spec_contents(spec_contents)

        with then:
            thrown(InvalidFeatureBlockException)

    def successful_expectation(self):
        with given:
            spec_contents = """from nimoy.specification import Specification

class JimbobSpec(Specification):

    def test(self):
        with expect:
            a = 3
            a != 4
        """

        with when:
            result = self._run_spec_contents(spec_contents)

        with then:
            result.wasSuccessful() == True

    def failing_expectation(self):
        with given:
            spec_contents = """from nimoy.specification import Specification

class JimbobSpec(Specification):

    def test(self):
        with expect:
            a = 3
            a == 4
        """

        with when:
            result = self._run_spec_contents(spec_contents)

        with then:
            result.wasSuccessful() == False

    def multiple_expectation(self):
        with given:
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

        with when:
            result = self._run_spec_contents(spec_contents)

        with then:
            result.wasSuccessful() == True

    def expect_after_where(self):
        with given:
            spec_contents = """from nimoy.specification import Specification

class JimbobSpec(Specification):

    def test(self):
        with where:
            pass

        with expect:
            2 != 1
        """

        with when:
            self._run_spec_contents(spec_contents)

        with then:
            thrown(InvalidFeatureBlockException)

    def double_where(self):
        with given:
            spec_contents = """from nimoy.specification import Specification

class JimbobSpec(Specification):

    def test(self):
        with where:
            pass

        with where:
            pass
            """

        with when:
            self._run_spec_contents(spec_contents)

        with then:
            thrown(InvalidFeatureBlockException)

    def expected_exception(self):
        with given:
            spec_contents = """from nimoy.specification import Specification

class JimbobSpec(Specification):

    def test(self):
        with when:
            raise Exception('Whaaaaat')
        with then:
            thrown(Exception)
            """

        with when:
            result = self._run_spec_contents(spec_contents)

        with then:
            result.wasSuccessful() == True

    def expected_derived_exception(self):
        with given:
            spec_contents = """from nimoy.specification import Specification

class JimbobSpec(Specification):

    def test(self):
        with when:
            raise AssertionError('Whaaaaat')
        with then:
            thrown(Exception)
            """

        with when:
            result = self._run_spec_contents(spec_contents)

        with then:
            result.wasSuccessful() == True

    def unexpected_exception(self):
        with given:
            spec_contents = """from nimoy.specification import Specification

class JimbobSpec(Specification):

    def test(self):
        with when:
            raise Exception('Whaaaaat')
        with then:
            pass
            """

        with when:
            result = self._run_spec_contents(spec_contents)

        with then:
            "Exception: Whaaaaat" in result.errors[0][1]
            result.wasSuccessful() == False

    def successful_exception_message_assertion(self):
        with given:
            spec_contents = """from nimoy.specification import Specification

class JimbobSpec(Specification):

    def test(self):
        with when:
            raise Exception('Whaaaaat')
        with then:
            err = thrown(Exception)
            str(err[1]) == 'Whaaaaat'
            """

        with when:
            result = self._run_spec_contents(spec_contents)

        with then:
            result.wasSuccessful() == True

    def failed_exception_type_assertion(self):
        with given:
            spec_contents = """from nimoy.specification import Specification

class JimbobSpec(Specification):

    def test(self):
        with when:
            raise Exception('Whaaaaat')
        with then:
            err = thrown(ArithmeticError)
            """

        with when:
            result = self._run_spec_contents(spec_contents)
            "'ArithmeticError' but found 'Exception'" in result.failures[0][1]

        with then:
            result.wasSuccessful() == False

    def failed_exception_message_assertion(self):
        with given:
            spec_contents = """from nimoy.specification import Specification

class JimbobSpec(Specification):

    def test(self):
        with when:
            raise Exception('Whaaaaat')
        with then:
            err = thrown(Exception)
            str(err[1]) == 'Moo'
            """

        with when:
            result = self._run_spec_contents(spec_contents)

        with then:
            "Expected: 'Moo'" in result.failures[0][1]
            result.wasSuccessful() == False

    def unfulfilled_exception_expectation(self):
        with given:
            spec_contents = """from nimoy.specification import Specification

class JimbobSpec(Specification):

    def test(self):
        with when:
            pass
        with then:
            err = thrown(Exception)
            err.message == 'Whaaaaat'
            """

        with when:
            result = self._run_spec_contents(spec_contents)

        with then:
            "'Exception' to be thrown" in result.failures[0][1]
            result.wasSuccessful() == False

    def _run_spec_contents(self, spec_contents):
        return SpecRunner._run_on_contents([('/fake/path.py', spec_contents)])
