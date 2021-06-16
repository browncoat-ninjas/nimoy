from typing import Dict
from unittest import TestCase
import copy
from nimoy.context.feature_block_context import FeatureBlock
from nimoy.compare.internal import Compare
from nimoy.assertions.mocks import MockAssertions
from nimoy.assertions.exceptions import ExceptionAssertions
from nimoy.assertions.power import PowerAssertions


class DataDrivenSpecification(type):
    @staticmethod
    def data_driver(test_method):
        def helper(*args, **kwargs):
            if not hasattr(args[0], test_method.__name__ + '_where'):
                return test_method(*args, **kwargs)

            where_method = getattr(args[0], test_method.__name__ + '_where')
            data_to_inject = DataDrivenSpecification._get_data_to_inject(where_method)
            for data_set in data_to_inject:
                copy_of_kwargs = copy.copy(kwargs)
                copy_of_kwargs.update(data_set)
                test_method(*args, **copy_of_kwargs)

        helper.__name__ = test_method.__name__

        return helper

    @staticmethod
    def _get_data_to_inject(where_function):
        data_to_inject = {}
        where_function(data_to_inject)

        iterable_data_to_inject = []
        for key in data_to_inject:
            values = data_to_inject[key]
            for index, value in enumerate(values):
                if (index + 1) > len(iterable_data_to_inject):
                    iterable_data_to_inject.append({})
                iterable_data_to_inject[index][key] = value
        return iterable_data_to_inject

    def __new__(mcs, clsname, superclasses, attributedict):
        for attribute in attributedict:
            DataDrivenSpecification.wrap_data_driven_method(attributedict, attribute)

        return type.__new__(mcs, clsname, superclasses, attributedict)

    @staticmethod
    def wrap_data_driven_method(attributedict, attribute):
        if callable(attribute) or attribute.startswith("_"):
            return

        attributedict[attribute] = DataDrivenSpecification.data_driver(attributedict[attribute])


class Specification(TestCase, metaclass=DataDrivenSpecification):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.thrown_exceptions = []

    def _feature_block_context(self, block_name):
        return FeatureBlock(block_name, self.thrown_exceptions)

    def _compare(self, left, right, comparison_type_name):
        Compare().compare(left, right, comparison_type_name)

    def _power_assert(self, expression: Dict):
        PowerAssertions().assert_and_raise(expression)

    def _assert_mock(self, number_of_invocations, mock, method, *args):
        MockAssertions().assert_mock(number_of_invocations, mock, method, *args)

    def _exception_thrown(self, expected_exception_type):
        return ExceptionAssertions().assert_exception(self.thrown_exceptions, expected_exception_type)
