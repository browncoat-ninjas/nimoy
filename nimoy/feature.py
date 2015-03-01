__author__ = 'luftzug'


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


