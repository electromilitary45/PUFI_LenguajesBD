import cx_Oracle

##RUTA DEREK
cx_Oracle.init_oracle_client(lib_dir=r"g:\ORACLE\instantclient")

# ------------------ MUDLO ROLES ------------------ #
def rolesDatos():
    try:
        connection=cx_Oracle.connect(
            user='DBADEREK',
            password='Villaley45',
            dsn='localhost:1521/orcl',
            encoding='UTF-8'
        )

        ##print(connection.version)
        cursor=connection.cursor()

        cursor.execute("SELECT * FROM rol")
        results = cursor.fetchall()

        roles=[]
        # print("Número de filas recuperadas:", len(results))
        for row in results:
            roles.append(row)

    except Exception as ex:
        print(ex)

    finally:
        if connection:
            connection.close()
    return roles

def rolesCant():
    try:
        connection=cx_Oracle.connect(
            user='DBADEREK',
            password='Villaley45',
            dsn='localhost:1521/orcl',
            encoding='UTF-8'
        )

        ##print(connection.version)
        cursor=connection.cursor()

        cursor.execute("SELECT * FROM rol")
        results = cursor.fetchall()

    except Exception as ex:
        print(ex)

    finally:
        if connection:
            connection.close()
    return len(results)

def InsertRol():
    # ---- Nombre rol
    nombreRol=""
    while (nombreRol==""):
        nombreRol=input("Ingrese el nombre del rol: ")
    
    try:
        connection=cx_Oracle.connect(
            user='DBADEREK',
            password='Villaley45',
            dsn='localhost:1521/orcl',
            encoding='UTF-8'
        )
        ##coneccion 
        cursor=connection.cursor()
        ## sentencia de insercion de rol
        cursor.execute("INSERT INTO rol (nombre) VALUES('"+nombreRol+"')")
        
        # execute de un sp
        #cursor.callproc("sp_insertar_rol", [nombreRol])
        
        ## commit
        cursor.execute("commit")
        
    except Exception as ex:
        print(ex)
    finally:
        if connection:
            connection.close()
            print("Rol creado con éxito")

def VerRoles():
    try:
        connection=cx_Oracle.connect(
            user='DBADEREK',
            password='Villaley45',
            dsn='localhost:1521/orcl',
            encoding='UTF-8'
        )

        ##print(connection.version)
        cursor=connection.cursor()
        ## sentencia de select de rol
        cursor.execute("SELECT * FROM rol")

        results = cursor.fetchall()

        print("Número de filas recuperadas:", len(results))
        for row in results:
            print(row)

    except Exception as ex:
        print(ex)

    finally:
        if connection:
            connection.close()

def EditarRol():
    #---- TRAIGO LOS DATOS DE LOS ROLES Y LOS GUARDO EN UN VECTOR
    NomRol=rolesDatos()
    
    #---- CONCATENO LOS DATOS DE LOS ROLES EN UN STRING
    sR=""
    for i in NomRol:
        sR=sR+str(i)+"\n"
    
    #---- MUESTRO LOS DATOS DE LOS ROLES Y PIDO QUE SE SELECCIONE UNO
    op=""
    while op=="":
        op=input(sR+"\nSelecione el # de rol que desea editar o 'S' para cancelar:")
    
    #---- SI NO CANCELA LA OPERACION
    if(op!="S"):
        
        #----- BUSCO EL ROL POR ID
        idRol=0
        nombreRol=""
        encontrado=False
        for i in NomRol:
            if(op==str(i[0])):
                idRol=i[0]
                nombreRol=i[1]
                encontrado=True
                break
            
        #---- SI ENCUENTRA EL ROL
        if(encontrado):
            print("Rol seleccionado: "+nombreRol)
            
            #---- PIDO EL NUEVO NOMBRE DEL ROL
            nombreNuevoRol=""
            while (nombreNuevoRol==""):
                nombreNuevoRol=input("Ingrese el nuevo nombre del rol: ")
            
            #---- ACTUALIZO EL ROL
            try:
                connection=cx_Oracle.connect(
                    user='DBADEREK',
                    password='Villaley45',
                    dsn='localhost:1521/orcl',
                    encoding='UTF-8'
                )
                ##coneccion 
                cursor=connection.cursor()
                ## sentencia de update de rol
                cursor.execute("UPDATE rol SET nombre='"+nombreNuevoRol+"' WHERE idRol='"+str(idRol)+"'")
                cursor.execute("commit")
            except Exception as ex:
                print(ex)
            finally:
                if connection:
                    connection.close()
                    print("Rol editado con éxito")
        #---- SI NO ENCUENTRA EL ROL
        else:
            print("ID de rol incorrecto")
    #---- SI CANCELA LA OPERACION
    else:
        print("Operación cancelada")

def EliminarRol():
    #---- TRAIGO LOS DATOS DE LOS ROLES Y LOS GUARDO EN UN VECTOR
    NomRol=rolesDatos()
    
    #---- CONCATENO LOS DATOS DE LOS ROLES EN UN STRING
    sR=""
    for i in NomRol:
        sR=sR+str(i)+"\n"
    
    #---- MUESTRO LOS DATOS DE LOS ROLES Y PIDO QUE SE SELECCIONE UNO
    print("********ROLES*********")
    print(sR)
    
    op=""
    while op=="":
        op=input("Selecione el # de rol que desea eliminar o 'S' para cancelar:")
    
    if(op!="S"):
        #----- BUSCO EL ROL POR ID
        encontrado=False
        for i in NomRol:
            if(op==str(i[0])):
                encontrado=True
                break
            
        if(encontrado):
            #---- TRAIGO LOS DATOS DE LOS ROLES Y LOS GUARDO EN UN VECTOR
            usuarios=VerUsuariosRol(op)
            
            #---- SI EL ROL TIENE USUARIOS ASOCIADOS
            if(len(usuarios)!=0):
                print("El rol tiene usuarios asociados, no se puede eliminar")
            else:
                try:
                    connection=cx_Oracle.connect(
                        user='DBADEREK',
                        password='Villaley45',
                        dsn='localhost:1521/orcl',
                        encoding='UTF-8'
                    )
                    #Conexion
                    cursor=connection.cursor()
                    #---- ELIMINO EL ROL
                    cursor.execute("DELETE FROM rol WHERE idRol='"+str(op)+"'")
                    #---- COMMIT
                    cursor.execute("commit")
                except Exception as ex:
                    print(ex)
                finally:
                    if connection:
                        connection.close()
                        print("Rol eliminado con éxito")

##------------------ MODULOS USUARIOS------------------##

def EncUsuarioID(idUsuario):
    try:
        connection=cx_Oracle.connect(
            user='DBADEREK',
            password='Villaley45',
            dsn='localhost:1521/orcl',
            encoding='UTF-8'
        )
        ##print(connection.version)
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE idUsuario='"+str(idUsuario)+"'")
        results = cursor.fetchall()
        encontrado=False
        dUsuario=[]
        for row in results:
            print(row[0])
            if (str(row[0])==idUsuario):
                dUsuario=row
                encontrado=True
                break

    except Exception as ex:
        print(ex)

    finally:
        if connection:
            connection.close()
    return encontrado,row

def InsertUsuario():
    # DATOS DE USUARIO
    nombre=""
    while (nombre==""):
        nombre=input("Ingrese su nombre: ")
    # ---- APELLIDO 2
    apellido1=""
    while (apellido1==""):
        apellido1=input("Ingrese su Primer Apellido: ")
    # ---- APELLIDO 2
    apellido2=""
    while (apellido2==""):
        apellido2=input("Ingrese su Segundo Apellido: ")
    # ---- CEDULA
    cedula=""
    while (cedula==""):
        cedula=input("Ingrese su cédula: ")
    # ---- CORREO
    correo=""
    while (correo==""):
        correo=input("Ingrese su correo: ")
    contrasenna=input("Ingrese su contraseña: ")
    # ---- ROL
    idRol=""
    encontrado=False
    while (encontrado==False and idRol==""):
        usuarios=rolesDatos()
        
        u=""
        for u in usuarios:
            u=str(u)+"\n"
        
        idRol=input("Ingrese su rol: \n"+u+"\n")
        
        for i in usuarios:
            if (str(i[0])==idRol):
                encontrado=True
                idRol=i[0]
                break
            
        if (encontrado==False):
            print("Rol no encontrado/nReintente nuevamente")
    # ---- DIRECCION
    idDireccion=0

    try:
        connection=cx_Oracle.connect(
            user='DBADEREK',
            password='Villaley45',
            dsn='localhost:1521/orcl',
            encoding='UTF-8'
        )
        ##coneccion 
        cursor=connection.cursor()
        ## sentencia de insercion de usuario
        cursor.execute("INSERT INTO usuario (nombre,primapellido,segapellido,cedula,correo,contrasenna,idRol,idDireccion) VALUES('"+nombre+"', '"+apellido1+"', '"+apellido2+"', '"+cedula+"', '"+correo+"', '"+contrasenna+"', '"+str(idRol)+"', '"+str(idDireccion)+"')")
        cursor.execute("commit")
        print("Usuario creado con éxito")
    except Exception as ex:
        print(ex)
    finally:
        if connection:
            connection.close()

def VerUsuarios():
    try:
        connection=cx_Oracle.connect(
            user='DBADEREK',
            password='Villaley45',
            dsn='localhost:1521/orcl',
            encoding='UTF-8'
        )

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

def VerUsuarioEspecifico():
    
    op=""
    id=""
    nombre=""
    Apellido1=""
    Apellido2=""
    Cedula=""
    Correo=""
    
    
    
    while op=="":
        op=input("Con cual dato quiere buscar el usuario:"
                "\n1. ID"
                "\n2. Nombre"
                "\n3. Apellido1"
                "\n4. Apellido2"
                "\n5. Cedula"
                "\n6. Correo"
                "\n7. Salir"
                )
        
        if op=="1":
            while id=="": 
                id=input("Ingrese el id del usuario: ")
        elif op=="2":
            while nombre=="":
                nombre=input("Ingrese el nombre del usuario: ")
        elif op=="3":
            while Apellido1=="":
                Apellido1=input("Ingrese el primer apellido del usuario: ")
        elif op=="4":
            while Apellido2=="":
                Apellido2=input("Ingrese el segundo apellido del usuario: ")
        elif op=="5":
            while Cedula=="":
                Cedula=input("Ingrese la cedula del usuario: ")
        elif op=="6":
            while Correo=="":
                Correo=input("Ingrese el correo del usuario: ")

    try:
        connection=cx_Oracle.connect(
            user='DBADEREK',
            password='Villaley45',
            dsn='localhost:1521/orcl',
            encoding='UTF-8'
        )

        ##print(connection.version)
        cursor=connection.cursor()
        
        # --- SELECT POR ID ----
        if op=="1":
            cursor.execute("SELECT * FROM usuario WHERE idUsuario='"+str(id)+"'")
        # --- SELECT POR NOMBRE
        elif op=="2":
            cursor.execute("SELECT * FROM usuario WHERE nombre='"+str(nombre)+"'")
        # --- SELECT POR APELLIDO 1
        elif op=="3":
            cursor.execute("SELECT * FROM usuario WHERE primApellido='"+str(Apellido1)+"'")
        # --- SELECT POR APELLIDO 2
        elif op=="4":
            cursor.execute("SELECT * FROM usuario WHERE segApellido='"+str(Apellido2)+"'")
        # --- SELECT POR CEDULA
        elif op=="5":
            cursor.execute("SELECT * FROM usuario WHERE cedula='"+str(Cedula)+"'")
        # --- SELECT POR CORREO
        elif op=="6":
            cursor.execute("SELECT * FROM usuario WHERE correo='"+str(Correo)+"'")

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
    
    #pide el id del usuario a actualizar
    idUsuario=""

    while (idUsuario==""):
        idUsuario=input("Ingrese el id del usuario a actualizar: ")
    dUsuario=[]
    #se buscar el usuario por id
    (encontrado,dUsuario)=EncUsuarioID(idUsuario)
    
    if(encontrado):
        
        idUsuario=dUsuario[0]
        nombre=dUsuario[1]
        primApellido=dUsuario[2]
        segApellido=dUsuario[3]
        cedula=dUsuario[4]
        correo=dUsuario[5]
        contrasenna=dUsuario[6]
        idRol=dUsuario[7]
        idDireccion=dUsuario[8]

        nombre2=""
        primApellido2=""
        segApellido2=""
        cedula2=""
        correo2=""
        contrasenna2=""
        idRol2=""
        idDireccion2=""
        
        op=""
        while (str(op)!="0"):
            print(
                "QUE DATO DESEA EDITAR: \n"
                "1. Nombre: ("+nombre+")\n"
                "2. Primer Apellido: ("+primApellido+")\n"
                "3. Segundo Apellido: ("+segApellido+")\n"
                "4. Cedula: ("+str(cedula)+")\n"
                "5. Correo: ("+correo+")\n"
                "6. Contraseña: ("+contrasenna+")\n"
                "7. Rol: ("+str(idRol)+")\n"
                "8. Direccion: ("+str(idDireccion)+")\n"
                "0. Salir"
            )
            op=input("Ingrese una opción: ")
            
            if op=="1":
                # while (nombre2=="" or nombre2==nombre):
                nombre=input("Ingrese el nuevo nombre: ")
            elif op=="2":
                # while (primApellido2=="" and primApellido2==primApellido):
                primApellido=input("Ingrese el nuevo primer apellido: ")
            elif op=="3":
                # while (segApellido2=="" and segApellido2==segApellido):
                segApellido=input("Ingrese el nuevo segundo apellido: ")
            elif op=="4":
                # while (cedula2=="" and cedula2==cedula):
                cedula=input("Ingrese la nueva cedula: ")
            elif op=="5":
                # while (correo2=="" and correo2==correo):
                correo=input("Ingrese el nuevo correo: ")
            elif op=="6":
                # while (contrasenna2=="" and contrasenna2==contrasenna):
                contrasenna=input("Ingrese la nueva contraseña: ")
            elif op=="7":
                # while (idRol2=="" and idRol2==idRol):
                VerRoles()
                idRol=input("Ingrese el nuevo rol: ")
            # elif op=="8":
            #     while (idDireccion2=="" and idDireccion2==idDireccion):
            #         idDireccion2=input("Ingrese la nueva direccion: ")

            try:
                connection=cx_Oracle.connect(
                    user='DBADEREK',
                    password='Villaley45',
                    dsn='localhost:1521/orcl',
                    encoding='UTF-8'
                )
                ##coneccion 
                cursor=connection.cursor()
                ## sentencia de update de rol
                cursor.execute("UPDATE usuario SET nombre='"+nombre+"',primApellido='"+primApellido+"',segApellido='"+segApellido+"',cedula='"+cedula+"',correo='"+correo+"',idRol='"+str(idRol)+"', idDireccion='"+str(idDireccion)+"' WHERE idUsuario='"+str(idUsuario)+"'")
                
                cursor.execute("commit")
                
            except Exception as ex:
                print(ex)
            finally:
                if connection:
                    connection.close()
                    print("Usuario editado con éxito")
    else:
        print("Usuario no encontrado")

def DesactivarUsuario():
    print("OPCIÓN EN DESARROLLO")

def VerUsuariosRol(idRol):
    try:
        connection=cx_Oracle.connect(
            user='DBADEREK',
            password='Villaley45',
            dsn='localhost:1521/orcl',
            encoding='UTF-8'
        )

        ##print(connection.version)
        cursor=connection.cursor()

        cursor.execute("SELECT * FROM usuario WHERE idRol='"+str(idRol)+"'")
        results = cursor.fetchall()
        usuarios=[]
        
        for row in results:
            usuarios.append(row)
        
    except Exception as ex:
        print(ex)

    finally:
        if connection:
            connection.close()
    return usuarios

##----------------- MODULO TIPO PRODUCTO -----------------## 

def insertarTipoProducto():
    ## ---- NOMBRE TIPO PRODUCTO
    nombre=""
    while (nombre==""):
        nombre=input("Ingrese el nombre del tipo de producto: ")
    ## --- DESCRIPCION TIPO PRODUCTO
    desc=""
    while (desc==""):
        desc=input("Ingrese la descripcion del tipo de producto: ")
    
    try:
        connection=cx_Oracle.connect(
            user='DBADEREK',
            password='Villaley45',
            dsn='localhost:1521/orcl',
            encoding='UTF-8'
        )
        ##coneccion 
        cursor=connection.cursor()
        ## sentencia de insercion de rol
        cursor.execute("INSERT INTO TipoProducto (nombre,descripcion) VALUES('"+nombre+"','"+desc+"')")
        
        # execute de un sp
        #cursor.callproc("sp_insertar_rol", [nombreRol])
        
        ## commit
        cursor.execute("commit")
        
    except Exception as ex:
        print(ex)
    finally:
        if connection:
            connection.close()
            print("Tipo de producto "+nombre+" creado con éxito")

def verTipoProducto():
    print("OPCIÓN EN DESARROLLO")

def editarTipoProducto():
    print("OPCIÓN EN DESARROLLO")

def verTipoProductoEspecifico():
    print("OPCIÓN EN DESARROLLO")

def eliminarTipoProducto():
    print("OPCIÓN EN DESARROLLO")


##------------------ MODULOS PRODUCTOS------------------##

def CrearProducto():
    # ---- NOMBRE PRODUCTO
    nombre=""
    while (nombre==""):
        nombre=input("Ingrese el nombre del producto: ")
    # ---- DESCRIPCION
    descripcion=""
    while (descripcion==""):
        descripcion=input("Ingrese la descripcion del producto: ")
    # ---- PRECIO
    precio=""
    while (precio==""):
        precio=input("Ingrese el precio del producto: ")
    # ---- STOCK
    stock=""
    while (stock==""):
        stock=input("Ingrese el stock del producto: ")
    # ---- idTipoProducto
    idTipoProducto=""
    while (idTipoProducto==""):
        idTipoProducto=input("Ingrese el idTipoProducto del producto: ")

def VerProductos():
    try:
        connection=cx_Oracle.connect(
            user='DBADEREK',
            password='Villaley45',
            dsn='localhost:1521/orcl',
            encoding='UTF-8'
        )

        ##print(connection.version)
        cursor=connection.cursor()

        cursor.execute("SELECT * FROM TipoUsuario")
        results = cursor.fetchall()

        print("Número de filas recuperadas:", len(results))
        for row in results:
            print(row)

    except Exception as ex:
        print(ex)

    finally:
        if connection:
            connection.close()

def EditarProducto():
    print("OPCIÓN EN DESARROLLO")

def VerProductoEspecifico():
    print("OPCIÓN EN DESARROLLO")


##------------------ MODULOS PEDIDOS------------------##


##------------------ MENUS------------------##
def MENUROLES():
    op=""
    while op!="0":
        print(
            "********** MENU DE ROLES**********\n"
            "1. CREAR ROL\n"
            "2. VER ROLES\n"
            "3. EDITAR ROL\n"
            "4. ELIMINAR ROL\n"
            "0. SALIR\n"
        )
        op=input("Ingrese una opción: ")
        if op=="1":
            InsertRol()
        elif op=="2":
            VerRoles()
        elif op=="3":
            EditarRol()
        elif op=="4":
            EliminarRol()

def MENUUSUARIOS():
    op=""
    while op!="0":
        print(
            "********** MENU DE USUARIOS**********\n"
            "1. CREAR usuarios\n"
            "2. VER usuarios\n"
            "3. VER usuario especifico\n"
            "4. ACTUALIZAR usuario\n"
            "5. DESACTIVAR usuario\n"
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
            DesactivarUsuario()

def MENUTIPOPRODUCTO():
    op=""
    while op!="0":
        input(
            "********** MENU DE TIPO PRODUCTO**********\n"
            "1. CREAR TIPO PRODUCTO\n"
            "2. VER TIPO PRODUCTO\n"
            "3. VER TIPO PRODUCTO ESPECIFICO\n"
            "4. EDITAR TIPO PRODUCTO\n"
            "0. SALIR\n"
            "Ingrese una opción:"
        )
        
        if op=="1":
            insertarTipoProducto()
        elif op=="2":
            verTipoProducto()

def MENUPRODUCTOS():
    op=""
    while op!="0":
        print(
            "********** MENU DE PRODUCTOS**********\n"
            "1. CREAR PRODUCTO\n"
            "2. VER PRODUCTOS\n"
            "3. VER PRODUCTO ESPECIFICO\n"
            "4. EDITAR PRODUCTO\n"
            "0. SALIR\n"
        )
        op=input("Ingrese una opción: ")
        if op=="1":
            CrearProducto()
        elif op=="2":
            VerProductos()
        elif op=="3":
            VerProductoEspecifico()
        elif op=="4":
            EditarProducto()

def MENUPRINCIPAL():
    op=""
    while op!="0":
        op=input(
            "********** MENU **********\n"
            "1. ROLES\n"
            "2. USUARIOS\n"
            "3. TIPO PRODUCTO\n"
            "4. PRODUCTOS\n"
            "0. SALIR\n"
            "Ingrese una opción:"
        )
        
        if op=="1":
            MENUROLES()
        elif op=="2":
            MENUUSUARIOS()
        elif op=="3":
            MENUTIPOPRODUCTO()
        elif op=="4":
            MENUPRODUCTOS()


# -----PROGRAMA PRINCIPAL-----
MENUPRINCIPAL()