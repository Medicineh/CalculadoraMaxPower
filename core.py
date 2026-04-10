import ast
from decimal import Decimal, getcontext

OPERADORES = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.Pow: lambda a, b: a ** b,
}

def normalizar_expr(expr, modo):
    if modo == "ignorar":
        return expr.replace(" ", "")
    if modo == "suma":
        return expr.replace(" ", "+")

    tokens = expr.split()
    nueva = ""
    for t in tokens:
        if nueva and nueva[-1].isdigit() and t.isdigit():
            nueva += t
        else:
            if nueva:
                nueva += " "
            nueva += t
    return nueva.replace(" ", "")

def evaluar(expr, decimales):
    getcontext().prec = max(100, decimales + 5)

    def _eval(node):
        if isinstance(node, ast.BinOp):
            return OPERADORES[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.Num):
            return Decimal(str(node.n))
        elif isinstance(node, ast.Expression):
            return _eval(node.body)
        else:
            raise ValueError("Expresión no válida")

    tree = ast.parse(expr, mode="eval")
    resultado = _eval(tree)

    return format(resultado, f".{decimales}f")
