import ast
import keyword
import operator
import sympy as sp
from decimal import Decimal, getcontext

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}

class SafeEvaluator:
    def __init__(self):
        self.variables = {}

    def eval(self, expr: str):
        if "=" in expr:
            parsed = ast.parse(expr, mode='exec')
            if len(parsed.body) != 1 or not isinstance(parsed.body[0], ast.Assign):
                raise ValueError("Asignación inválida; solo se permite una asignación simple")

            assign = parsed.body[0]
            if len(assign.targets) != 1 or not isinstance(assign.targets[0], ast.Name):
                raise ValueError("Asignación inválida; solo se permite una asignación simple")

            name = assign.targets[0].id
            if not name.isidentifier() or keyword.iskeyword(name):
                raise ValueError("Nombre de variable inválido")

            val = self._eval(assign.value)
            self.variables[name] = val
            return val
        return self._eval(ast.parse(expr, mode='eval').body)

    def _eval(self, node):
        if isinstance(node, ast.BinOp):
            return OPS[type(node.op)](
                self._eval(node.left),
                self._eval(node.right)
            )
        elif isinstance(node, ast.UnaryOp):
            return -self._eval(node.operand)
        elif isinstance(node, ast.Constant):
            return Decimal(str(node.value))
        elif isinstance(node, ast.Name):
            if node.id in self.variables:
                return self.variables[node.id]
            raise ValueError
        else:
            raise ValueError

class CalculatorCore:
    def __init__(self, precision=50, mode="decimal"):
        self.mode = mode
        self.evaluator = SafeEvaluator()
        getcontext().prec = precision

    def calculate(self, expr: str):
        try:
            if self.mode == "decimal":
                return str(self.evaluator.eval(expr).normalize())
            else:
                return str(sp.N(sp.sympify(expr, locals={
                    "sin": sp.sin,
                    "cos": sp.cos,
                    "tan": sp.tan,
                    "log": sp.log,
                    "sqrt": sp.sqrt,
                    "pi": sp.pi,
                    "e": sp.E
                }), getcontext().prec))
        except ZeroDivisionError:
            return "∞"
        except Exception:
            return "Error"
