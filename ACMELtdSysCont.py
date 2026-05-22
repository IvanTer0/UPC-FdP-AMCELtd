#importacion de librerias json para la base de datos 
import json
import os

#establecer nombre de la base de datos y limite semanal para validacion de gastos
DB_FILE = 'acme_cont_db.json'
LIMITE_SEMANAL = 150.0

#funcion para leer la base de datos desde un archivo JSON
def cargar_bd():
    """Carga los datos del archivo JSON.""" #docstring para explicar la funcion
    if not os.path.exists(DB_FILE):
        return {"usuarios": {}, "boletas": {}}
    with open(DB_FILE, 'r') as f:
        return json.load(f)

#función para guardar los datos en la base de datos json
def guardar_bd(bd):
    """Guarda los datos en el archivo JSON."""
    with open(DB_FILE, 'w') as f:
        json.dump(bd, f, indent=4)

#función para limpiar pantalla de la consola luego de ingresar valores (para mejor visibilidad)
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

### 1ER MODULO: CREACIÓN DE USUARIOS
def crear_usuario(bd):
    limpiar_pantalla()
    print("--- 1. CREAR USUARIO ---")
    dni = input("DNI: ")
    
    for user_id in bd["usuarios"]:
        if bd["usuarios"][user_id]["dni"] == dni: #con esto se valida si existe el DNI en la db
            print("El DNI ya se encuentra registrado.")
            input("Presiona Enter para volver...")
            return

    nombres = input("Nombres y apellidos: ")
    correo = input("Correo electrónico: ")
    password = input("Contraseña: ")
    es_conta = input("¿Es personal de contabilidad? (SI/NO): ").strip().upper()

    rol = "C" if es_conta == "SI" else "U" #si es usuario contabilidad, establece la C al inicio para crear el usuario con DNI, de lo contrario U
    id_usuario = f"{rol}{dni}"

    print("\n--- Resumen de Datos Ingresados ---")
    print(f"Usuario creado: {id_usuario}")
    print(f"DNI: {dni}\nNombres: {nombres}\nCorreo: {correo}\nRol: {'Contabilidad' if rol == 'C' else 'Usuario Regular'}")
    
    confirmar = input("\nPresiona 'Enter' para confirmar la creación o escribe 'X' para cancelar: ")
    if confirmar.upper() != 'X':
        bd["usuarios"][id_usuario] = {
            "dni": dni, "nombres": nombres, "correo": correo, 
            "password": password, "rol": rol
        }
        if id_usuario not in bd["boletas"] and rol == "U":
            bd["boletas"][id_usuario] = [] 
        guardar_bd(bd)
        print("El usuario se ha creado correctamente")
    input("Presiona Enter para continuar...")

### 2DO MODULO: MENU DE USUARIO PARA REGISTRAR BOLETAS
def menu_usuario(bd, id_usuario):
    while True:
        limpiar_pantalla()
        print(f"--- BIENVENIDO: {bd['usuarios'][id_usuario]['nombres']} ---")
        print("1. Registrar boletas")
        print("2. Ver boletas registradas")
        print("3. Ver devoluciones pendientes")
        print("4. Ver devoluciones aprobadas")
        print("5. Ver devoluciones rechazadas")
        print("6. Cerrrar sesión y volver")
        
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            registrar_boleta(bd, id_usuario)
        elif opcion == '2':
            ver_boletas_por_estado(bd, id_usuario, "TODAS")
        elif opcion == '3':
            ver_boletas_por_estado(bd, id_usuario, "PENDIENTE")
        elif opcion == '4':
            ver_boletas_por_estado(bd, id_usuario, "APROBADA")
        elif opcion == '5':
            ver_boletas_por_estado(bd, id_usuario, "RECHAZADA")
        elif opcion == '6':
            break
