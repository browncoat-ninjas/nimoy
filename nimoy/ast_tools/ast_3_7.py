import _ast


class AST:

    @staticmethod
    def str(s):
        return _ast.Str(s)

    @staticmethod
    def name_constant(value=None):
        return _ast.NameConstant(value=value)

    @staticmethod
    def args(args=None):
        return _ast.arguments(
            args=args,
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[])

    @staticmethod
    def num(n=None):
        return _ast.Num(n=n)
