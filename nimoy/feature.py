from pprint import pprint
from nimoy import helpers

__author__ = 'luftzug'
import inspect
import ast


class Expectations():
    """
    This manager actually transforms the code in it's 'with' block so that every line is executed separately and
    evaluated into a boolean value. At the end of the block False values treated as failed asserts and fail the test
    """

    def __enter__(self):
        print('Starting then block')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Leaving then block')


class Stimulus():
    pass


class Setup():
    pass


class Where():
    pass


def _transform_function(function):
    print('Transforming function %s' % function)
    source = inspect.getsource(function)
    print('Source function:\n%s' % (source,))
    return ast.parse('Specification', source)


class Feature():
    """
    Decorate a function or method as a feature
    """
    def __init__(self, desc):
        self.desc = desc
        self._original_function = None

    def __call__(self, fn):
        self._original_function = fn
        def feature_method(*args, **kwargs):
            print("Do something before feature")
            transformed = _transform_function(fn)
            transformed(*args, **kwargs)
            print("Do something after feature")
        feature_method.__name__ = self.desc
        feature_method.is_feature = True
        return feature_method
