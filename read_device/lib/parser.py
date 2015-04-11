import ast
import operator

# http://stackoverflow.com/a/9558001
class Parser:
	operators = {
		ast.Mult: operator.mul,
		ast.Div:  operator.truediv,
		ast.USub: operator.neg,
		'int':    int,
	}

	def eval(self, expr, ctx={}):
		self.variables = ctx
		return self._eval(ast.parse(expr, mode='eval').body)

	def _eval(self, node):
		try:
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
				return self.operators[node.func.id](self._eval(*node.args))
			# Varaible: <variable>
			elif isinstance(node, ast.Name):
				return self.variables.get(node.id)
			else:
				raise TypeError(node)

		except:
			# TODO: Handle this better
			e = Exception("TODO: There was a problem interpreting the results from the device")
			e.__cause__ = None
