import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del archivo .env

# Variables
TOKEN = os.getenv("TOKEN")
PLANES_FILE = 'planes.json'

USUARIOS_PERMITIDOS = os.getenv("USUARIOS_PERMITIDOS", "")
USUARIOS_PERMITIDOS = [u.strip() for u in USUARIOS_PERMITIDOS.split(",") if u.strip()]

# Estados de conversación
BORRAR_FECHA, BORRAR_ELEGIR = range(2)

