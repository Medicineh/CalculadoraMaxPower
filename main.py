import tkinter as tk
from config import cargar_config
from historial import cargar_historial, limpiar_antiguos
from ui import CalculadoraUI

def main():
    config = cargar_config()
    historial = cargar_historial()
    historial = limpiar_antiguos(historial, config["auto_borrar_dias"])

    root = tk.Tk()
    root.title("Calculadora MAX POWER") #Ops

    CalculadoraUI(root, config, historial)

    root.mainloop()

if __name__ == "__main__":
    main()
