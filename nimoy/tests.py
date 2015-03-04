import unittest
from nimoy.feature import Feature
from nimoy.spec import Specification

__author__ = 'luftzug'


class SpecTesting(unittest.TestCase):

    def a_spec_should_gather_features(self):
        class Spec(Specification):
            def method1(self):
                pass

            @Feature('Feature test')
            def feature1(self):
                pass

        assert hasattr(Spec, 'features')
        assert not hasattr(Spec, 'feature1')
        assert 'Feature test' in Spec.features
        assert callable(Spec.features['Feature test'])
