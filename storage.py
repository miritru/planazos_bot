import json
from config import PLANES_FILE

def cargar_planes():
    try:
        with open(PLANES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def guardar_planes(planes):
    with open(PLANES_FILE, 'w') as f:
        json.dump(planes, f, indent=2)