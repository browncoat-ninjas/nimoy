import sys
import ast
import _ast

IS_3_9 = sys.version_info >= (3, 9)

IS_3_8 = sys.version_info >= (3, 8)
if IS_3_8:
    from .ast_3_8 import AST
else:
    from .ast_3_7 import AST


def ast_str(s):
    return AST.str(s)


def ast_name_constant(value=None):
    return AST.name_constant(value)


def ast_args(args=None):
    return AST.args(args)


def ast_num(n=None):
    return AST.num(n)


def slice_access(value=None):
    if IS_3_9:
        return ast.Constant(value=value)
    return _ast.Index(value=value)
