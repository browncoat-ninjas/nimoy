from unittest import TestCase
import types
import copy
from nimoy.context.feature_block_context import FeatureBlock
from nimoy.compare.internal import Compare


class DataDrivenSpecification(type):
    @staticmethod
    def data_driver(test_method, where_function):
        def helper(*args, **kwargs):
            data_to_inject = DataDrivenSpecification._get_data_to_inject(where_function)
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

    def __new__(cls, clsname, superclasses, attributedict):
        for attribute in attributedict:
            DataDrivenSpecification.wrap_data_driven_method(attributedict, attribute)

        return type.__new__(cls, clsname, superclasses, attributedict)

    @staticmethod
    def wrap_data_driven_method(attributedict, attribute):
        if callable(attribute) or attribute.startswith("_"):
            return

        if not hasattr(attributedict[attribute], '__code__'):
            return

        method_expressions = attributedict[attribute].__code__.co_consts
        where_name_expression = next(
            expression for expression in method_expressions if
            expression and type(expression) == str and expression.endswith('where'))

        if not where_name_expression:
            return

        # Inspection the contents of __code__ we see that first comes the method impl and one index after it comes the
        # method name. So to find the where method, first find the index of the name and then you know that the impl
        # is located in the location of the name - 1
        index_of_name = method_expressions.index(where_name_expression)
        where = method_expressions[index_of_name - 1]
        where_function = types.FunctionType(where, {})

        attributedict[attribute] = DataDrivenSpecification.data_driver(attributedict[attribute], where_function)


class Specification(TestCase, metaclass=DataDrivenSpecification):
    def _feature_block_context(self, block_name):
        return FeatureBlock(block_name)

    def _compare(self, left, right, comparison_type_name):
        Compare().compare(left, right, comparison_type_name)
