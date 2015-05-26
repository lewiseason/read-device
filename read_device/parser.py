# Copyright 2015 University of Edinburgh
# Licensed under GPLv3 - see README.md for information

import ast
import operator

# http://stackoverflow.com/a/9558001
class Parser:
    operators = {
            ast.Mult: operator.mul,
            ast.Div:  operator.truediv,
            ast.USub: operator.neg,
            'int':    int,
            'round':  round,
    }

    def eval(self, expr, ctx=None):
        self.variables = ctx or {}
        return self._eval(ast.parse(expr, mode='eval').body)

    def _eval(self, node):
        # Number: <number>
        if isinstance(node, ast.Num):
            return node.n
        # Infix: <leftExpr> <operator> <rightExpr>
        elif isinstance(node, ast.BinOp):
            return self.operators[type(node.op)](self._eval(node.left), self._eval(node.right))
        # Unary: <operator> <operand>
        elif isinstance(node, ast.UnaryOp):
            return self.operators[type(node.op)](self._eval(node.operand))
        # Function: <function>(<args>, ...)
        elif isinstance(node, ast.Call):
            function  = self.operators[node.func.id]
            arguments = list(map(self._eval, node.args))
            return function(*arguments)
        # Varaible: <variable>
        elif isinstance(node, ast.Name):
            return self.variables.get(node.id)
        else:
            raise TypeError('Parser tried to evaluate an unknown type of node: %s' % node.__class__.__name__)
