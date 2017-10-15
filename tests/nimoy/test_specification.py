import unittest
from nimoy.specification import Specification


class FeatureBlockRuleEnforcerTest(unittest.TestCase):
    def test_that_where_function_is_called_before_feature(self):
        class SomeSpec(Specification):
            def test_something(self, where_visited=False):
                self.assertTrue(where_visited)

            def test_something_where(self, data_to_inject):
                assert isinstance(data_to_inject, dict)
                data_to_inject['where_visited'] = [True]

        SomeSpec().test_something()

    def test_that_normal_feature_is_called(self):
        class SomeSpec(Specification):
            def test_something(self, where_visited=False):
                self.assertFalse(where_visited)

        SomeSpec().test_something()
