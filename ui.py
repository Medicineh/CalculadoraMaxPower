import tkinter as tk
import time
from core import evaluar, normalizar_expr
from historial import guardar_historial
from config import guardar_config

class CalculadoraUI:
    def __init__(self, root, config, historial):
        self.root = root
        self.config = config
        self.historial = historial
        self.expr = ""

        self._build()

    def _build(self):
        self.display = tk.Entry(self.root, font=("Courier", 18), justify="right")
        self.display.pack(fill="x", padx=10, pady=10)

        botones = [
            "789/",
            "456*",
            "123-",
            "0.=+"
        ]

        for fila in botones:
            f = tk.Frame(self.root)
            f.pack(expand=True, fill="both")
            for c in fila:
                tk.Button(f, text=c, command=lambda x=c: self.click(x)).pack(side="left", expand=True, fill="both")

        tk.Button(self.root, text="Historial", command=self.ver_historial).pack(fill="x")
        tk.Button(self.root, text="Ajustes", command=self.ajustes).pack(fill="x")

    def click(self, c):
        if c == "=":
            self.calcular()
        elif c == "C":
            self.expr = ""
        else:
            self.expr += c

        self.display.delete(0, tk.END)
        self.display.insert(0, self.expr)

    def calcular(self):
        try:
            expr = normalizar_expr(self.expr, self.config["modo_espacios"])
            res = evaluar(expr, self.config["decimales"])

            self.historial.append({
                "exp": self.expr,
                "res": res,
                "time": time.time()
            })

            guardar_historial(self.historial)
            self.expr = res

        except ZeroDivisionError:
            self.expr = "∞"
        except Exception:
            self.expr = "Error"

        self.display.delete(0, tk.END)
        self.display.insert(0, self.expr)

    def ver_historial(self):
        win = tk.Toplevel(self.root)
        for h in reversed(self.historial):
            tk.Label(win, text=f"{h['exp']} = {h['res']}").pack()

    def ajustes(self):
        win = tk.Toplevel(self.root)

        tk.Label(win, text="Decimales").pack()
        dec = tk.Scale(win, from_=0, to=100, orient="horizontal")
        dec.set(self.config["decimales"])
        dec.pack()

        def guardar():
            self.config["decimales"] = dec.get()
            guardar_config(self.config)
            win.destroy()

        tk.Button(win, text="Guardar", command=guardar).pack()
