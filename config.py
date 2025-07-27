import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del archivo .env

# Variables
TOKEN = os.getenv("TOKEN")
PLANES_FILE = 'planes.json'

# Estados de conversación
BORRAR_FECHA, BORRAR_ELEGIR = range(2)

# Lista de usuarios permitidos
USUARIOS_PERMITIDOS = ['mirianconn', 'Mirfraper']
