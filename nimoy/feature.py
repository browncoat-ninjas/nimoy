__author__ = 'luftzug'
import inspect
import ast


class Then():
    """
    This manager actually transforms the code in it's 'with' block so that every line is executed separately and
    evaluated into a boolean value. At the end of the block False values treated as failed asserts and fail the test
    """
    pass

    def __enter__(self):
        print('Starting then block')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Leaving then block')


class When():
    pass


class Expect():
    pass


class Setup():
    pass


class Where():
    pass


class Feature():
    """
    Decorate a function or method as a feature
    """
    def __init__(self, desc):
        self.desc = desc

    def __call__(self, fn):
        def feature_method(*args, **kwargs):
            print("Do something before feature")
            fn(*args, **kwargs)
            print("Do something after feature")
        feature_method.__name__ = self.desc
        feature_method.is_feature = True
        return feature_method

    def transform_then_blocks(self):
        pass
