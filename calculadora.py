import tkinter as tk
import json
import os
import time
from core import CalculatorCore

CONFIG_FILE = "config.json"
HIST_FILE = "historial.json"

DEFAULT = {
    "decimales": 20,
    "historial_max": 100,
    "auto_borrado_dias": 0,
    "modo_default": "decimal"
}

class Calculadora(tk.Tk):
    def __init__(self):
        super().__init__()

        self.config_data = self._load_config()
        self.hist = self._load_hist()
        self._auto_borrar_historial()

        self.expr = ""

        self.core = CalculatorCore(
            self.config_data["decimales"],
            mode=self.config_data.get("modo_default", "decimal")
        )

        self.title("Calculadora PRO")
        self.geometry("360x550")
        self.configure(bg="#1e1e2e")

        self.display = tk.Entry(self, font=("Courier", 22), justify="right",
                                bg="#181825", fg="#cdd6f4", insertbackground="#cdd6f4")
        self.display.pack(fill="x", padx=10, pady=10)

        self.mode_label = tk.Label(self, text=self.core.mode.upper(),
                                  fg="#89b4fa", bg="#1e1e2e")
        self.mode_label.pack()

        tk.Label(self, text="Ej: sin(pi/2), log(10)",
                 fg="#888", bg="#1e1e2e").pack()

        self._crear_botones()

    def _crear_botones(self):
        grid = [
            "789/",
            "456*",
            "123-",
            "0.=+"
        ]

        frame = tk.Frame(self, bg="#1e1e2e")
        frame.pack()

        for r, row in enumerate(grid):
            for c, ch in enumerate(row):
                tk.Button(frame, text=ch, width=6, height=2,
                          command=lambda x=ch: self._click(x)).grid(row=r, column=c)

        tk.Button(self, text="Modo", command=self._toggle_mode).pack(fill="x")
        tk.Button(self, text="Variables", command=self._mostrar_variables).pack(fill="x")
        tk.Button(self, text="Historial", command=self._mostrar_historial).pack(fill="x")
        tk.Button(self, text="Opciones", command=self._abrir_opciones).pack(fill="x")

    def _click(self, x):
        if x == "=":
            self._calcular()
        else:
            self.expr += x
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expr)

    def _calcular(self):
        expr_original = self.expr
        res = self.core.calculate(self.expr)

        self.expr = res

        self.display.delete(0, tk.END)
        self.display.insert(0, res)

        self.hist.append({
            "expr": expr_original,
            "res": res,
            "time": time.time()
        })

        self.hist = self.hist[-self.config_data["historial_max"]:]
        self._save_hist()

    def _toggle_mode(self):
        if self.core.mode == "decimal":
            self.core.mode = "sympy"
        else:
            self.core.mode = "decimal"

        self.mode_label.config(text=self.core.mode.upper())

    def _mostrar_variables(self):
        win = tk.Toplevel(self)
        win.title("Variables")
        for k, v in self.core.evaluator.variables.items():
            tk.Label(win, text=f"{k} = {v}").pack()

    def _mostrar_historial(self):
        win = tk.Toplevel(self)
        win.title("Historial")

        text = tk.Text(win, height=20, width=40)
        text.pack()

        for h in self.hist:
            text.insert(tk.END, f'{h["expr"]} = {h["res"]}\n')

        text.config(state="disabled")

    def _exportar_historial(self):
        with open("historial.txt", "w") as f:
            for h in self.hist:
                f.write(f'{h["expr"]} = {h["res"]}\n')

    def _borrar_historial(self):
        self.hist = []
        self._save_hist()

    def _auto_borrar_historial(self):
        dias = self.config_data.get("auto_borrado_dias", 0)
        if dias <= 0:
            return

        ahora = time.time()
        limite = dias * 86400

        self.hist = [
            h for h in self.hist
            if ahora - h["time"] <= limite
        ]

        self._save_hist()

    def _abrir_opciones(self):
        win = tk.Toplevel(self)
        win.title("Opciones")

        tk.Label(win, text="Decimales (1-100):").pack()
        dec_entry = tk.Entry(win)
        dec_entry.insert(0, str(self.config_data["decimales"]))
        dec_entry.pack()

        tk.Label(win, text="Auto borrar historial (días, 0=off):").pack()
        dias_entry = tk.Entry(win)
        dias_entry.insert(0, str(self.config_data.get("auto_borrado_dias", 0)))
        dias_entry.pack()

        tk.Label(win, text="Modo por defecto:").pack()
        modo_var = tk.StringVar(value=self.config_data.get("modo_default", "decimal"))

        tk.Radiobutton(win, text="Decimal", variable=modo_var, value="decimal").pack()
        tk.Radiobutton(win, text="SymPy", variable=modo_var, value="sympy").pack()

        tk.Button(win, text="Borrar historial", command=self._borrar_historial).pack(pady=5)
        tk.Button(win, text="Exportar historial", command=self._exportar_historial).pack(pady=5)

        def guardar():
            try:
                dec = min(100, max(1, int(dec_entry.get())))
                dias = max(0, int(dias_entry.get()))

                self.config_data["decimales"] = dec
                self.config_data["auto_borrado_dias"] = dias
                self.config_data["modo_default"] = modo_var.get()

                self.core = CalculatorCore(dec, mode=self.core.mode)

                with open(CONFIG_FILE, "w") as f:
                    json.dump(self.config_data, f)

                win.destroy()
            except:
                pass

        tk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def _load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as f:
                return json.load(f)
        return DEFAULT

    def _load_hist(self):
        if os.path.exists(HIST_FILE):
            with open(HIST_FILE) as f:
                return json.load(f)
        return []

    def _save_hist(self):
        with open(HIST_FILE, "w") as f:
            json.dump(self.hist, f)

if __name__ == "__main__":
    app = Calculadora()
    app.mainloop()
