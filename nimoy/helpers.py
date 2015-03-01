__author__ = 'luftzug'

import ast


class RecursivePrintVisitor(ast.NodeVisitor):
    def __init__(self, indent=2):
        self._indent = indent
        self._depth = 0

    def generic_visit(self, node):
        print((' ' * (self._depth * self._indent)) + str(node))
        if hasattr(node, 'body'):
            self._depth += 1
            for next_node in node.body:
                self.generic_visit(next_node)
            self._depth -= 1
