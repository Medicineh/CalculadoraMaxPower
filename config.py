import json
import os

CONFIG_FILE = "calc_config.json"

DEFAULT_CONFIG = {
    "decimales": 10,
    "historial_max": 50,
    "auto_borrar_dias": 0,
    "modo_espacios": "inteligente"
}

def cargar_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    return DEFAULT_CONFIG.copy()

def guardar_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
