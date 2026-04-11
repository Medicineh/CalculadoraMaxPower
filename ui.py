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
            "C",
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

        tk.Label(win, text="Historial máximo").pack()
        historial_max = tk.Spinbox(win, from_=1, to=100000, increment=1)
        historial_max.delete(0, tk.END)
        historial_max.insert(0, str(max(1, int(self.config.get("historial_max", 50)))))
        historial_max.pack()

        tk.Label(win, text="Auto borrar (días)").pack()
        auto_borrar_dias = tk.Spinbox(win, from_=0, to=36500, increment=1)
        auto_borrar_dias.delete(0, tk.END)
        auto_borrar_dias.insert(0, str(max(0, int(self.config.get("auto_borrar_dias", 0)))))
        auto_borrar_dias.pack()

        tk.Label(win, text="Modo espacios").pack()
        modo_espacios = tk.StringVar(value=self.config.get("modo_espacios", "inteligente"))
        if modo_espacios.get() not in {"ignorar", "suma", "inteligente"}:
            modo_espacios.set("inteligente")
        tk.OptionMenu(win, modo_espacios, "ignorar", "suma", "inteligente").pack(fill="x")

        def _entero_con_minimo(valor, minimo, default):
            try:
                return max(minimo, int(valor))
            except (TypeError, ValueError):
                return default

        def guardar():
            self.config["decimales"] = dec.get()
            self.config["historial_max"] = _entero_con_minimo(historial_max.get(), 1, 50)
            self.config["auto_borrar_dias"] = _entero_con_minimo(auto_borrar_dias.get(), 0, 0)
            self.config["modo_espacios"] = modo_espacios.get() if modo_espacios.get() in {"ignorar", "suma", "inteligente"} else "inteligente"
            guardar_config(self.config)
            win.destroy()

        tk.Button(win, text="Guardar", command=guardar).pack()
