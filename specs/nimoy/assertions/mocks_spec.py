from nimoy.assertions.mocks import MockAssertions
from nimoy.specification import Specification
from unittest import mock


class MockAssertionsSpec(Specification):

    def mock_was_never_called(self):
        with setup:
            the_mock = mock.Mock()
        with when:
            MockAssertions().assert_mock(4, the_mock, 'non_existing')
        with then:
            thrown(AssertionError)

    def mock_was_never_called_and_zero_interactions_expected(self):
        with setup:
            the_mock = mock.Mock()
        with expect:
            MockAssertions().assert_mock(0, the_mock, 'not_called')

    def mock_not_called_enough(self):
        with setup:
            the_mock = mock.Mock()
            the_mock.some_method()
        with when:
            MockAssertions().assert_mock(2, the_mock, 'some_method')
        with then:
            thrown(AssertionError)

    def mock_argument_mismatch(self):
        with setup:
            the_mock = mock.Mock()
            the_mock.some_method('a')
        with when:
            MockAssertions().assert_mock(1, the_mock, 'some_method', 'b')
        with then:
            thrown(AssertionError)
