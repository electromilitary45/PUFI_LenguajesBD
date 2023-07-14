import cx_Oracle

def establecer_conexion():
    try:
        connection = cx_Oracle.connect(
            user='DBA_AURA',
            password='ADMIN1',
            dsn='localhost:1521/orcl',
            encoding='UTF-8'
        )
        return connection
    except cx_Oracle.Error as error:
        print('Error al establecer la conexión: ',error)
        return None

# ------------------ MUDLO ROLES ------------------ #
def InsertRol():
    # ---- Nombre rol
    nombreRol = ""
    while nombreRol == "":
        nombreRol = input("Ingrese el nombre del rol: ")
    
    try:
        # Establecer la conexión a la base de datos
        connection = establecer_conexion()
        if connection is None:
            return print('No se logró establecer la conexión con la base de datos en el proceso de inserción')
        
        ##coneccion 
        cursor = connection.cursor()

        # Habilitar la captura de mensajes de salida
        cursor.callproc("DBMS_OUTPUT.ENABLE")

        # execute de un sp
        cursor.callproc("SP_CrearRol", [nombreRol])

        
        # Recuperar los mensajes de DBMS_OUTPUT
        message = cursor.var(cx_Oracle.STRING)
        status = cursor.var(cx_Oracle.NUMBER)
        cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))
        while status.getvalue() == 0:
            print(message.getvalue())
            cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))

        ## commit
        cursor.execute("commit")
        
    except Exception as ex:
        print(ex)
    finally:
        if connection:
            connection.close()

def vistaRoles():
    idRol=[]
    nombre=[]

    try:
        # Establecer la conexión a la base de datos
        connection = establecer_conexion()
        if connection is None:
            return idRol, nombre

        cursor=connection.cursor()

        cursor.execute("SELECT * FROM InfoRoles")
        results = cursor.fetchall()

        
        for row in results:
            idRol.append(row[0])
            nombre.append(row[1])


    except Exception as ex:
        print('Error al obtener los registros:',ex)

    finally:
        cursor.close()
        connection.close()

    return idRol, nombre

def editar_rol(id_rol, nuevo_nombre):
    # Establecer la conexión a la base de datos
    connection = establecer_conexion()
    if connection is None:
        return id_rol,nuevo_nombre
    try:
        cursor=connection.cursor()

        # Habilitar la salida de DBMS_OUTPUT
        cursor.callproc('DBMS_OUTPUT.ENABLE')
        
        cursor.callproc('SP_EditarRol',[id_rol,nuevo_nombre])

        # Recuperar los mensajes de DBMS_OUTPUT
        message = cursor.var(cx_Oracle.STRING)
        status = cursor.var(cx_Oracle.NUMBER)
        cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))
        while status.getvalue() == 0:
            print(message.getvalue())
            cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))

        connection.commit()

    except cx_Oracle.Error as error:
        print('Error al ejecutar el procedimiento para editar roles: ',error)
    
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()


#PRUEBAS
InsertRol()

##Prueba vista roles
# Llamar a la función y obtener los vectores de resultados
#idRol_result, nombre_result = vistaRoles()

# Imprimir los vectores
#print("ID Rol:", idRol_result)
#print("Nombre:", nombre_result)

def solicitar_id_rol():
    while True:
        id_rol_a_editar = input("\nIngrese el ID del rol que desea editar (o 'q' para salir): ")
        if id_rol_a_editar.lower() == 'q' or id_rol_a_editar.lower() == 'salir':
            return None  # Devolver None para indicar que se desea salir
        elif id_rol_a_editar.isdigit():
            return int(id_rol_a_editar)
        else:
            print("Error: Por favor, ingrese un número válido.")

def menu_editar_roles():
    # Obtener los registros de la vista InfoRoles
    idRol_array, nombre_array = vistaRoles()

    print('\n**********************************************************')
    print('*************** MODULO ROLES - EDITAR ROL ***************')
    print('**********************************************************')

    # Imprimir los registros disponibles
    print("\nRegistros disponibles:\n")
    for i in range(len(idRol_array)):
        print("--ID Rol:", idRol_array[i], "- Nombre:", nombre_array[i])

    # Solicitar al usuario el ID del rol a editar
    id_rol_a_editar = solicitar_id_rol()
    if id_rol_a_editar is None:
        # Salir del programa 
        print("\nSaliendo del programa...")
    else:
        # Continuar con el procesamiento
        print("\nID del rol a editar:", id_rol_a_editar)

    # Verificar si el ID del rol ingresado existe en los registros obtenidos
    if id_rol_a_editar in idRol_array:
        nuevo_nombre = input("\nIngrese el nuevo nombre para el rol: ")
        editar_rol(id_rol_a_editar, nuevo_nombre)



#----------------------------MENUS--------------------------------
def menu_roles():
    print("EN DESARRROLLO")

def menu_usuarios():
    print("EN DESARRROLLO")

def menu_tipoServicios():
    print("EN DESARRROLLO")

def menu_servicios():
    print("EN DESARRROLLO")

def menu_tipoProductos():
    print("EN DESARRROLLO")

def menu_productos():
    print("EN DESARRROLLO")

def MENU_PRINCIPAL():
    op=""
    while op!="0":
        op=input(
            "********** MENU **********\n"
            "1. ROLES\n"
            "2. USUARIOS\n"
            "3. TIPO PRODUCTO\n"
            "4. PRODUCTOS\n"
            "5. TIPO SERVICIO\n"
            "6. SERVICIOS\n"
            "0. SALIR\n"
            "Ingrese una opción:"
        )
        
        if op=="1":
            menu_roles()
        elif op=="2":
            menu_usuarios()
        elif op=="3":
            menu_tipoProductos()
        elif op=="4":
            menu_productos()
        elif op=="5":
            menu_tipoServicios()
        elif op=="6":
            menu_servicios()

#---------------------------MAIN----------------------------------
MENU_PRINCIPAL()
