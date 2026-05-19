#Librerías a importar
import json
import os

#Base de datos
DB_FILE = 'acme_cont_db.json'
LIMITE_SEMANAL = 300.0

#configuracióin inicial
def cargar_bd():
    """Carga los datos del archivo JSON"""
    if not os.path.exists(DB_FILE):
        return {"usuarios": {}, "boletas": {}}
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def guardar_bd(bd):
    """Guarda los datos en el archivo JSON"""
    with open(DB_FILE, 'w') as f:
        json.dump(bd, f, indent=4)

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

asd
assertda
setas
defas
def
asd