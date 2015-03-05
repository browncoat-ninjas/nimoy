import unittest
from nimoy.feature import Feature, Then
from nimoy.spec import Specification

__author__ = 'luftzug'


class SpecTesting(unittest.TestCase):

    def a_spec_should_gather_features(self):
        class Spec(Specification):
            def method1(self):
                pass

            @Feature('Feature test')
            def feature1(self):
                return True

        assert hasattr(Spec, 'features')
        assert not hasattr(Spec, 'feature1')
        assert 'Feature test' in Spec.features
        assert callable(Spec.features['Feature test'])
        return_value = Spec.features['Feature test'](Spec())
        assert return_value


class ThenBlockTransforming():

    def exploration_test(self):
        outer_var = ''
        then_manager = Then()
        def method_with_then():
            outer_var = 'outer'
            with then_manager:
                'out' in outer_var
                True
                1 > 2
        method_with_then()
