import _ast
import ast


class AST:

    @staticmethod
    def str(s):
        return ast.Str(s)

    @staticmethod
    def name_constant(value=None):
        return ast.NameConstant(value=value)

    @staticmethod
    def args(args=None):
        return _ast.arguments(
            args=args,
            posonlyargs=[],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[])

    @staticmethod
    def num(n=None):
        return ast.Num(n=n)
