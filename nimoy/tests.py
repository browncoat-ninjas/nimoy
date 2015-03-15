import unittest
import inspect
from pprint import pprint
from nimoy import feature

from nimoy.feature import Feature, Expectations
from nimoy.helpers import RecursivePrintVisitor
from nimoy.spec import Specification

__author__ = 'luftzug'


class SpecTesting(unittest.TestCase):
    def test_a_spec_should_gather_features(self):
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


class CodeTransformationTests(unittest.TestCase):

    def test_exploration(self):
        class SpecForTesting(Specification):
            @Feature('test with expectations')
            def sample_test(self):
                localvar = 'local'
                with Expectations():
                    localvar = 'assignment'
                    'ass' in localvar  # Should assert

        for name, feature in SpecForTesting.features.items():
            print('Running feature %s' % name)
            feature()

