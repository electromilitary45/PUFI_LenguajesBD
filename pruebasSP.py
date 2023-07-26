import cx_Oracle

##RUTA DEREK
cx_Oracle.init_oracle_client(lib_dir=r"g:\ORACLE\instantclient")

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
            print("Rol insertado con éxito")

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
    try:
        # Traer y mostrar los datos de los roles
        roles = VerRoles()

        # Pedir al usuario seleccionar un número de rol para editar o 'S' para cancelar
        op = input("\nSeleccione el # de rol que desea editar o 'S' para cancelar: ")

        # Si no cancela la operación
        if op != "S":
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

    except Exception as ex:
        print(ex)

    finally:
        if connection:
            connection.close()

def EliminarRol():
    try:
        # Traer y mostrar los datos de los roles
        roles = VerRoles()

        # Pedir al usuario seleccionar un número de rol para eliminar o 'S' para cancelar
        op = input("\nSeleccione el # de rol que desea eliminar o 'S' para cancelar: ")

        # Si no cancela la operación
        if op != "S":
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
                connection = conexion()
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

        idRol = input("Ingrese su rol: \n" + u + "\n")

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
        print("Usuario creado con éxito")

    except Exception as ex:
        print(ex)

    finally:
        if connection:
            connection.close()

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
                   "\n7. Salir"
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

    try:
        connection = establecer_conexion()
        cursor = connection.cursor()

        # SELECT para buscar el usuario según el atributo proporcionado
        query = "SELECT idUsuario, nombre, primApellido, segApellido, cedula, correo FROM usuario WHERE"

        if op == "1":
            query += " idUsuario = :idUsuario"
        elif op == "2":
            query += " nombre = :nombreUsuario"
        elif op == "3":
            query += " primApellido = :apellido1"
        elif op == "4":
            query += " segApellido = :apellido2"
        elif op == "5":
            query += " cedula = :cedulaUsuario"
        elif op == "6":
            query += " correo = :correoUsuario"
        else:
            return

        # Ejecutar la consulta SQL con los parámetros correspondientes
        cursor.execute(query, idUsuario=id, nombreUsuario=nombre, apellido1=Apellido1,
                       apellido2=Apellido2, cedulaUsuario=Cedula, correoUsuario=Correo)

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
        con=establecer_conexion()
        if con is None:
            print("No se logró establecer la conexión con la base de datos en el proceso de inserción")
        else:
            cur=con.cursor()
            cur.callproc("DBMS_OUTPUT.ENABLE")
            cur.execute("SELECT * FROM V_TiposServicio")
            
            # Recuperar los mensajes de salida
            results = cur.fetchall()
            if results:
                print("---Tipos de Servicios Registrados---")
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
# vistaTipoServicio()

def verTipoProductoEspecifico():
    # op=0
    # nombre=""
    # id=0
    # while op!=1 and op!=2:
    #     input("Ingrese 1 para buscar por ID o 2 para buscar por nombre: ")
    
    # if op==1:
    #     id=input("Ingrese el ID del tipo de producto: ")
    # else:
    #     nombre=input("Ingrese el nombre del tipo de producto: ")
    
    # try:
    print("EN DESARRROLLO")

def editarTipoProducto():
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

def eliminarTipoProducto():
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
        con=establecer_conexion()
        if con is None:
            print("No se logró establecer la conexión con la base de datos en el proceso de inserción")
        else:
            cur=con.cursor()
            cur.callproc("DBMS_OUTPUT.ENABLE")
            cur.execute("SELECT * FROM V_Servicios")
            
            # Recuperar los mensajes de salida
            results = cur.fetchall()
            if results:
                print("---Servicios Registrados---")
                print("ID","\tNombre","\tDescripcion","\tCupos","\tEstatus","\tFecha","\tTipoServicio")
                for row in results:
                    print(row[0],"\t",row[1],"\t",row[3],"\t",row[4],"\t",row[5],"\t",row[6],"\t",row[7])
            else:
                print("No hay registros")

    except Exception as ex:
        print(ex)
    finally:
        if con:
            con.close()
# vistaServicios()

def verServicioEspecifico():
    print("EN DESARRROLLO")

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



#----------------------------MENUS--------------------------------
def menu_roles():
    print("EN DESARRROLLO")

def menu_usuarios():
    print("EN DESARRROLLO")

def menu_tipoServicios():
    op=""
    while op!="0":
        print(
            "********** MENU DE TIPO PRODUCTO**********\n"
            "1. CREAR TIPO SERVICIO\n"
            "2. VER TIPO SERVICIO\n"
            "3. VER TIPO SERVICIO ESPECIFICO\n"
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
            verTipoProductoEspecifico()
        elif op=="4":
            editarTipoProducto()
        elif op=="5":
            eliminarTipoProducto()

def menu_servicios():
    op=""
    while op!="0":
        print(
                "***************** MENU DE SERVICIOS *****************\n"
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
# MENU_PRINCIPAL()
