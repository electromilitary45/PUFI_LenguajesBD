import cx_Oracle
import sys

##RUTA DEREK
#cx_Oracle.init_oracle_client(lib_dir=r"g:\ORACLE\instantclient")

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
def rolesDatos(p_idRol):
    try:
        connection = establecer_conexion()
        cursor = connection.cursor()

        # Habilitar el DBMS_OUTPUT para capturar los mensajes del SP
        cursor.callproc("DBMS_OUTPUT.ENABLE")

        # Ejecutar el SP con el parámetro de entrada
        cursor.callproc("SP_LeerRol", [p_idRol])

        # Recuperar los mensajes de DBMS_OUTPUT del SP
        message = cursor.var(cx_Oracle.STRING)
        status = cursor.var(cx_Oracle.NUMBER)
        cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))
        while status.getvalue() == 0:
            print(message.getvalue())
            cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))

    except Exception as ex:
        print(ex)

    finally:
        if connection:
            connection.close()

def rolesCant():
    try:
        connection = establecer_conexion()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM InfoRoles")
        result = cursor.fetchone()
        role_count = result[0]

    except Exception as ex:
        print(ex)

    finally:
        if connection:
            connection.close()
    return role_count

def InsertRol():
    # ---- Nombre rol
    nombreRol = ""
    while nombreRol == "":
        nombreRol = input("Ingrese el nombre del rol: ")

    try:
        connection = establecer_conexion()
        ##coneccion 
        cursor = connection.cursor()

        ## Habilitar el DBMS_OUTPUT para capturar los mensajes del trigger
        cursor.callproc("DBMS_OUTPUT.ENABLE")

        ## Ejecutar el SP para crear el rol
        cursor.callproc("SP_CrearRol", [nombreRol])

        ## Recuperar el mensaje de salida del SP (y también del trigger)
        message = cursor.var(cx_Oracle.STRING)
        status = cursor.var(cx_Oracle.NUMBER)
        cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))
        while status.getvalue() == 0:
            print(message.getvalue())
            cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))

        ## Commit después de ejecutar el SP 
        connection.commit()

    except Exception as ex:
        print(ex)

    finally:
        if connection:
            connection.close()

def VerRoles():
    try:
        connection = establecer_conexion()
        cursor = connection.cursor()

        ## sentencia de select de rol desde la vista
        cursor.execute("SELECT * FROM InfoRoles")

        results = cursor.fetchall()

        print("Roles disponibles:")
        for row in results:
            print(row)

        return results

    except Exception as ex:
        print(ex)

def EditarRol():
    connection = None
    try:
        # Traer y mostrar los datos de los roles
        roles = VerRoles()

        # Pedir al usuario seleccionar un número de rol para editar o 'Q' para cancelar
        op = input("\nSeleccione el # de rol que desea editar o 'Q' para cancelar: ")

        # Si no cancela la operación
        if op.lower() != "q":
            # Buscar el rol por ID
            idRol = int(op)
            encontrado = False
            for row in roles:
                if idRol == row[0]:
                    encontrado = True
                    nombreRol = row[1]
                    break

            # Si encuentra el rol
            if encontrado:
                print("\nRol seleccionado:", nombreRol)

                # Pedir el nuevo nombre del rol
                nombreNuevoRol = input("Ingrese el nuevo nombre del rol: ")

                # Si no está vacío, aplicar el SP para editar el rol
                if nombreNuevoRol.strip() != "":
                    connection = establecer_conexion()
                    cursor = connection.cursor()

                    # Habilitar el DBMS_OUTPUT para capturar los mensajes del trigger
                    cursor.callproc("DBMS_OUTPUT.ENABLE")

                    # Ejecutar el SP con los parámetros de entrada
                    cursor.callproc("SP_EditarRol", [idRol, nombreNuevoRol])

                    # Recuperar los mensajes de DBMS_OUTPUT (también del trigger)
                    message = cursor.var(cx_Oracle.STRING)
                    status = cursor.var(cx_Oracle.NUMBER)
                    cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))
                    while status.getvalue() == 0:
                        print(message.getvalue())
                        cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))

                    # Realizar el commit si no hay mensajes de error
                    connection.commit()

            # Si no encuentra el rol
            else:
                print("ID de rol incorrecto")

        # Si cancela la operación
        else:
            print("Operación cancelada")
            menu_roles()

    except Exception as ex:
        print(ex)

    finally:
        if connection is not None:
            connection.close()

def EliminarRol():
    try:
        # Traer y mostrar los datos de los roles
        roles = VerRoles()

        # Pedir al usuario seleccionar un número de rol para eliminar o 'Q' para cancelar
        op = input("\nSeleccione el # de rol que desea eliminar o 'Q' para cancelar: ")

        # Si no cancela la operación
        if op.lower() != "q":
            # Buscar el rol por ID
            idRol = int(op)
            encontrado = False
            for row in roles:
                if idRol == row[0]:
                    encontrado = True
                    nombreRol = row[1]
                    break

            # Si encuentra el rol
            if encontrado:
                print("\nRol seleccionado:", nombreRol)

                # Llama al SP para eliminar el rol
                connection = establecer_conexion()
                cursor = connection.cursor()

                # Habilitar el DBMS_OUTPUT para capturar los mensajes del SP
                cursor.callproc("DBMS_OUTPUT.ENABLE")

                # Ejecutar el SP con los parámetros de entrada y salida
                output_msg = cursor.var(cx_Oracle.STRING)
                cursor.callproc("SP_EliminarRol", [idRol, output_msg])

                # Recuperar el mensaje de salida del SP
                mensaje_salida = output_msg.getvalue()

                # Realizar el commit si no hay mensajes de error
                if mensaje_salida == "El rol ha sido eliminado exitosamente.":
                    connection.commit()

                print(mensaje_salida)

            # Si no encuentra el rol
            else:
                print("ID de rol incorrecto")

        # Si cancela la operación
        else:
            print("Operación cancelada")
            menu_roles()

    except Exception as ex:
        print(ex)

    finally:
        if connection:
            connection.close()

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
    idRol_array, nombre_array = VerRoles()

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
        EditarRol(id_rol_a_editar, nuevo_nombre)

def verRolEspecifico():
    connection = None
    try:
        while True:
            # Pedir al usuario el ID del rol
            id_rol_input = input("Ingrese el ID del rol (o 'q' para volver al menu): ")
            
            if id_rol_input.lower() == 'q':
                menu_roles()
                
            
            if not id_rol_input:
                print("Error: El ID del rol no puede estar vacío.")
                continue

            id_rol = int(id_rol_input)

            # Establecer la conexión a la base de datos
            connection = establecer_conexion()

            # Crear un cursor para llamar al procedimiento SP_LeerRol
            cursor = connection.cursor()

            # Habilitar el modo "serveroutput"
            cursor.callproc("dbms_output.enable")

            # Llamar al procedimiento SP_LeerRol
            cursor.callproc("SP_LeerRol", [id_rol])

            # Obtener los mensajes de salida del procedimiento y mostrarlos
            status_var = cursor.var(cx_Oracle.NUMBER)
            line_var = cursor.var(str)
            while True:
                cursor.callproc("dbms_output.get_line", (line_var, status_var))
                if status_var.getvalue() != 0:
                    break
                print(line_var.getvalue())

            # Cerrar el cursor y confirmar la transacción
            cursor.close()
            connection.commit()

    except ValueError:
        print("Error: Ingrese un valor numérico válido.")
    except cx_Oracle.DatabaseError as e:
        print("Error al obtener el rol:", e)
    finally:
        # Cerrar la conexión si está definida
        if connection is not None:
            connection.close()

#--------------------MODULO USUARIOS--------------------#
def EncUsuarioID(idUsuario):
    encontrado = False
    dUsuario = []

    try:
        connection = establecer_conexion()
        cursor = connection.cursor()

        # Crear un objeto de tipo cursor para el resultado del SP
        result_cursor = cursor.var(cx_Oracle.CURSOR)

        # Ejecutar el SP para obtener el usuario por ID
        cursor.callproc("SP_ObtenerUsuarioPorID", [idUsuario, result_cursor])

        # Obtener el resultado del SP del cursor
        result_set = result_cursor.getvalue()

        # Verificar si se encontró el usuario
        for row in result_set:
            if str(row[0]) == idUsuario:
                dUsuario = row
                encontrado = True
                break

    except Exception as ex:
        print(ex)

    finally:
        if connection:
            connection.close()

    return encontrado, dUsuario

def VerUsuarios():
    try:
        connection=establecer_conexion()
        ##print(connection.version)
        cursor=connection.cursor()

        cursor.execute("SELECT * FROM usuario")
        results = cursor.fetchall()

        print("Número de filas recuperadas:", len(results))
        for row in results:
            print(row)

    except Exception as ex:
        print(ex)

    finally:
        if connection:
            connection.close()

def InsertUsuario():
    if rolesCant() != 0:
        # DATOS DE USUARIO
        nombre = ""
        while nombre == "":
            nombre = input("Ingrese su nombre: ")
        # ---- APELLIDO 1
        apellido1 = ""
        while apellido1 == "":
            apellido1 = input("Ingrese su Primer Apellido: ")
        # ---- APELLIDO 2
        apellido2 = ""
        while apellido2 == "":
            apellido2 = input("Ingrese su Segundo Apellido: ")
        # ---- CEDULA
        cedula = ""
        while cedula == "":
            cedula = input("Ingrese su cédula: ")
        # ---- CORREO
        correo = ""
        while correo == "":
            correo = input("Ingrese su correo: ")
        contrasenna = input("Ingrese su contraseña: ")
        # ---- ROL
        idRol = ""
        encontrado = False
        while not encontrado and idRol == "":
            usuarios = VerRoles()

            u = ""
            for u in usuarios:
                u = str(u) + "\n"

            idRol = input("Ingrese su rol: \n")

            for i in usuarios:
                if str(i[0]) == idRol:
                    encontrado = True
                    idRol = i[0]
                    break

            if not encontrado:
                print("Rol no encontrado\nReintente nuevamente")
        try:
            connection = establecer_conexion()
            ##coneccion 
            cursor = connection.cursor()

            # Recuperar los mensajes de DBMS_OUTPUT
            message = cursor.var(cx_Oracle.STRING)
            status = cursor.var(cx_Oracle.NUMBER)
            # Llamada al SP para crear el usuario
            cursor.callproc("SP_CrearUsuario", [nombre, apellido1, apellido2, cedula, correo, contrasenna, idRol])
            cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))
            while status.getvalue() == 0:
                print(message.getvalue())
                cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))

            cursor.execute("commit")


        except Exception as ex:
            print(ex)

        finally:
            if connection:
                connection.close()
    else:
        print("Debe crear roles previamente")

def VerUsuarioEspecifico():
    op = ""
    id = ""
    nombre = ""
    Apellido1 = ""
    Apellido2 = ""
    Cedula = ""
    Correo = ""

    while op == "":
        op = input("Con cual dato quiere buscar el usuario:"
                   "\n1. ID"
                   "\n2. Nombre"
                   "\n3. Apellido1"
                   "\n4. Apellido2"
                   "\n5. Cedula"
                   "\n6. Correo"
                   "\n7. Salir\nOpción: "
                   )

        if op == "1":
            id = input("Ingrese el id del usuario: ")
        elif op == "2":
            nombre = input("Ingrese el nombre del usuario: ")
        elif op == "3":
            Apellido1 = input("Ingrese el primer apellido del usuario: ")
        elif op == "4":
            Apellido2 = input("Ingrese el segundo apellido del usuario: ")
        elif op == "5":
            Cedula = input("Ingrese la cedula del usuario: ")
        elif op == "6":
            Correo = input("Ingrese el correo del usuario: ")
        elif op == "7":
            print("Saliendo...")
            menu_usuarios()

        try:
            connection = establecer_conexion()
            cursor = connection.cursor()

            # SELECT para buscar el usuario según el atributo proporcionado
            query = "SELECT idUsuario, nombre, primApellido, segApellido, cedula, correo FROM usuario WHERE "

            bind_variables = {}  # Diccionario para mantener las variables vinculadas

            if op == "1":
                query += "idUsuario = :idUsuario"
                bind_variables['idUsuario'] = id
            elif op == "2":
                query += "nombre = :nombreUsuario"
                bind_variables['nombreUsuario'] = nombre
            elif op == "3":
                query += "primApellido = :apellido1"
                bind_variables['apellido1'] = Apellido1
            elif op == "4":
                query += "segApellido = :apellido2"
                bind_variables['apellido2'] = Apellido2
            elif op == "5":
                query += "cedula = :cedulaUsuario"
                bind_variables['cedulaUsuario'] = Cedula
            elif op == "6":
                query += "correo = :correoUsuario"
                bind_variables['correoUsuario'] = Correo
            else:
                return

            # Ejecutar la consulta SQL con los parámetros correspondientes
            cursor.execute(query, bind_variables)

            results = cursor.fetchall()

            for row in results:
                print(row)

        except Exception as ex:
            print(ex)

        finally:
            if connection:
                connection.close()

def ActualizarUsuario():
    print("********USUARIOS*********")
    VerUsuarios()
    print("*************************")
    
    # Pide el id del usuario a actualizar
    idUsuario = ""
    while idUsuario == "":
        idUsuario = input("Ingrese el id del usuario a actualizar: ")
        
    # Se busca el usuario por id
    (encontrado, dUsuario) = EncUsuarioID(idUsuario)
    
    if encontrado:
        idUsuario = dUsuario[0]
        nombre = dUsuario[1]
        primApellido = dUsuario[2]
        segApellido = dUsuario[3]
        cedula = dUsuario[4]
        correo = dUsuario[5]
        contrasenna = dUsuario[6]
        idRol = dUsuario[7]
        idDireccion = dUsuario[8]

        nombre2 = ""
        primApellido2 = ""
        segApellido2 = ""
        cedula2 = ""
        correo2 = ""
        contrasenna2 = ""
        idRol2 = ""
        idDireccion2 = ""
        
        op = ""
        while str(op) != "0":
            print(
                "QUE DATO DESEA EDITAR: \n"
                "1. Nombre: (" + nombre + ")\n"
                "2. Primer Apellido: (" + primApellido + ")\n"
                "3. Segundo Apellido: (" + segApellido + ")\n"
                "4. Cedula: (" + str(cedula) + ")\n"
                "5. Correo: (" + correo + ")\n"
                "6. Contraseña: (" + contrasenna + ")\n"
                "7. Rol: (" + str(idRol) + ")\n"
                "8. Direccion: (" + str(idDireccion) + ")\n"
                "0. Salir"
            )
            op = input("Ingrese una opción: ")
            
            if op == "1":
                nombre = input("Ingrese el nuevo nombre: ")
            elif op == "2":
                primApellido = input("Ingrese el nuevo primer apellido: ")
            elif op == "3":
                segApellido = input("Ingrese el nuevo segundo apellido: ")
            elif op == "4":
                cedula = input("Ingrese la nueva cedula: ")
            elif op == "5":
                correo = input("Ingrese el nuevo correo: ")
            elif op == "6":
                contrasenna = input("Ingrese la nueva contraseña: ")
            elif op == "7":
                VerRoles()
                idRol = input("Ingrese el nuevo rol: ")

        try:
            connection = establecer_conexion()
            cursor = connection.cursor()

            # Recuperar los mensajes de DBMS_OUTPUT
            message = cursor.var(cx_Oracle.STRING)
            status = cursor.var(cx_Oracle.NUMBER)
            cursor.callproc("SP_EditarUsr", [idUsuario, nombre, primApellido, segApellido, cedula, correo,
                                             contrasenna, idRol, idDireccion])
            cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))
            while status.getvalue() == 0:
                print(message.getvalue())
                cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))

            cursor.execute("commit")
            
        except Exception as ex:
            print(ex)
        finally:
            if connection:
                connection.close()

    else:
        print("Usuario no encontrado")

def VerUsuariosRol(idRol):
    try:
        connection = establecer_conexion()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM V_UsuariosConRol WHERE \"ID Rol\"='" + str(idRol) + "'")
        results = cursor.fetchall()
        usuarios = []

        for row in results:
            usuarios.append(row)

    except Exception as ex:
        print(ex)

    finally:
        if connection:
            connection.close()
    return usuarios

def eliminar_usuario():
    try:
        #Establecer conexion
        connection = establecer_conexion()
        VerUsuarios()

        
        # Crear un cursor
        cursor = connection.cursor()

        # Solicitar el ID del usuario a eliminar
        while True:
            id_usuario_input = input("\nIngrese el ID del usuario que desea eliminar (o 'q' para salir): ")
            
            if id_usuario_input.lower() == 'q':
                print("\nSaliendo...")
                return
                
            if not id_usuario_input.isdigit():
                print("Entrada inválida. Ingrese un número de ID válido o 'q' para salir.")
                continue
                
            id_usuario = int(id_usuario_input)
            break

        # Llamada al procedimiento almacenado para eliminar el usuario
        cursor.callproc("SP_EliminarUsuario", [id_usuario])

        # Realizar commit en la transacción
        connection.commit()
        print("\nUsuario eliminado exitosamente.")

    except Exception as ex:
        print("Error:", ex)
    finally:
        if connection:
            connection.close()

#---------------------MODULO TIPO SERVICIOS---------------------
def tipoServicioDatos():
    try:
        connection=establecer_conexion()
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM TipoServicio")
        results = cursor.fetchall()
        tipoProducto=[]
        
        for row in results:
            tipoProducto.append(row)
            
    except Exception as ex:
        print(ex)
        
    finally:
        if connection:
            connection.close()
    return tipoProducto

def EncTipoServicioID(idTipoServicio):
    try:
        connection=establecer_conexion()
        
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM TipoServicio WHERE idTipoServicio='"+str(idTipoServicio)+"'")
        results = cursor.fetchall()
        encontrado=False
        dTipoServicio=[]
        for row in results:
            if (str(row[0])==idTipoServicio):
                dTipoServicio=row
                encontrado=True
                break
    except Exception as ex:
        print(ex)
    
    finally:
        if connection:
            connection.close()
    
    return encontrado,row

def InsertTipoServicio():
    ## ---- NOMBRE TIPO PRODUCTO
    nombre=""
    while (nombre==""):
        nombre=input("Ingrese el nombre del tipo de servicio: ")
    ## --- DESCRIPCION TIPO PRODUCTO
    desc=""
    while (desc==""):
        desc=input("Ingrese la descripcion del tipo de servicio: ")
    
    try:
        # Establecer la conexión a la base de datos
        con=establecer_conexion()
        if con is None:
            print("No se logró establecer la conexión con la base de datos en el proceso de inserción")
        else:
            cursor=con.cursor()
            cursor.callproc("DBMS_OUTPUT.ENABLE")
            cursor.callproc("SP_CrearTipoServicio",[nombre,desc])
            # Recuperar los mensajes de salida
            status_var = cursor.var(cx_Oracle.NUMBER)
            line_var = cursor.var(cx_Oracle.STRING)
            while True:
                cursor.callproc('DBMS_OUTPUT.GET_LINE', (line_var, status_var))
                if status_var.getvalue() != 0:
                    break
                print(line_var.getvalue())
            con.commit()
            
    except Exception as ex:
        print(ex)
    finally:
        if con:
            con.close()
# InsertTipoServicio()

def vistaTipoServicio():
    try:
        # Establecer la conexión a la base de datos
        con = establecer_conexion()
        if con is None:
            print("No se logró establecer la conexión con la base de datos en el proceso de inserción")
        else:
            cur = con.cursor()
            cur.callproc("DBMS_OUTPUT.ENABLE")
            cur.execute("SELECT * FROM V_TiposServicio")
            
            # Recuperar los mensajes de salida
            results = cur.fetchall()
            if results:
                print("--- Tipos de Servicios Registrados ---")
                print("{:<5} {:<20} {:<30}".format("ID", "Nombre", "Descripción"))
                for row in results:
                    print("{:<5} {:<20} {:<30}".format(row[0], row[1], row[2]))
            else:
                print("No hay registros")

    except Exception as ex:
        print(ex)
    finally:
        if con:
            con.close()
# vistaTipoServicio()

def verTipoServicioEspecifico():
    try:
        # Establecer la conexión a la base de datos
        connection = establecer_conexion()
        
        # Crear un cursor
        cursor = connection.cursor()

        # Solicitar el ID del tipo de servicio a leer
        while True:
            id_tipo_servicio_input = input("\nIngrese el ID del tipo de servicio que desea leer (o 'q' para salir): ")
            
            if id_tipo_servicio_input.lower() == 'q':
                print("Saliendo...")
                return
                
            if not id_tipo_servicio_input.isdigit():
                print("Entrada inválida. Ingrese un número de ID válido o 'q' para salir.")
                continue
                
            id_tipo_servicio = int(id_tipo_servicio_input)
            break

        # Configurar la salida de mensajes del servidor
        cursor.callproc("DBMS_OUTPUT.ENABLE")

        # Llamada al procedimiento almacenado para leer el tipo de servicio
        cursor.callproc("SP_LeerTipoServicio", [id_tipo_servicio])

        # Recuperar los mensajes de DBMS_OUTPUT
        message = cursor.var(cx_Oracle.STRING)
        status = cursor.var(cx_Oracle.NUMBER)
        cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))
        while status.getvalue() == 0:
            print(message.getvalue())
            cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))

    except Exception as ex:
        print("Error:", ex)
    finally:
        if connection:
            connection.close()

def editarTipoServicio():
    vistaTipoServicio()
    
    #pide el id del tipo de producto a actualizar
    idTipoServicio=""
    dTipoServicio=[]
    
    while (idTipoServicio==""):
        idTipoServicio=input("Ingrese el id del tipo de servicio a actualizar: ")

    #se buscar el tipo de producto por id
    (encontrado,dTipoServicio)=EncTipoServicioID(idTipoServicio)
    
    if encontrado:
        idTipoServicio=dTipoServicio[0]
        nombre=dTipoServicio[1]
        desc=dTipoServicio[2]
        
        nombre2=""
        des2=""
        
        op=""
        while (str(op)!="0"):
            print(
                "QUE DATO DESEA EDITAR: \n"
                "1. Nombre: ("+nombre+")\n"
                "2. Descripcion: ("+desc+")\n"
                "0. Salir"
            )
            op=input("Ingrese una opción: ")
            if op=="1":
                nombre=input("Ingrese el nuevo nombre: ")
            elif op=="2":
                desc=input("Ingrese la nueva descripcion: ")
            
            try:
                con=establecer_conexion()
                if con is None:
                    print("No se logró establecer la conexión con la base de datos")
                else:
                    cursor=con.cursor()
                    cursor.callproc("DBMS_OUTPUT.ENABLE")
                    cursor.callproc("SP_EditarTipoServicio",[idTipoServicio,nombre,desc])
                    # Recuperar los mensajes de salida
                    status_var = cursor.var(cx_Oracle.NUMBER)
                    line_var = cursor.var(cx_Oracle.STRING)
                    while True:
                        cursor.callproc('DBMS_OUTPUT.GET_LINE', (line_var, status_var))
                        if status_var.getvalue() != 0:
                            break
                        print(line_var.getvalue())
                    con.commit()
            except Exception as ex:
                print(ex)
            finally:
                if con:
                    con.close()
    else:
        print("Tipo de servicio no encontrado")
# editarTipoProducto()

def eliminarTipoServicio():
    vistaTipoServicio()
    op=""
    while op=="":
        op=input("Ingrese el id del tipo de servicio a eliminar: ")
    
    try:
        con=establecer_conexion()
        cursor=con.cursor()
        cursor.callproc("DBMS_OUTPUT.ENABLE")
        cursor.callproc("SP_EliminarTipoServicio",[str(op)])
        #recuperar los mensajes de salida
        status_var = cursor.var(cx_Oracle.NUMBER)
        line_var = cursor.var(cx_Oracle.STRING)
        while True:
            cursor.callproc('DBMS_OUTPUT.GET_LINE', (line_var, status_var))
            if status_var.getvalue() != 0:
                break
            print(line_var.getvalue())
        con.commit()
    except Exception as ex:
        print(ex)
    finally:
        if con:
            con.close()
# eliminarTipoProducto()

#-------------------------MODULO SERVICIOS-------------------------
def EncServicioID(idServicio):
    try:
        connection=establecer_conexion()
        
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM Servicio WHERE idServicio='"+str(idServicio)+"'")
        results = cursor.fetchall()
        encontrado=False
        dServicio=[]
        for row in results:
            if (str(row[0])==idServicio):
                dServicio=row
                encontrado=True
                break
    except Exception as ex:
        print(ex)
    
    finally:
        if connection:
            connection.close()
    
    return encontrado,dServicio

def InsertServicio():
    nombre=""
    while(nombre==""):
        nombre=input("Ingrese el nombre del servicio: ")
    desc=""
    while(desc==""):
        desc=input("Ingrese la descripcion del servicio: ")
    img="/"
    cupos=0
    while(cupos==0):
        cupos=input("Ingrese el numero de cupos: ")
    estatus=1
    fecha=""
    ##la fecha se ingresa en el formato dd/mmm/yyy (ejemplo: 01/ene/2021)
    while(fecha==""):
        fecha=input("Ingrese la fecha: (dd/mmm/yyyy) (ejemplo 01/jan/2011): ")
    idTipoServicio=0
    while(idTipoServicio==0):
        vistaTipoServicio()
        idTipoServicio=input("Ingrese el id del tipo de servicio: ")
    try:
        con=establecer_conexion()
        if con is None:
            print("No se logró establecer la conexión con la base de datos")
        else:
            cursor=con.cursor()
            cursor.callproc("DBMS_OUTPUT.ENABLE")
            cursor.callproc("SP_CrearServicio",[nombre,img,desc,cupos,estatus,fecha,idTipoServicio])
            # Recuperar los mensajes de salida
            status_var = cursor.var(cx_Oracle.NUMBER)
            line_var = cursor.var(cx_Oracle.STRING)
            while True:
                cursor.callproc('DBMS_OUTPUT.GET_LINE', (line_var, status_var))
                if status_var.getvalue() != 0:
                    break
                print(line_var.getvalue())
            con.commit()
    except Exception as ex:
        print(ex)
    finally:
        if con:
            con.close()
# InsertServicio()

def vistaServicios():
    try:
        # Establecer la conexión a la base de datos
        con = establecer_conexion()
        if con is None:
            print("No se logró establecer la conexión con la base de datos en el proceso de inserción")
        else:
            cur = con.cursor()
            cur.callproc("DBMS_OUTPUT.ENABLE")
            cur.execute("SELECT * FROM V_Servicios")
            
            # Recuperar los mensajes de salida
            results = cur.fetchall()
            if results:
                print("---Servicios Registrados---")
                print("{:<10} {:<30} {:<50} {:<10} {:<10} {:<15} {:<20}".format("ID", "Nombre", "Descripcion", "Cupos", "Estatus", "Fecha", "TipoServicio"))
                for row in results:
                    print("{:<10} {:<30} {:<50} {:<10} {:<10} {:<15} {:<20}".format(row[0], row[1], row[3], row[4], row[5], row[6].strftime('%d-%m-%Y'), row[7]))
            else:
                print("No hay registros")

    except Exception as ex:
        print(ex)
    finally:
        if con:
            con.close()
# vistaServicios()

def verServicioEspecifico():
    try:
        # Establecer la conexión a la base de datos
        connection = establecer_conexion()
        
        # Crear un cursor
        cursor = connection.cursor()

        # Solicitar el ID del servicio a leer
        while True:
            id_servicio_input = input("\nIngrese el ID del servicio que desea leer (o 'q' para salir): ")
            
            if id_servicio_input.lower() == 'q':
                print("Saliendo...")
                return
                
            if not id_servicio_input.isdigit():
                print("Entrada inválida. Ingrese un número de ID válido o 'q' para salir.")
                continue
                
            id_servicio = int(id_servicio_input)
            break

        # Llamada al procedimiento almacenado para leer el servicio
        cursor.callproc("SP_LeerServicio", [id_servicio])

        # Recuperar los mensajes de DBMS_OUTPUT
        message = cursor.var(cx_Oracle.STRING)
        status = cursor.var(cx_Oracle.NUMBER)
        cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))
        while status.getvalue() == 0:
            print(message.getvalue())
            cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))

    except Exception as ex:
        print("Error:", ex)
    finally:
        if connection:
            connection.close()

def editarServicio():
    vistaServicios()
    
    idServicio=""
    dServicio=[]
    
    while(idServicio==""):
        idServicio=input("Ingrese el id del servicio a actualizar: ")
        
    (encontrado,dServicio)=EncServicioID(idServicio)
    if encontrado:
        idServicio=dServicio[0]
        nombre=dServicio[1]
        desc=dServicio[3]
        cupos=dServicio[4]
        estatus=dServicio[5]
        fecha=dServicio[6].strftime("%d/%b/%Y")
        idTipoServicio=dServicio[7]
        (encontrado,dTipoServicio)=EncTipoServicioID(idTipoServicio)
        nombreTipoServicio=dTipoServicio[1]
        
        op=""
        while op!="0":
            print(
                "QUE DATO DESEA EDITAR: \n"
                "1. Nombre: ("+nombre+")\n"
                "2. Descripcion: ("+desc+")\n"
                "3. Cupos: ("+str(cupos)+")\n"
                "4. Estatus: ("+str(estatus)+")\n"
                "5. Fecha: ("+fecha+")\n"
                "6. Tipo de Servicio: ("+str(idTipoServicio)+"-"+nombreTipoServicio+")\n"
                "0. Salir"
            )
            op=input("Ingrese una opción: ")
            
            if op=="1":
                nombre=input("Ingrese el nuevo nombre: (anterior: "+nombre+")")
            elif op=="2":
                desc=input("Ingrese la nueva descripcion: (anterior: "+desc+")")
            elif op=="3":
                cupos=input("Ingrese el nuevo numero de cupos: (anterior: "+str(cupos)+")")
            elif op=="4":
                tipoEstatus=""
                if estatus==1:
                    tipoEstatus="Activo"
                else:
                    tipoEstatus="Inactivo"
                    
                estatus=input("Ingrese el nuevo estatus: (anterior: "+tipoEstatus+"\n)"
                            "1. Activo\n"
                            "0. Inactivo\n")
            elif op=="5":
                fecha=input("Ingrese la nueva fecha: (anterior: "+fecha+") (dd/mmm/yyyy) (ejemplo 01/jan/2011): ")
                
            elif op=="6":
                vistaTipoServicio()
                (encontrado,dTipoServicio)=EncTipoServicioID(idTipoServicio)
                nombreTipoServicio=dTipoServicio[1]
                idTipoServicio=input("Ingrese el nuevo id del tipo de servicio: (anterior: "+str(idTipoServicio)+")")
            
            try:
                con=establecer_conexion()
                if con is None:
                    print("No se logró establecer la conexión con la base de datos")
                else:
                    cursor=con.cursor()
                    cursor.callproc("DBMS_OUTPUT.ENABLE")
                    cursor.callproc("SP_EditarServicio",[str(idServicio),nombre,desc,str(cupos),str(estatus),fecha,str(idTipoServicio)])
                    # Recuperar los mensajes de salida
                    status_var = cursor.var(cx_Oracle.NUMBER)
                    line_var = cursor.var(cx_Oracle.STRING)
                    while True:
                        cursor.callproc('DBMS_OUTPUT.GET_LINE', (line_var, status_var))
                        if status_var.getvalue() != 0:
                            break
                        print(line_var.getvalue())
                    con.commit()
            except Exception as ex:
                print(ex)
            finally:
                if con:
                    con.close()
# editarServicio()

def eliminarServicio():
    vistaServicios()
    
    op=""
    while op=="":
        op=input("Ingrese el id del servicio a eliminar o 'S' para SALIR:")
    
    if op.upper()!="S":
        try:
            con=establecer_conexion()
            cursor=con.cursor()
            cursor.callproc("DBMS_OUTPUT.ENABLE")
            cursor.callproc("SP_EliminarServicio",[str(op)])
            #recuperar los mensajes de salida
            status_var = cursor.var(cx_Oracle.NUMBER)
            line_var = cursor.var(cx_Oracle.STRING)
            while True:
                cursor.callproc('DBMS_OUTPUT.GET_LINE', (line_var, status_var))
                if status_var.getvalue() != 0:
                    break
                print(line_var.getvalue())
            con.commit()
        except Exception as ex:
            print(ex)
        finally:
            if con:
                con.close()
# eliminarServicio()

def verServiciosPorTipo():
    vistaTipoServicio()
    idTipoServicio=""
    while idTipoServicio=="":
        idTipoServicio=input("Ingrese el id del tipo de servicio: ")
    
    try:
        con=establecer_conexion()
        if con is None:
            print("No se logró establecer la conexión con la base de datos")
        else:
            cursor=con.cursor()
            cursor.callproc("DBMS_OUTPUT.ENABLE")
            cursor.callproc("SP_verServiciosTipo",[str(idTipoServicio)])
            # Recuperar los mensajes de salida
            status_var = cursor.var(cx_Oracle.NUMBER)
            line_var = cursor.var(cx_Oracle.STRING)
            while True:
                cursor.callproc('DBMS_OUTPUT.GET_LINE', (line_var, status_var))
                if status_var.getvalue() != 0:
                    break
                print(line_var.getvalue())
            con.commit()
    except Exception as ex:
        print(ex)
    finally:
        if con:
            con.close()
# verServiciosPorTipo()

#-------------------------MODULO TIPO PRODUCTOS-------------------------
def tipoProductoDatos():
    try:
        connection=establecer_conexion()
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM TipoProducto")
        results = cursor.fetchall()
        tipoProducto=[]
        
        for row in results:
            tipoProducto.append(row)
            
    except Exception as ex:
        print(ex)
        
    finally:
        if connection:
            connection.close()
    return tipoProducto

def EncTipoProductoID(idTipoProducto):
    try:
        connection=establecer_conexion()
        
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM TipoProducto WHERE idTipoProducto='"+str(idTipoProducto)+"'")
        results = cursor.fetchall()
        encontrado=False
        dTipoProducto=[]
        for row in results:
            if (str(row[0])==idTipoProducto):
                dTipoProducto=row
                encontrado=True
                break
    except Exception as ex:
        print(ex)
    
    finally:
        if connection:
            connection.close()
    
    return encontrado,row

def InsertTipoProducto():
    ## ---- NOMBRE TIPO PRODUCTO
    nombre=""
    while (nombre==""):
        nombre=input("Ingrese el nombre del tipo de Producto: ")
    ## --- DESCRIPCION TIPO PRODUCTO
    desc=""
    while (desc==""):
        desc=input("Ingrese la descripcion del tipo de Producto: ")
    
    try:
        # Establecer la conexión a la base de datos
        con=establecer_conexion()
        if con is None:
            print("No se logró establecer la conexión con la base de datos en el proceso de inserción")
        else:
            cursor=con.cursor()
            cursor.callproc("DBMS_OUTPUT.ENABLE")
            cursor.callproc("SP_CrearTipoProducto",[nombre,desc])
            # Recuperar los mensajes de salida
            status_var = cursor.var(cx_Oracle.NUMBER)
            line_var = cursor.var(cx_Oracle.STRING)
            while True:
                cursor.callproc('DBMS_OUTPUT.GET_LINE', (line_var, status_var))
                if status_var.getvalue() != 0:
                    break
                print(line_var.getvalue())
            con.commit()
            
    except Exception as ex:
        print(ex)
    finally:
        if con:
            con.close()
# InsertTipoProducto()

def vistaTipoProducto():
    try:
        # Establecer la conexión a la base de datos
        con=establecer_conexion()
        if con is None:
            print("No se logró establecer la conexión con la base de datos en el proceso de inserción")
        else:
            cur=con.cursor()
            cur.callproc("DBMS_OUTPUT.ENABLE")
            cur.execute("SELECT * FROM V_TiposProducto")
            
            # Recuperar los mensajes de salida
            results = cur.fetchall()
            if results:
                print("---Tipos de Productos Registrados---")
                print("ID","\tNombre","\tDescripcion")
                for row in results:
                    print(row[0],"\t",row[1],"\t",row[2])
            else:
                print("No hay registros")

    except Exception as ex:
        print(ex)
    finally:
        if con:
            con.close()
# vistaTipoProducto()

def verTipoProductoEspecifico():
    try:
        # Establecer la conexión a la base de datos
        connection = establecer_conexion()
        
        # Crear un cursor
        cursor = connection.cursor()

        # Habilitar DBMS_OUTPUT para capturar los mensajes del procedimiento
        cursor.callproc("DBMS_OUTPUT.ENABLE")
        
        # Solicitar el ID del tipo de producto a leer
        while True:
            id_tipo_producto_input = input("\nIngrese el ID del tipo de producto que desea leer (o 'q' para salir): ")
            
            if id_tipo_producto_input.lower() == 'q':
                print("Saliendo...")
                return
                
            if not id_tipo_producto_input.isdigit():
                print("Entrada inválida. Ingrese un número de ID válido o 'q' para salir.")
                continue
                
            id_tipo_producto = int(id_tipo_producto_input)
            break

        # Llamada al procedimiento almacenado para leer el tipo de producto
        cursor.callproc("SP_LeerTipoProducto", [id_tipo_producto])

        # Recuperar los mensajes de DBMS_OUTPUT
        message = cursor.var(cx_Oracle.STRING)
        status = cursor.var(cx_Oracle.NUMBER)
        cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))
        while status.getvalue() == 0:
            print(message.getvalue())
            cursor.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))

    except Exception as ex:
        print("Error:", ex)
    finally:
        if connection:
            connection.close()

def editarTipoProducto():
    vistaTipoProducto()
    
    #pide el id del tipo de producto a actualizar
    idTipoProducto=""
    dTipoProducto=[]
    
    while (idTipoProducto==""):
        idTipoProducto=input("Ingrese el id del tipo de Producto a actualizar: ")

    #se buscar el tipo de producto por id
    (encontrado,dTipoProducto)=EncTipoProductoID(idTipoProducto)
    
    if encontrado:
        idTipoProducto=dTipoProducto[0]
        nombre=dTipoProducto[1]
        desc=dTipoProducto[2]
        
        nombre2=""
        des2=""
        
        op=""
        while (str(op)!="0"):
            print(
                "QUE DATO DESEA EDITAR: \n"
                "1. Nombre: ("+nombre+")\n"
                "2. Descripcion: ("+desc+")\n"
                "0. Salir"
            )
            op=input("Ingrese una opción: ")
            if op=="1":
                nombre=input("Ingrese el nuevo nombre: ")
            elif op=="2":
                desc=input("Ingrese la nueva descripcion: ")
            
            try:
                con=establecer_conexion()
                if con is None:
                    print("No se logró establecer la conexión con la base de datos")
                else:
                    cursor=con.cursor()
                    cursor.callproc("DBMS_OUTPUT.ENABLE")
                    cursor.callproc("SP_EditarTipoProducto",[idTipoProducto,nombre,desc])
                    # Recuperar los mensajes de salida
                    status_var = cursor.var(cx_Oracle.NUMBER)
                    line_var = cursor.var(cx_Oracle.STRING)
                    while True:
                        cursor.callproc('DBMS_OUTPUT.GET_LINE', (line_var, status_var))
                        if status_var.getvalue() != 0:
                            break
                        print(line_var.getvalue())
                    con.commit()
            except Exception as ex:
                print(ex)
            finally:
                if con:
                    con.close()
    else:
        print("Tipo de Producto no encontrado")
# editarTipoProducto()

def eliminarTipoProducto():
    vistaTipoProducto()
    op=""
    while op=="":
        op=input("Ingrese el id del tipo de Producto a eliminar: ")
    
    try:
        con=establecer_conexion()
        cursor=con.cursor()
        cursor.callproc("DBMS_OUTPUT.ENABLE")
        cursor.callproc("SP_EliminarTipoProducto",[str(op)])
        #recuperar los mensajes de salida
        status_var = cursor.var(cx_Oracle.NUMBER)
        line_var = cursor.var(cx_Oracle.STRING)
        while True:
            cursor.callproc('DBMS_OUTPUT.GET_LINE', (line_var, status_var))
            if status_var.getvalue() != 0:
                break
            print(line_var.getvalue())
        con.commit()
    except Exception as ex:
        print(ex)
    finally:
        if con:
            con.close()
# eliminarTipoProducto()

#-------------------------MODULO Productos-------------------------
def EncProductoID(idProducto):
    try:
        connection=establecer_conexion()
        
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM Producto WHERE idProducto='"+str(idProducto)+"'")
        results = cursor.fetchall()
        encontrado=False
        dProducto=[]
        for row in results:
            if (str(row[0])==idProducto):
                dProducto=row
                encontrado=True
                break
    except Exception as ex:
        print(ex)
    
    finally:
        if connection:
            connection.close()
    
    return encontrado,dProducto

def InsertProducto():
    nombre=""
    while(nombre==""):
        nombre=input("Ingrese el nombre del producto: ")
    desc=""
    while(desc==""):
        desc=input("Ingrese la descripcion del producto: ")
    stock=0
    while(stock==0):
        stock=input("Ingrese el numero de stock: ")
    estatus=1
    precio=0
    while(precio==0):
        precio=input("Ingrese el precio: ")
    idTipoProducto=0
    while(idTipoProducto==0):
        vistaTipoProducto()
        idTipoProducto=input("Ingrese el id del tipo de producto: ")
    try:
        con=establecer_conexion()
        if con is None:
            print("No se logró establecer la conexión con la base de datos")
        else:
            cursor=con.cursor()
            cursor.callproc("DBMS_OUTPUT.ENABLE")
            cursor.callproc("SP_CrearProducto",[nombre,desc,stock,estatus,precio,idTipoProducto])
            # Recuperar los mensajes de salida
            status_var = cursor.var(cx_Oracle.NUMBER)
            line_var = cursor.var(cx_Oracle.STRING)
            while True:
                cursor.callproc('DBMS_OUTPUT.GET_LINE', (line_var, status_var))
                if status_var.getvalue() != 0:
                    break
                print(line_var.getvalue())
            con.commit()
    except Exception as ex:
        print(ex)
    finally:
        if con:
            con.close()
# InsertProducto()

def vistaProductos():
    try:
        # Establecer la conexión a la base de datos
        con = establecer_conexion()
        if con is None:
            print("No se logró establecer la conexión con la base de datos en el proceso de inserción")
        else:
            cur = con.cursor()
            cur.callproc("DBMS_OUTPUT.ENABLE")
            cur.execute("SELECT * FROM V_Productos")
            
            # Recuperar los mensajes de salida
            results = cur.fetchall()
            if results:
                print("---Productos Registrados---")
                print("{:<6} {:<20} {:<60} {:<10} {:<8} {:<20}".format("ID", "Nombre", "Descripción", "Stock", "Estatus", "TipoProducto"))
                for row in results:
                    print("{:<6} {:<20} {:<60} {:<10} {:<8} {:<20}".format(row[0], row[1], row[2], row[3], row[4], row[5]))
            else:
                print("No hay registros")
                
    except Exception as ex:
        print("Error:", ex)
    finally:
        if con:
            con.close()

def verProductoEspecifico():
    try:
        # Establecer la conexión a la base de datos
        con = establecer_conexion()
        
        if con is None:
            print("No se logró establecer la conexión con la base de datos.")
        else:
            cur = con.cursor()
            
            # Habilitar DBMS_OUTPUT para capturar los mensajes del procedimiento
            cur.callproc("DBMS_OUTPUT.ENABLE")
            
            # Solicitar el ID del producto a ver
            while True:
                id_producto_input = input("\nIngrese el ID del producto que desea ver (o 'q' para salir): ")
                
                if id_producto_input.lower() == 'q':
                    print("Saliendo...")
                    return
                    
                if not id_producto_input.isdigit():
                    print("Entrada inválida. Ingrese un número de ID válido o 'q' para salir.")
                    continue
                    
                id_producto = int(id_producto_input)
                break
            
            cur.callproc("SP_LeerProducto", [id_producto])  # Llamar al procedimiento almacenado
            
            # Recuperar los mensajes de salida
            message = cur.var(cx_Oracle.STRING)
            status = cur.var(cx_Oracle.NUMBER)
            cur.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))
            while status.getvalue() == 0:
                print(message.getvalue())
                cur.execute('BEGIN DBMS_OUTPUT.GET_LINE(:message, :status); END;', (message, status))
                
    except Exception as ex:
        print("Error:", ex)
    finally:
        if con:
            con.close()

def editarProductos():
    vistaProductos()
    
    idProducto=""
    dProducto=[]
    
    while(idProducto==""):
        idProducto=input("Ingrese el id del producto a actualizar: ")
        
    (encontrado,dProducto)=EncProductoID(idProducto)
    if encontrado:
        idProducto=dProducto[0]
        nombre=dProducto[1]
        desc=dProducto[2]
        stock=dProducto[3]
        estatus=dProducto[4]
        precio=dProducto[5]
        idTipoProducto=dProducto[6]
        (encontrado,dTipoProducto)=EncTipoProductoID(idTipoProducto)
        nombreTipoProducto=dTipoProducto[1]
        
        op=""
        while op!="0":
            print(
                "QUE DATO DESEA EDITAR: \n"
                "1. Nombre: ("+nombre+")\n"
                "2. Descripcion: ("+desc+")\n"
                "3. Stock: ("+str(stock)+")\n"
                "4. Estatus: ("+str(estatus)+")\n"
                "5. Precio: ("+str(precio)+")\n"
                "6. Tipo de Producto: ("+str(idTipoProducto)+"-"+nombreTipoProducto+")\n"
                "0. Salir"
            )
            op=input("Ingrese una opción: ")
            
            if op=="1":
                nombre=input("Ingrese el nuevo nombre: (anterior: "+nombre+")")
            elif op=="2":
                desc=input("Ingrese la nueva descripcion: (anterior: "+desc+")")
            elif op=="3":
                stock=input("Ingrese el nuevo numero de stock del producto: (anterior: "+str(stock)+")")
            elif op=="4":
                tipoEstatus=""
                if estatus==1:
                    tipoEstatus="Activo"
                else:
                    tipoEstatus="Inactivo"
                    
                estatus=input("Ingrese el nuevo estatus: (anterior: "+tipoEstatus+")\n"
                            "1. Activo\n"
                            "0. Inactivo\n")
            elif op=="5":
                precio=input("Ingrese el nuevo precio: (anterior: "+str(precio)+")")
                
            elif op=="6":
                vistaTipoProducto()
                (encontrado,dTipoProducto)=EncTipoProductoID(idTipoProducto)
                nombreTipoProducto=dTipoProducto[1]
                idTipoProducto=input("Ingrese el nuevo id del tipo de producto: (anterior: "+str(idTipoProducto)+")")
            
            try:
                con=establecer_conexion()
                if con is None:
                    print("No se logró establecer la conexión con la base de datos")
                else:
                    cursor=con.cursor()
                    cursor.callproc("DBMS_OUTPUT.ENABLE")
                    cursor.callproc("SP_EditarProducto",[str(idProducto),nombre,desc,str(stock),str(estatus),precio,str(idTipoProducto)])
                    # Recuperar los mensajes de salida
                    status_var = cursor.var(cx_Oracle.NUMBER)
                    line_var = cursor.var(cx_Oracle.STRING)
                    while True:
                        cursor.callproc('DBMS_OUTPUT.GET_LINE', (line_var, status_var))
                        if status_var.getvalue() != 0:
                            break
                        print(line_var.getvalue())
                    con.commit()
            except Exception as ex:
                print(ex)
            finally:
                if con:
                    con.close()
# editarProducto()

def eliminarProductos():
    vistaProductos()
    
    op=""
    while op=="":
        op=input("Ingrese el id del producto a eliminar o 'S' para SALIR:")
    
    if op.upper()!="S":
        try:
            con=establecer_conexion()
            cursor=con.cursor()
            cursor.callproc("DBMS_OUTPUT.ENABLE")
            cursor.callproc("SP_EliminarProducto",[str(op)])
            #recuperar los mensajes de salida
            status_var = cursor.var(cx_Oracle.NUMBER)
            line_var = cursor.var(cx_Oracle.STRING)
            while True:
                cursor.callproc('DBMS_OUTPUT.GET_LINE', (line_var, status_var))
                if status_var.getvalue() != 0:
                    break
                print(line_var.getvalue())
            con.commit()
        except Exception as ex:
            print(ex)
        finally:
            if con:
                con.close()
# eliminarProducto()

def verProductosPorTipo():
    vistaTipoProducto()
    idTipoProducto=""
    while idTipoProducto=="":
        idTipoProducto=input("\nIngrese el id del tipo de producto: ")
    
    try:
        con=establecer_conexion()
        if con is None:
            print("No se logró establecer la conexión con la base de datos")
        else:
            cursor=con.cursor()
            cursor.callproc("DBMS_OUTPUT.ENABLE")
            cursor.callproc("SP_verProductosTipo",[str(idTipoProducto)])
            # Recuperar los mensajes de salida
            status_var = cursor.var(cx_Oracle.NUMBER)
            line_var = cursor.var(cx_Oracle.STRING)
            while True:
                cursor.callproc('DBMS_OUTPUT.GET_LINE', (line_var, status_var))
                if status_var.getvalue() != 0:
                    break
                print(line_var.getvalue())
            con.commit()
    except Exception as ex:
        print(ex)
    finally:
        if con:
            con.close()


####################################################### Modulo Compras #######################################################

# Función para mostrar los productos disponibles
def mostrar_productos_disponibles():
    # Establecer la conexión a la base de datos
    connection = establecer_conexion()
    try:
        # Consulta para obtener los productos disponibles desde la vista
        cursor = connection.cursor()
        cursor.execute("""SELECT "ID", "NOMBRE", "DESCRIPCION", "PRECIO"
                        FROM Vista_LeerProductos v
                        WHERE v."ESTATUS" = 1""")
        
        # Hacer commit para asegurarse de refrescar los datos en la vista
        connection.commit()
        
        # Mostrar los productos disponibles al cliente
        print("-- Datos de los productos disponibles --")
        print("-------------------------------------")

        # Configurar el tamaño del conjunto de resultados a "all" para leer todos los registros
        rows = cursor.fetchall()

        for row in rows:
            print(f"ID: {row[0]}, Nombre: {row[1]}, Descripción: {row[2]}, Precio: {row[3]}")
        print("-------------------------------------")
        cursor.close()
    except cx_Oracle.DatabaseError as e:
        print("Error al obtener los datos de la vista Vista_LeerProductos:", e)
    finally:
        if connection:
            # Cerrar la conexión
            connection.close()

def mostrar_resumen_compras():
    try:
        # Establecer la conexión a la base de datos
        connection = establecer_conexion()

        # Ejecutar la consulta para obtener el resumen de compras
        cursor = connection.cursor()
        cursor.execute("SELECT IDCOMPRA, NUMEROTRACKING, \"Cliente\", CORREO, \"CANTIDAD PRODUCTOS\", PRECIOTOTAL FROM resumen_compras")

        # Mostrar los resultados
        print("\n--- Resumen de Compras ---")
        for compra in cursor:
            print(f"ID de Compra: {compra[0]}")
            print(f"Número de Tracking: {compra[1]}")
            print(f"Cliente: {compra[2]}")
            print(f"Correo del Cliente: {compra[3]}")
            print(f"Cantidad de Productos: {compra[4]}")
            print(f"Precio Total: {compra[5]}")
            print("--------------------------")

    except cx_Oracle.DatabaseError as e:
        print("Error al mostrar el resumen de compras:", e)
        
    finally:
        if connection:
            # Cerrar el cursor y la conexión
            cursor.close()
            connection.close()

def mostrar_resumen_compras_por_estatus(estatus):
    try:
        # Establecer la conexión a la base de datos
        connection = establecer_conexion()

        # Ejecutar la consulta para obtener el resumen de compras
        cursor = connection.cursor()
        cursor.execute(f"SELECT IDCOMPRA, NUMEROTRACKING, \"Cliente\", CORREO, \"CANTIDAD PRODUCTOS\", PRECIOTOTAL FROM resumen_compras WHERE ESTATUS = {estatus}")

        # Mostrar los resultados
        print("\n--- Resumen de Compras ---")
        for compra in cursor:
            print(f"ID de Compra: {compra[0]}")
            print(f"Número de Tracking: {compra[1]}")
            print(f"Cliente: {compra[2]}")
            print(f"Correo del Cliente: {compra[3]}")
            print(f"Cantidad de Productos: {compra[4]}")
            print(f"Precio Total: {compra[5]}")
            print("--------------------------")

    except cx_Oracle.DatabaseError as e:
        print("Error al mostrar el resumen de compras:", e)
        
    finally:
        if connection:
            # Cerrar el cursor y la conexión
            cursor.close()
            connection.close()

# Función para realizar una compra
def realizar_compra():
    # Establecer la conexión a la base de datos
    connection = establecer_conexion()

    try:
        # Pedir al usuario los datos para realizar la compra
        while True:
            VerUsuarios()
            id_usuario = input("Ingrese el ID del usuario que realiza la compra (Escriba 'q' para salir): ")
            if id_usuario.lower() == 'q':
                print("Operación cancelada.")
                return menu_compras()
            elif not id_usuario.isdigit():
                print("Error: Ingrese un valor numérico válido.")
            else:
                id_usuario = int(id_usuario)
                break

        while True:
            num_productos = input("Ingrese el número de productos que desea comprar (Escriba 'q' para salir): ")
            if num_productos.lower() == 'q':
                print("Operación cancelada.")
                return
            elif not num_productos.isdigit():
                print("Error: Ingrese un valor numérico válido.")
            else:
                num_productos = int(num_productos)
                break

        productos = []
        cantidades = []

        for i in range(num_productos):
            while True:
                vistaProductos()
                id_producto = input(f"Ingrese el ID del producto {i+1} (Escriba 'q' para salir): ")
                if id_producto.lower() == 'q':
                    print("Operación cancelada.")
                    return menu_compras()
                elif not id_producto.isdigit():
                    print("Error: Ingrese un valor numérico válido.")
                else:
                    id_producto = int(id_producto)
                    break

            while True:
                cantidad = input(f"Ingrese la cantidad del producto {i+1} (Escriba 'q' para salir): ")
                if cantidad.lower() == 'q':
                    print("Operación cancelada.")
                    return menu_compras()
                elif not cantidad.isdigit():
                    print("Error: Ingrese un valor numérico válido.")
                else:
                    cantidad = int(cantidad)
                    break

            productos.append(id_producto)
            cantidades.append(cantidad)

        # Convertir las listas de Python a un objeto SYS.ODCINUMBERLIST de Oracle
        productos_array = connection.cursor().arrayvar(cx_Oracle.NUMBER, productos)
        cantidades_array = connection.cursor().arrayvar(cx_Oracle.NUMBER, cantidades)

        # Llamar al procedimiento RealizarCompra del paquete PKG_Compras
        cursor = connection.cursor()
        cursor.callproc("PKG_Compras.RealizarCompra", [id_usuario, productos_array, cantidades_array])
        cursor.close()
        connection.commit()

        print("¡Compra realizada con éxito!")

    except ValueError:
        print("Error: Ingrese un valor numérico válido.")
    except cx_Oracle.DatabaseError as e:
        print("Error al realizar la compra:", e)
        
    finally:
        if connection:
            # Cerrar la conexión
            connection.close()

# Procedimiento para agregar un producto a una compra existente
def agregar_producto_a_compra():
    try:
        # Establecer la conexión a la base de datos
        connection = establecer_conexion()

        # Mostrar productos disponibles
        mostrar_resumen_compras()
        print("\n****************************************************************")
        print("****************************************************************\n")
        mostrar_productos_disponibles()

        # Pedir al usuario los datos para agregar un producto a una compra
        while True:
            id_compra = input("Ingrese el ID de la compra existente (Escriba 'q' para cancelar): ")
            if id_compra.lower() == 'q':
                print("Operación cancelada.")
                return menu_compras()
            elif not id_compra.isdigit():
                print("Error: Ingrese un valor numérico válido.")
            else:
                id_compra = int(id_compra)
                break

        while True:
            id_producto = input("Ingrese el ID del producto a agregar (Escriba 'q' para cancelar): ")
            if id_producto.lower() == 'q':
                print("Operación cancelada.")
                return menu_compras()
            elif not id_producto.isdigit():
                print("Error: Ingrese un valor numérico válido.")
            else:
                id_producto = int(id_producto)
                break

        while True:
            cantidad = input("Ingrese la cantidad del producto a agregar (Escriba 'q' para cancelar): ")
            if cantidad.lower() == 'q':
                print("Operación cancelada.")
                return menu_compras()
            elif not cantidad.isdigit():
                print("Error: Ingrese un valor numérico válido.")
            else:
                cantidad = int(cantidad)
                break

        # Llamar al procedimiento AgregarProductoACompra del paquete PKG_Compras
        cursor = connection.cursor()
        cursor.callproc("PKG_Compras.AgregarProductoACompra", [id_compra, id_producto, cantidad])
        cursor.close()
        connection.commit()

        print("Producto agregado a la compra exitosamente.")

    except ValueError:
        print("Error: Ingrese un valor numérico válido.")
    except cx_Oracle.DatabaseError as e:
        print("Error al agregar el producto a la compra:", e)
        
    finally:
        if connection:
            # Cerrar la conexión
            connection.close()

# Función para obtener el detalle de una compra
def obtener_detalle_compra():
    try:
        mostrar_resumen_compras_por_estatus(0)

        # Pedir al usuario el ID de la compra para obtener su detalle
        while True:
            id_compra = input("Ingrese el ID de la compra (Escriba 'q' para cancelar): ")
            if id_compra.lower() == 'q':
                print("Operación cancelada.")
                return menu_compras()
            elif not id_compra.isdigit():
                print("Error: Ingrese un valor numérico válido.")
            else:
                id_compra = int(id_compra)
                break

        # Establecer la conexión a la base de datos
        connection = establecer_conexion()

        # Crear un cursor para llamar al procedimiento ObtenerDetalleCompra del paquete PKG_Compras
        cursor = connection.cursor()

        # Habilitar el modo "serveroutput"
        cursor.callproc("dbms_output.enable")

        # Llamar al procedimiento ObtenerDetalleCompra del paquete PKG_Compras
        cursor.callproc("PKG_Compras.ObtenerDetalleCompra", [id_compra])
        print("\n")

        # Obtener los mensajes de salida del procedimiento y mostrarlos
        status_var = cursor.var(cx_Oracle.NUMBER)
        line_var = cursor.var(str)
        while True:
            cursor.callproc("dbms_output.get_line", (line_var, status_var))
            if status_var.getvalue() != 0:
                break
            print(line_var.getvalue())
        print("\n")
        # Cerrar el cursor y confirmar la transacción
        cursor.close()
        connection.commit()

    except ValueError:
        print("Error: Ingrese un valor numérico válido.")
    except cx_Oracle.DatabaseError as e:
        print("Error al obtener el detalle de la compra:", e)
    finally:
        if connection:
            # Cerrar la conexión
            connection.close()

# Función para obtener el total de compras por usuario
def obtener_total_compras_usuario():
    try:
        # Establecer la conexión a la base de datos
        connection = establecer_conexion()
        VerUsuarios()
        
        # Pedir al usuario el ID del usuario para obtener el total de compras
        while True:
            id_usuario_input = input("\nIngrese el ID del usuario (Escriba 'q' para cancelar): ")
            if id_usuario_input.lower() == 'q':
                print("Operación cancelada.")
                return menu_compras()
            elif not id_usuario_input.isdigit():
                print("Error: Ingrese un valor numérico válido.")
            else:
                id_usuario = int(id_usuario_input)
                break

        

        # Obtener los datos del cliente
        cursor = connection.cursor()
        cursor.execute("SELECT nombre, primapellido, segapellido, correo FROM Usuario WHERE idUsuario = :id_usuario", id_usuario=id_usuario)
        datos_cliente = cursor.fetchone()
        
        if datos_cliente is None:
            print(f"No se encontró un cliente con el ID {id_usuario}.")
            return

        nombre_cliente = f"{datos_cliente[0]} {datos_cliente[1]} {datos_cliente[2]}"
        correo_cliente = datos_cliente[3]

        # Llamar a la función ObtenerTotalComprasUsuario del paquete PKG_Compras
        total_compras = cursor.callfunc("PKG_Compras.ObtenerTotalComprasUsuario", cx_Oracle.NUMBER, [id_usuario])
        connection.commit()

        print(f"\nDatos del cliente con ID {id_usuario}:")
        print(f"Nombre: {nombre_cliente}")
        print(f"Correo: {correo_cliente}")
        print(f"El total de compras del cliente son: {total_compras}")
    except ValueError:
        print("Error: Ingrese un valor numérico válido.")
    except cx_Oracle.DatabaseError as e:
        print("Error al obtener los datos del cliente y el total de compras:", e)
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

def eliminar_producto_de_compra():
    try:
        # Establecer la conexión a la base de datos
        connection = establecer_conexion()

        while True:
            # Pedir al usuario los datos para eliminar un producto de una compra
            id_compra_input = input("Ingrese el ID de la compra existente (Escriba 'q' para cancelar): ")
            if id_compra_input.lower() == 'q':
                print("Operación cancelada.")
                return menu_compras()
            elif not id_compra_input.isdigit():
                print("Error: Ingrese un valor numérico válido.")
            else:
                id_compra = int(id_compra_input)
                break

        while True:
            id_producto_input = input("Ingrese el ID del producto a eliminar (Escriba 'q' para cancelar): ")
            if id_producto_input.lower() == 'q':
                print("Operación cancelada.")
                return menu_compras()
            elif not id_producto_input.isdigit():
                print("Error: Ingrese un valor numérico válido.")
            else:
                id_producto = int(id_producto_input)
                break

        # Llamar al procedimiento EliminarProductoDeCompra del paquete PKG_Compras
        cursor = connection.cursor()
        cursor.callproc("PKG_Compras.EliminarProductoDeCompra", [id_compra, id_producto])
        connection.commit()

        print("Producto eliminado de la compra exitosamente.")

    except ValueError:
        print("Error: Ingrese un valor numérico válido.")
    except cx_Oracle.DatabaseError as e:
        print("Error al eliminar el producto de la compra:", e)
        
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

def compras():
    try:
        # Establecer la conexión a la base de datos
        connection = establecer_conexion()

        # Ejecutar la consulta para obtener el resumen de compras
        cursor = connection.cursor()
        cursor.execute("SELECT IDCOMPRA, NUMEROTRACKING, \"Cliente\", PRECIOTOTAL, ESTATUS FROM resumen_compras")

        # Mostrar los resultados
        print("\n--- Resumen de Compras ---")
        for compra in cursor:
            print(f"ID de Compra: {compra[0]}")
            print(f"Número de Tracking: {compra[1]}")
            print(f"Cliente: {compra[2]}")
            print(f"Precio Total: {compra[3]}")
            print(f"STATUS: {compra[4]}")
            print("--------------------------")
            print("")
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()



def obtener_total_productos_compra():
    try:
        # Establecer la conexión a la base de datos
        connection = establecer_conexion()

        compras()

        while True:
            # Pedir al usuario el ID de la compra para obtener el total de productos
            id_compra_input = input("Ingrese el ID de la compra (Escriba 'q' para cancelar): ")
            if id_compra_input.lower() == 'q':
                print("Operación cancelada.")
                return menu_compras()
            elif not id_compra_input.isdigit():
                print("Error: Ingrese un valor numérico válido.")
            else:
                id_compra = int(id_compra_input)
                break

        # Llamar a la función ObtenerTotalProductosCompra del paquete PKG_Compras
        cursor = connection.cursor()
        total_productos = cursor.callfunc("PKG_Compras.ObtenerTotalProductosCompra", cx_Oracle.NUMBER, [id_compra])
        connection.commit()

        print(f"El total de productos en la compra con ID {id_compra} son: {total_productos}")

    except ValueError:
        print("Error: Ingrese un valor numérico válido.")
    except cx_Oracle.DatabaseError as e:
        print("Error al obtener el total de productos en la compra:", e)
        
    finally:
        if connection:
            # Cerrar el cursor y la conexión
            cursor.close()
            connection.close()

def mostrar_posibles_estatus():
    print("Posibles estatus:")
    print("0 = pendiente")
    print("1 = en proceso")
    print("2 = revisión")
    print("3 = entregado")
    print("4 = cancelado")

def actualizar_estatus_compra():
    try:
        # Establecer la conexión a la base de datos
        connection = establecer_conexion()

        # Mostrar el resumen de compras
        mostrar_resumen_compras()

        while True:
            # Pedir al usuario el ID de la compra para actualizar el estatus
            id_compra_input = input("Ingrese el ID de la compra (Escriba 'q' para cancelar): ")
            if id_compra_input.lower() == 'q':
                print("Operación cancelada.")
                return menu_compras()
            elif not id_compra_input.isdigit():
                print("Error: Ingrese un valor numérico válido.")
            else:
                id_compra = int(id_compra_input)
                break

        # Mostrar los posibles estatus
        mostrar_posibles_estatus()

        while True:
            # Pedir al usuario el nuevo estatus
            nuevo_estatus_input = input("Ingrese el nuevo estatus de la compra (0-3): ")
            if nuevo_estatus_input.lower() == 'q':
                print("Operación cancelada.")
                return menu_compras()
            elif not nuevo_estatus_input.isdigit() or int(nuevo_estatus_input) < 0 or int(nuevo_estatus_input) > 3:
                print("Error: Ingrese un valor numérico válido entre 0 y 3.")
            else:
                nuevo_estatus = int(nuevo_estatus_input)
                break

        # Llamar al procedimiento ActualizarEstatusCompra del paquete PKG_Compras
        cursor = connection.cursor()
        cursor.callproc("PKG_Compras.ActualizarEstatusCompra", [id_compra, nuevo_estatus])
        connection.commit()

        print(f"Estatus de la compra con ID {id_compra} actualizado correctamente.")

    except ValueError:
        print("Error: Ingrese un valor numérico válido.")
    except cx_Oracle.DatabaseError as e:
        print("Error al actualizar el estatus de la compra:", e)
        
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

def cancelar_compra():
    try:
        # Establecer la conexión a la base de datos
        connection = establecer_conexion()

        # Mostrar el resumen de compras
        mostrar_resumen_compras()

        while True:
            # Pedir al usuario el ID de la compra que desea cancelar
            id_compra_input = input("Ingrese el ID de la compra a cancelar (Escriba 'q' para cancelar): ")
            if id_compra_input.lower() == 'q':
                print("Operación cancelada.")
                return menu_compras()
            elif not id_compra_input.isdigit():
                print("Error: Ingrese un valor numérico válido.")
            else:
                id_compra = int(id_compra_input)
                break

        # Establecer la conexión a la base de datos
        connection = establecer_conexion()

        # Llamar al procedimiento CancelarCompra del paquete PKG_Compras
        cursor = connection.cursor()
        cursor.callproc("PKG_Compras.CancelarCompra", [id_compra])
        connection.commit()

        print(f"Compra con ID {id_compra} cancelada correctamente.")

    except ValueError:
        print("Error: Ingrese un valor numérico válido.")
    except cx_Oracle.DatabaseError as e:
        print("Error al cancelar la compra:", e)
        
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

def consultar_compras_por_estatus():
    try:
        # Mostrar los posibles estatus
        mostrar_posibles_estatus()

        while True:
            # Pedir al usuario el estatus de las compras que desea consultar
            estatus_input = input("Ingrese el estatus de las compras (0-4) que desea consultar (Escriba 'q' para cancelar): ")
            if estatus_input.lower() == 'q':
                print("Operación cancelada.")
                return
            elif not estatus_input.isdigit() or int(estatus_input) not in [0, 1, 2, 3, 4]:
                print("Error: Ingrese un valor numérico válido entre 0 y 4.")
            else:
                estatus = int(estatus_input)
                break

        # Mostrar el resumen de compras por el estatus proporcionado
        mostrar_resumen_compras_por_estatus(estatus)

    except ValueError:
        print("Error: Ingrese un valor numérico válido.")
    except cx_Oracle.DatabaseError as e:
        print("Error al consultar las compras por estatus:", e)

#----------------------------MENUS--------------------------------
def menu_roles():
    op=""
    while op!="0":
        print(
            "\n********** MENU DE ROLES**********\n"
            "1. CREAR ROL\n"
            "2. VER ROLES\n"
            "3. VER ROL ESPECIFICO\n"
            "4. EDITAR ROL\n"
            "5. ELIMINAR ROL\n"
            "0. SALIR\n"
        )
        op=input("Ingrese una opción: ")
        
        if op=="1":
            InsertRol()
        elif op=="2":
            VerRoles()
        elif op=="3":
            verRolEspecifico()
        elif op=="4":
            EditarRol()
        elif op=="5":
            EliminarRol()
        elif op=="0":
            print("\nSaliendo del menú de roles...\n")
            MENU_PRINCIPAL()
        else:
            print("\nOpción no válida. Intente nuevamente.\n")

def menu_usuarios():
    op=""
    while op!="0":
        print(
            "\n********** MENU DE USUARIOS**********\n"
            "1. CREAR USUARIO\n"
            "2. VER USUARIOS\n"
            "3. VER USUARIO ESPECIFICO\n"
            "4. EDITAR USUARIO\n"
            "5. ELIMINAR USUARIO\n"
            "0. SALIR\n"
        )
        op=input("Ingrese una opción: ")
        if op=="1":
            InsertUsuario()
        elif op=="2":
            VerUsuarios()
        elif op=="3":
            VerUsuarioEspecifico()
        elif op=="4":
            ActualizarUsuario()
        elif op=="5":
            eliminar_usuario()
        elif op=="0":
            print("\nSaliendo del menú de usuarios...\n")
            MENU_PRINCIPAL()
        else:
            print("\nOpción no válida. Intente nuevamente.\n")

def menu_tipoServicios():
    op=""
    while op!="0":
        print(
            "\n********** MENU DE TIPO SERVICIOS**********\n"
            "1. CREAR TIPO SERVICIO\n"
            "2. VER TIPO SERVICIO\n"
            "3. VER TIPO SERVICIO ESPECIFICOS\n"
            "4. EDITAR TIPO SERVICIO\n"
            "5. ELIMINAR TIPO SERVICIO\n"
            "0. SALIR\n"
        )
        op=input("Ingrese una opción: ")
        
        if op=="1":
            InsertTipoServicio()
        elif op=="2":
            vistaTipoServicio()
        elif op=="3":
            verTipoServicioEspecifico()
        elif op=="4":
            editarTipoServicio()
        elif op=="5":
            eliminarTipoServicio()
        elif op=="0":
            print("\nSaliendo del menú de tipo servicios...\n")
            MENU_PRINCIPAL()
        else:
            print("\nOpción no válida. Intente nuevamente.\n")

def menu_servicios():
    op=""
    while op!="0":
        print(
                "\n***************** MENU DE SERVICIOS *****************\n"
                "1. CREAR SERVICIO\n"
                "2. VER SERVICIOS\n"
                "3. VER SERVICIO ESPECIFICO\n"
                "4. EDITAR SERVICIO\n"
                "5. ELIMINAR SERVICIO\n"
                "6. VER SERVICIOS POR TIPO\n"
                "0. SALIR\n"
            )
        
        op=input("Ingrese una opción: ")
        if op=="1":
            InsertServicio()
        elif op=="2":
            vistaServicios()
        elif op=="3":
            verServicioEspecifico()
        elif op=="4":
            editarServicio()
        elif op=="5":
            eliminarServicio()
        elif op=="6":
            verServiciosPorTipo()
        elif op=="0":
            print("\nSaliendo del menú de servicios...\n")
            MENU_PRINCIPAL()
        else:
            print("\nOpción no válida. Intente nuevamente.\n")

def menu_tipoProductos():
    op=""
    while op!="0":
        print(
            "\n********** MENU DE TIPO PRODUCTO**********\n"
            "1. CREAR TIPO PRODUCTO\n"
            "2. VER TIPO PRODUCTO\n"
            "3. VER TIPO PRODUCTO ESPECIFICO\n"
            "4. EDITAR TIPO PRODUCTO\n"
            "5. ELIMINAR TIPO PRODUCTO\n"
        )
        op=input("Ingrese una opción: ")
        
        if op=="1":
            InsertTipoProducto()
        elif op=="2":
            vistaTipoProducto()
        elif op=="3":
            verTipoProductoEspecifico()
        elif op=="4":
            editarTipoProducto()
        elif op=="5":
            eliminarTipoProducto()
        elif op=="0":
            print("\nSaliendo del menú de tipo producto...\n")
            MENU_PRINCIPAL()
        else:
            print("\nOpción no válida. Intente nuevamente.\n")

def menu_productos():
    op=""
    while op!="0":
        print(
                "\n***************** MENU DE PRODUCTOS *****************\n"
                "1. CREAR PRODUCTOS\n"
                "2. VER PRODUCTOS\n"
                "3. VER PRODUCTO ESPECIFICO\n"
                "4. EDITAR PRODUCTOS\n"
                "5. ELIMINAR PRODUCTOS\n"
                "6. VER PRODUCTOS POR TIPO\n"
                "0. SALIR\n"
            )
        
        op=input("Ingrese una opción: ")
        if op=="1":
            InsertProducto()
        elif op=="2":
            vistaProductos()
        elif op=="3":
            verProductoEspecifico()
        elif op=="4":
            editarProductos()
        elif op=="5":
            eliminarProductos()
        elif op=="6":
            verProductosPorTipo()
        elif op=="0":
            print("\nSaliendo del menú de productos...\n")
            MENU_PRINCIPAL()
        else:
            print("\nOpción no válida. Intente nuevamente.\n")

def menu_compras():
    op = ""
    while op != "0":
        print(
            "\n********** MENÚ DE COMPRAS **********\n"
            "1. REALIZAR COMPRA\n"
            "2. AGREGAR PRODUCTO A COMPRA EXISTENTE\n"
            "3. ELIMINAR PRODUCTO DE COMPRA EXISTENTE\n"
            "4. ACTUALIZAR STATUS DE COMPRA EXISTENTE\n"
            "5. CANCELAR COMPRA EXISTENTE\n"
            "6. OBTENER TOTAL DE PRODUCTOS EN UNA COMPRA\n"
            "7. OTBENER TOTAL DE COMPRAS POR USUARIO\n"
            "8. OBTENER DETALLE DE COMPRA ESPECIFICA\n"
            "9. CONSULTAR COMPRAS POR STATUS\n"
            "0. SALIR\n"
            "************************************\n"
        )
        op = input("Ingrese una opción:")
        if op == "1":
            realizar_compra()
        elif op == "2":
            agregar_producto_a_compra()
        elif op == "3":
            eliminar_producto_de_compra()
        elif op == "4":
            actualizar_estatus_compra()
        elif op == "5":
            cancelar_compra()
        elif op == "6":
            obtener_total_productos_compra()
        elif op == "7":
            obtener_total_compras_usuario()
        elif op == "8":
            obtener_detalle_compra()
        elif op == "9":
            consultar_compras_por_estatus()
        elif op == "0":
            print("\nSaliendo del menú de compras...\n")
            MENU_PRINCIPAL()
        else:
            print("\nOpción no válida. Intente nuevamente.\n")

def MENU_PRINCIPAL():
    while True:
        op = input(
            "\n********** MENU **********\n"
            "1. ROLES\n"
            "2. USUARIOS\n"
            "3. TIPO PRODUCTO\n"
            "4. PRODUCTOS\n"
            "5. TIPO SERVICIO\n"
            "6. SERVICIOS\n"
            "7. COMPRAS\n"
            "0. SALIR\n"
            "\nIngrese una opción: "
        )
        
        if op == "1":
            menu_roles()
        elif op == "2":
            menu_usuarios()
        elif op == "3":
            menu_tipoProductos()
        elif op == "4":
            menu_productos()
        elif op == "5":
            menu_tipoServicios()
        elif op == "6":
            menu_servicios()
        elif op == "7":
            menu_compras()
        elif op == "0":
            print("\nGracias por usar el sistema.\n")
            sys.exit()
        else:
            print("\nOpción no válida. Intente nuevamente.\n")
#---------------------------MAIN----------------------------------
MENU_PRINCIPAL()
