from unittest.mock import Mock

from nimoy.runner.spec_executor import SpecExecutor
from nimoy.specification import Specification


class SpecificationExecutorSpec(Specification):
    def execution(self):
        with given:
            execution_framework_mock = Mock()

            spec_mock = Mock()

            spec_feature_stub = {}
            module_mock = Mock(return_value=spec_feature_stub)

            spec_mock.owning_module = module_mock
            spec_mock.features = ['spec_feature']

        with when:
            SpecExecutor(execution_framework_mock).execute([spec_mock])

        with then:
            execution_framework_mock.append_test.assert_called_once_with(spec_feature_stub)
            execution_framework_mock.run.assert_called_once()
