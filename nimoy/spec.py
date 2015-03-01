__author__ = 'luftzug'


class SpecMetaClass(type):
    def __init__(cls, class_name, bases, namespace):
        features = {}
        for name, value in namespace.items():
            if callable(value) and hasattr(value, 'is_feature'):
                features[value.__name__] = value
                del namespace[name]
                print("Moving feature '" + value.__name__ + "' to features")
        super(SpecMetaClass, cls).__init__(class_name, bases, namespace)


class Specification(object, metaclass=SpecMetaClass):
    pass
