from nimoy.compare.types import Types


class ConstantValue:
    def __init__(self, value):
        self.value = value


class Variable:
    def __init__(self, name: str, value):
        self.name = name
        self.value = value


class PowerAssertions:

    def assert_and_render(self, left, right, op: Types):
        pass
