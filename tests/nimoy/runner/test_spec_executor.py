import unittest
from unittest import mock

from nimoy.runner.spec_executor import SpecExecutor


class TestSpecExecutor(unittest.TestCase):
    def test_execution(self):
        execution_framework_mock = mock.Mock()

        suit = {}
        execution_framework_mock.create_suite.return_value = suit

        spec_mock = mock.Mock()

        spec_feature_stub = {}
        module_mock = mock.Mock(return_value=spec_feature_stub)

        spec_mock.owning_module = module_mock
        spec_mock.features = ['spec_feature']

        SpecExecutor(execution_framework_mock).execute([spec_mock])
        execution_framework_mock.create_suite.assert_called_once()
        execution_framework_mock.append_test.assert_called_once_with(suit, spec_feature_stub)
        execution_framework_mock.run.assert_called_once_with(suit)
