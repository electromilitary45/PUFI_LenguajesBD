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
##InsertRol()

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
                connection=establecer_conexion()
                cursor=connection.cursor()
                cursor.execute("UPDATE TipoServicio SET nombre='"+nombre+"',descripcion='"+desc+"' WHERE idTipoServicio='"+str(idTipoServicio)+"'")
                cursor.execute("commit")
            except Exception as ex:
                print(ex)
            finally:
                if connection:
                    connection.close()
                    print("Tipo de servicio editado con éxito")
                    
    else:
        print("Tipo de servicio no encontrado")

def eliminarTipoProducto():
    print("EN DESARRROLLO")

#-------------------------MODULO SERVICIOS-------------------------
def InsertServicio():
    print ("EN DESARROLLO")
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

def verServicioEspecifico():
    print("EN DESARRROLLO")

def editarServicio():
    print("EN DESARRROLLO")

def eliminarServicio():
    print("EN DESARRROLLO")

def verServiciosPorTipo():
    print("EN DESARRROLLO")




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
        print("***************** MENU DE SERVICIOS *****************\n"
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
