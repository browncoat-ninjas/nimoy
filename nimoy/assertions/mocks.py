class MockAssertions:
    def assert_mock(self, number_of_invocations, mock, method, *args):
        if not hasattr(mock, method) and number_of_invocations > 0:
            raise AssertionError(method + " was never invoked") from None

        mocked_method = getattr(mock, method)
        if (number_of_invocations >= 0) and (mocked_method.call_count != number_of_invocations):
            raise AssertionError(
                method + " was to be invoked " + str(number_of_invocations) + " times but was invoked " + str(
                    mocked_method.call_count)) from None

        for value, expected_value in zip(mocked_method.call_args[0], args):
            if expected_value != '__nimoy_argument_wildcard' and expected_value != value:
                raise AssertionError(
                    method + " expected argument " + str(expected_value) + " but was invoked with " + str(
                        value)) from None
