import json
import os
import time

HISTORIAL_FILE = "historial.json"

def cargar_historial():
    if os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, "r") as f:
            return json.load(f)
    return []

def guardar_historial(historial):
    with open(HISTORIAL_FILE, "w") as f:
        json.dump(historial, f, indent=2)

def limpiar_antiguos(historial, dias):
    if dias <= 0:
        return historial

    limite = time.time() - dias * 86400
    return [h for h in historial if h["time"] > limite]
