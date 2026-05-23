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

#función para registras las boletas
def registrar_boleta(bd, id_usuario):
    limpiar_pantalla()
    print("--- REGISTRAR NUEVA BOLETA ---")
    semana = input("¿A qué semana corresponde? (Ej: 1, 2, 3, 4): ")
    fecha = input("Fecha de visita (DD/MM/AAAA): ")
    hora = input("Hora de visita (HH:MM): ")
    nro_boleta = input("Número de boleta: ")
    motivo = input("Motivo de viaje: ")
    cliente = input("Cliente visitado: ")
    try:
        monto = float(input("Monto gastado (S/): ")) #este valor se usará para la sumatoria de todas las boletas ingresadas
    except ValueError:
        print("Debe ingresar solo números")
        input("Presiona Enter para continuar...")
        return

    nueva_boleta = {
        "semana": semana, "fecha": fecha, "hora": hora, "nro_boleta": nro_boleta,
        "motivo": motivo, "cliente": cliente, "monto": monto,
        "estado": "PENDIENTE", "observacion": ""
    }
    
    bd["boletas"][id_usuario].append(nueva_boleta)
    guardar_bd(bd)
    print("La boleta se ha registrado correctamente.")
    input("Presiona Enter para volver...")

#función para ver las boletas registradas por cada estado
def ver_boletas_por_estado(bd, id_usuario, estado_filtro):
    limpiar_pantalla()
    print(f"--- BOLETAS: {estado_filtro} ---")
    boletas = bd["boletas"].get(id_usuario, [])
    
    if not boletas:
        print("No hay boletas registradas.")
    else:
        semanas = {}
        for b in boletas:
            if estado_filtro == "TODAS" or b["estado"] == estado_filtro:
                sem = b["semana"]
                if sem not in semanas: semanas[sem] = []
                semanas[sem].append(b)
        
        for sem, lista in sorted(semanas.items()):
            print(f"\n>> SEMANA {sem}:")
            for b in lista:
                print(f"  - Fecha: {b['fecha']} | Nro: {b['nro_boleta']} | Monto: S/{b['monto']} | Estado: {b['estado']}")
                if b['observacion']:
                    print(f"    *Obs: {b['observacion']}")
    
    input("\nPresiona Enter para volver...")

### 3ER MODULO: MENU DE CONTABILIDAD
def menu_contabilidad(bd):
    while True:
        limpiar_pantalla()
        print("--- BIENVENIDO AL MENÚ DE CONTABILIDAD ---")
        print("1. Ver lista de usuarios registrados y sus boletas")
        print("2. Gestionar boletas por usuario y semana")
        print("3. Cerrar sesión y volver")
        
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            listar_y_seleccionar_usuarios(bd)
        elif opcion == '2':
            limpiar_pantalla()
            usuario_id = input("Ingresa el ID del usuario a evaluar (Ej: U12345678): ")
            if usuario_id not in bd["boletas"]:
                print("El usuario no existe o no tiene boletas registradas.")
                input("Presiona Enter...")
                continue
            semana = input("Ingresa la semana a evaluar (Ej: 1, 2, 3, 4): ")
            gestionar_boletas_semana(bd, usuario_id, semana)
        elif opcion == '3':
            break

#función para listar los usuarios registrados ysus boletas
def listar_y_seleccionar_usuarios(bd):
    limpiar_pantalla()
    print("--- 1. USUARIOS REGISTRADOS & BOLETAS ---")
    usuarios_lista = list(bd["usuarios"].items())
    
    # Mostrar la lista con números y conteo de boletas
    for i, (uid, info) in enumerate(usuarios_lista, start=1):
        if info['rol'] == 'U':
            boletas = bd["boletas"].get(uid, [])
            total = len(boletas)
            pendientes = sum(1 for b in boletas if b["estado"] == "PENDIENTE")
            estado_txt = f" | Boletas: {total} (Pendientes: {pendientes})"
        else:
            estado_txt = " | (Personal de Contabilidad)"
            
        print(f"[{i}] ID: {uid} | Nombre: {info['nombres']}{estado_txt}")
        
    print("\n[0] Volver atrás")
    seleccion = input("\nSelecciona el número de usuario para ver y evaluar sus boletas: ")

    try:
        idx = int(seleccion)
        if idx == 0:
            return
        if 1 <= idx <= len(usuarios_lista):
            uid_seleccionado = usuarios_lista[idx-1][0]
            if bd["usuarios"][uid_seleccionado]["rol"] == 'C':
                print("No hay boletas para evaluar.")
                input("Presiona Enter...")
            else:
                evaluar_boletas_directo(bd, uid_seleccionado)
        else:
            print("El número está fuera de rangoo.")
            input("Presiona Enter...")
    except ValueError:
        print("Por favor, ingresa un número válido.")
        input("Presiona Enter...")

def evaluar_boletas_directo(bd, usuario_id):
    limpiar_pantalla()
    boletas = bd["boletas"].get(usuario_id, [])
    if not boletas:
        print(f"El usuario no tiene boletas registradas.")
        input("Presiona Enter para volver...")
        return
        
    print(f"--- BOLETAS DE: {bd['usuarios'][usuario_id]['nombres']} ---")
    
    # Mostrar resumen por semanas de este usuario
    semanas = {}
    for b in boletas:
        sem = b["semana"]
        if sem not in semanas: semanas[sem] = []
        semanas[sem].append(b)
        
    for sem, lista in sorted(semanas.items()):
        pendientes = sum(1 for b in lista if b["estado"] == "PENDIENTE")
        print(f">> SEMANA {sem}: {len(lista)} boletas registradas ({pendientes} pendientes de evaluación)")
        
    semana_elegida = input("\nIngresa el número de la SEMANA que deseas evaluar (o 'X' para cancelar): ")
    if semana_elegida.upper() != 'X':
        gestionar_boletas_semana(bd, usuario_id, semana_elegida)

#aquis e realiza la evaluacion de boletas de una semana especifica
def gestionar_boletas_semana(bd, usuario_id, semana):
    """Evalúa una semana específica de un usuario."""
    limpiar_pantalla()
    boletas_semana = [b for b in bd["boletas"][usuario_id] if b["semana"] == semana]
    
    if not boletas_semana:
        print(f"No hay boletas para la semana {semana}.")
        input("Presiona Enter...")
        return

    print(f"--- DETALLE SEMANA {semana} | Usuario: {usuario_id} ---")
    total_gastado = 0.0
    
    for i, b in enumerate(boletas_semana):
        print(f"[{i}] Fecha: {b['fecha']} | Nro: {b['nro_boleta']} | Monto: S/{b['monto']} | Estado: {b['estado']}")
        total_gastado += b['monto']
        
    print("-" * 30)
    print(f"MONTO TOTAL INGRESADO: S/ {total_gastado}")
    if total_gastado > LIMITE_SEMANAL:
        print(f"ADVERTENCIA: Supera el límite de S/{LIMITE_SEMANAL}. (Exceso: S/{total_gastado - LIMITE_SEMANAL})")
    else:
        print("El monto está dentro del límite permitido.")
        
    print("\nAcciones:")
    print("1. Cambiar estado a todas las boletas de la semana (Aprobar/Rechazar/Observar)")
    print("2. Atrás")
    acc = input("Seleccione: ")
    
    if acc == '1':
        nuevo_estado = input("Ingrese nuevo estado (APROBADA / RECHAZADA / OBSERVADA): ").upper()
        observacion = input("Ingrese una observación (opcional) o Enter para omitir: ")
        
        for b in bd["boletas"][usuario_id]:
            if b["semana"] == semana:
                b["estado"] = nuevo_estado
                b["observacion"] = observacion
                
        guardar_bd(bd)
        simular_envio_correo(bd["usuarios"][usuario_id]["correo"], nuevo_estado, total_gastado)
        input("Presiona Enter para continuar...")

def simular_envio_correo(correo, estado, monto):
    print("\n" + "="*40)
    print("ENVÍO DE CORREO...")
    print(f"Para: {correo}")
    print(f"Asunto: Actualización de Reembolso - Estado: {estado}")
    print(f"Mensaje: Su solicitud de reembolso por el monto de S/{monto} ha sido marcada como {estado}.")
    if estado == "APROBADA":
        print("El dinero será depositado en su cuenta en los próximos días.")
    elif estado == "RECHAZADA":
        print("Ha excedido las políticas de viáticos o los comprobantes no son válidos.")
    print("="*40 + "\n")

### 4TO MÓDULO : CAMBIO DE CONTRASEÑA
def cambiar_contrasena(bd):
    limpiar_pantalla()
    print("--- 4. CAMBIAR CONTRASEÑA ---")
    id_usuario = input("Ingrese su ID de Usuario: ")
    correo = input("Ingrese su correo electrónico registrado: ")
    
    if id_usuario in bd["usuarios"] and bd["usuarios"][id_usuario]["correo"] == correo:
        nueva_pass = input("Ingrese su nueva contraseña: ")
        bd["usuarios"][id_usuario]["password"] = nueva_pass
        guardar_bd(bd)
        print("Contraseña actualizada correctamente.")
    else:
        print("Error: Alguno de los datos son incorrectos.")
    input("Presiona Enter para volver al menú...")

###FLUJO PRINCIPAL DEL PROGRAMA
def main():
    bd = cargar_bd()
    
    while True:
        limpiar_pantalla()
        print("====== SISTEMA ACME CONT ======")
        print("1. Crear Usuario")
        print("2. Iniciar Sesión como USUARIO")
        print("3. Iniciar Sesión como CONTABILIDAD")
        print("4. Cambiar Contraseña")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            crear_usuario(bd)
        elif opcion in ['2', '3']:
            limpiar_pantalla()
            print("--- INICIAR SESIÓN ---")
            id_usuario = input("ID de Usuario: ")
            password = input("Contraseña: ")
            
            if id_usuario in bd["usuarios"] and bd["usuarios"][id_usuario]["password"] == password:
                rol = bd["usuarios"][id_usuario]["rol"]
                
                if opcion == '2' and rol == 'U':
                    menu_usuario(bd, id_usuario)
                elif opcion == '3' and rol == 'C':
                    menu_contabilidad(bd)
                else:
                    print("No tiene los privilegios suficiente para acceder a esta sección.")
                    input("Presiona Enter...")
            else:
                print("El usuario o contraseña son incorrectos o no existen")
                input("Presiona Enter...")
                
        elif opcion == '4':
            cambiar_contrasena(bd)
        elif opcion == '5':
            print("Saliendo del sistema...")
            break

if __name__ == "__main__":
    main()