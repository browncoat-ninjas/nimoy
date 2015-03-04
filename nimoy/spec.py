__author__ = 'luftzug'


class SpecMetaClass(type):
    def __new__(metacls, name, bases, namespace, **kwargs):
        features = {}
        features_original_names = []
        for name, value in namespace.items():
            if callable(value) and hasattr(value, 'is_feature'):
                features_original_names.append(name)
                features[value.__name__] = value
                print("Moving feature '" + value.__name__ + "' to features")
        namespace['features'] = features
        for name in features_original_names:
            del namespace[name]
        result_class = type.__new__(metacls, name, bases, namespace)
        return result_class


class Specification(object, metaclass=SpecMetaClass):
    pass
