import cx_Oracle

##RUTA DEREK
cx_Oracle.init_oracle_client(lib_dir=r"g:\ORACLE\instantclient")

def conexion():
    try:
        connection=cx_Oracle.connect(
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
def rolesDatos(): 
    try:
        connection=conexion()

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
        connection=conexion()

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
        connection=conexion()
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
        connection=conexion()

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
                connection=conexion()
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
                    connection=conexion()
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
        connection=conexion()
        ##print(connection.version)
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE idUsuario='"+str(idUsuario)+"'")
        results = cursor.fetchall()
        encontrado=False
        dUsuario=[]
        for row in results:
            if (str(row[0])==idUsuario):
                dUsuario=row
                encontrado=True
                break

    except Exception as ex:
        print(ex)

    finally:
        if connection:
            connection.close()
    return encontrado,dUsuario

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
        connection=conexion()
        ##coneccion 
        cursor=connection.cursor()
        ## sentencia de insercion de usuario
        cursor.execute("INSERT INTO usuario (nombre,primapellido,segapellido,cedula,correo,contrasenna,idRol,idDireccion) VALUES('"+nombre+"', '"+apellido1+"', '"+apellido2+"', '"+cedula+"', '"+correo+"', '"+contrasenna+"', '"+str(idRol)+"', '"+str(idDireccion)+"')")
        
        # execute de sp crear usuario
        # cursor.callproc("sp_insertar_usuario", [nombre,apellido1,apellido2,cedula,correo,contrasenna,idRol,idDireccion])
        
        
        
        cursor.execute("commit")
        print("Usuario creado con éxito")
    except Exception as ex:
        print(ex)
    finally:
        if connection:
            connection.close()

def VerUsuarios():
    try:
        connection=conexion()
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
        connection=conexion()

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
                connection=conexion()
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
        connection=conexion()

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
def tipoProductoDatos():
    try:
        connection=conexion()
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
        connection=conexion()
        
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
        connection=conexion()
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
    try:
        connection=conexion()
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM TipoProducto")
        results = cursor.fetchall()
        
        print("Número de filas recuperadas:", len(results))
        for row in results:
            print(row)
    except Exception as ex:
        print(ex)
    
    finally:
        if connection:
            connection.close()

def editarTipoProducto():
    print("*************TIPO PRODUCTO*************")
    verTipoProducto()
    print("****************************************")
    
    #pide el id del tipo de producto a actualizar
    idTipoProducto=""
    dTipoProducto=[]
    
    while (idTipoProducto==""):
        idTipoProducto=input("Ingrese el id del tipo de producto a actualizar: ")

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
                connection=conexion()
                cursor=connection.cursor()
                cursor.execute("UPDATE TipoProducto SET nombre='"+nombre+"',descripcion='"+desc+"' WHERE idTipoProducto='"+str(idTipoProducto)+"'")
                cursor.execute("commit")
            except Exception as ex:
                print(ex)
            finally:
                if connection:
                    connection.close()
                    print("Tipo de producto editado con éxito")
                    
    else:
        print("Tipo de producto no encontrado")

def verTipoProductoEspecifico():
    print("OPCIÓN NO DISPONIBLE")
    # op=""
    # id=""
    # nombre=""
    # desc=""
    
    # while op!="0":
    #     op=input(
    #         "Con cual dato quiere buscar el tipo de producto:"
    #         "\n1. ID"
    #         "\n2. Nombre"
    #         "\n0. Salir"
    #     )
        
    #     if op=="1":
    #         while id=="":
    #             id=input("Ingrese el id del tipo de producto: ")
    #     elif op=="2":
    #         while nombre=="":
    #             nombre=input("Ingrese el nombre del tipo de producto: ")
        
        
    #     try:
    #         connection=conexion()
    #         cursor=connection.cursor()
            
    #         if op=="1":
    #             cursor.execute("SELECT * FROM TipoProducto WHERE idTipoProducto='"+str(id)+"'")
    #         elif op=="2":
    #             cursor.execute("SELECT * FROM TipoProducto WHERE nombre='"+str(nombre)+"'")
                
    #         results = cursor.fetchall()
    #         for row in results:
    #             print(row)
                
    #     except Exception as ex:
    #         print(ex)
        
    #     finally:
    #         if connection:
    #             connection.close()

def eliminarTipoProducto():
    
    dTP=tipoProductoDatos()
    sTPr=""
    for i in dTP:
        sTPr=sTPr+str(i)+"\n"
    
    print("*************TIPO PRODUCTO*************")
    print(sTPr)
    
    op=""
    while op=="":
        op=input("Selecione el # de tipo de producto que desea eliminar o 'S' para cancelar:")
    
    if(op!="S"):
        encontrado=False
        for i in dTP:
            if(op==str(i[0])):
                encontrado=True
                break
        if encontrado:
            productos=verProductosTipoProducto(op)
            
            if(len(productos)!=0):
                print("El tipo de producto tiene productos asociados, no se puede eliminar")
            else:
                try:
                    connection=conexion()
                    cursor=connection.cursor()
                    cursor.execute("DELETE FROM TipoProducto WHERE idTipoProducto='"+str(op)+"'")
                    cursor.execute("commit")
                except Exception as ex:
                    print(ex)
                finally:
                    if connection:
                        connection.close()
                        print("Tipo de producto eliminado con éxito")

##------------------ MODULOS PRODUCTOS------------------##
def EncProductoID(idProducto):
    try:
        connection=conexion()
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

def verProductosTipoProducto(op):
    try:
        connection=conexion()
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM Producto WHERE idTipoProducto='"+str(op)+"'")
        results = cursor.fetchall()
        datos=[]
        
        for row in results:
            datos.append(row)
            
    except Exception as ex:
        print(ex)
        
    finally:
        if connection:
            connection.close()
            
    return datos

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
    
    estatus="1"
    # ---- idTipoProducto
    encontrado=False
    idTipoProducto=""
    while (idTipoProducto==""):
        TPd=tipoProductoDatos()
        sTP=""
        for i in TPd:
            sTP=sTP+str(i)+"\n"
        print(sTP)
        idTipoProducto=input("Ingrese el idTipoProducto del producto: ")
        
        for i in TPd:
            if (str(i[0])==idTipoProducto):
                idTipoProducto=i[0]
                encontrado=True
                break
        if encontrado!=True:
            print("Tipo de producto no encontrado")
            idTipoProducto=""
    
    try:
        connection=conexion()
        cursor=connection.cursor()
        cursor.execute("INSERT INTO Producto (nombre,descripcion,precio,stock,estatus,idTipoProducto) VALUES('"+nombre+"','"+descripcion+"','"+str(precio)+"','"+str(stock)+"','"+str(estatus)+"','"+str(idTipoProducto)+"')")
        cursor.execute("commit")
    except Exception as ex:
        print(ex)
    finally:
        if connection:
            connection.close()
            print("Producto "+nombre+" creado con éxito")

def VerProductos():
    try:
        connection=conexion()

        ##print(connection.version)
        cursor=connection.cursor()

        cursor.execute("SELECT * FROM producto")
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
    print("***PRODUCTOS***")
    VerProductos()
    print("***************")
    
    #pide el id del producto a actualizar
    idProducto=""
    while (idProducto==""):
        idProducto=input("Ingrese el id del producto a actualizar: ")
        
    dProducto=[]
    (encontrado,dProducto)=EncProductoID(idProducto)
    
    if encontrado:
        idProducto=dProducto[0]
        nombre=dProducto[1]
        descripcion=dProducto[2]
        stock=dProducto[3]
        status=dProducto[4]
        precio=dProducto[5]
        idTipoProducto=dProducto[6]
        
        op=""
        while (str(op)!="0"):
            print(
                "QUE DATO DESEA EDITAR: \n"
                "1. Nombre: ("+nombre+")\n"
                "2. Descripcion: ("+descripcion+")\n"
                "3. Stock: ("+str(stock)+")\n"
                "4. Status: ("+str(status)+")\n"
                "5. Precio: ("+str(precio)+")\n"
                "6. Tipo de producto: ("+str(idTipoProducto)+")\n"
                "0. Salir"
            )
            op=input("Ingrese una opción: ")
            if op=="1":
                nombre=input("Ingrese el nuevo nombre: ")
            elif op=="2":
                descripcion=input("Ingrese la nueva descripcion: ")
            elif op=="3":
                stock=input("Ingrese el nuevo stock: ")
            elif op=="4":
                status=input("Ingrese el nuevo status: ")
            elif op=="5":
                precio=input("Ingrese el nuevo precio: ")
            elif op=="6":
                verTipoProducto()
                idTipoProducto=input("Ingrese el nuevo idTipoProducto: ")
            
            try:
                connection=conexion()
                cursor=connection.cursor()
                cursor.execute("UPDATE Producto SET nombre='"+nombre+"',descripcion='"+descripcion+"',stock='"+str(stock)+"',estatus='"+str(status)+"',precio='"+str(precio)+"',idTipoProducto='"+str(idTipoProducto)+"' WHERE idProducto='"+str(idProducto)+"'")
                cursor.execute("commit")
            except Exception as ex:
                print(ex)
            finally:
                if connection:
                    connection.close()
                    print("Producto editado con éxito")
        else:
            print("Producto no encontrado")

def VerProductoEspecifico():
    print("OPCIÓN NO DISPONIBLE")


##------------------ MODULOS TIPO DE SERVICIOS------------------##
def tipoServicioDatos():
    try:
        connection=conexion()
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
        connection=conexion()
        
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

def insertarTipoServicio():
    ## ---- NOMBRE TIPO PRODUCTO
    nombre=""
    while (nombre==""):
        nombre=input("Ingrese el nombre del tipo de servicio: ")
    ## --- DESCRIPCION TIPO PRODUCTO
    desc=""
    while (desc==""):
        desc=input("Ingrese la descripcion del tipo de servicio: ")
    
    try:
        connection=conexion()
        ##coneccion 
        cursor=connection.cursor()
        ## sentencia de insercion de rol
        cursor.execute("INSERT INTO TipoServicio (nombre,descripcion) VALUES('"+nombre+"','"+desc+"')")
        
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

def verTipoServicio():
    try:
        connection=conexion()
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM TipoServicio")
        results = cursor.fetchall()
        
        print("Número de filas recuperadas:", len(results))
        for row in results:
            print(row)
    except Exception as ex:
        print(ex)
    
    finally:
        if connection:
            connection.close()

def editarTipoServicio():
    print("*************TIPO SERVICIO*************")
    verTipoServicio()
    print("****************************************")
    
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
                connection=conexion()
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

def verTipoServicioEspecifico():
    print("OPCIÓN NO DISPONIBLE")
    # op=""
    # id=""
    # nombre=""
    # desc=""
    
    # while op!="0":
    #     op=input(
    #         "Con cual dato quiere buscar el tipo de producto:"
    #         "\n1. ID"
    #         "\n2. Nombre"
    #         "\n0. Salir"
    #     )
        
    #     if op=="1":
    #         while id=="":
    #             id=input("Ingrese el id del tipo de producto: ")
    #     elif op=="2":
    #         while nombre=="":
    #             nombre=input("Ingrese el nombre del tipo de producto: ")
        
        
    #     try:
    #         connection=conexion()
    #         cursor=connection.cursor()
            
    #         if op=="1":
    #             cursor.execute("SELECT * FROM TipoProducto WHERE idTipoProducto='"+str(id)+"'")
    #         elif op=="2":
    #             cursor.execute("SELECT * FROM TipoProducto WHERE nombre='"+str(nombre)+"'")
                
    #         results = cursor.fetchall()
    #         for row in results:
    #             print(row)
                
    #     except Exception as ex:
    #         print(ex)
        
    #     finally:
    #         if connection:
    #             connection.close()

def eliminarTipoServicio():
    
    dTP=tipoServicioDatos()
    sTPr=""
    for i in dTP:
        sTPr=sTPr+str(i)+"\n"
    
    print("*************TIPO SERVICIO*************")
    print(sTPr)
    
    op=""
    while op=="":
        op=input("Selecione el # de tipo de servicio que desea eliminar o 'S' para cancelar:")
    
    if(op!="S"):
        encontrado=False
        for i in dTP:
            if(op==str(i[0])):
                encontrado=True
                break
        if encontrado:
            productos=verServiciosTipoServivios(op)
            
            if(len(productos)!=0):
                print("El tipo de servicios tiene servicio asociados, no se puede eliminar")
            else:
                try:
                    connection=conexion()
                    cursor=connection.cursor()
                    cursor.execute("DELETE FROM TipoServicio WHERE idTipoServicio='"+str(op)+"'")
                    cursor.execute("commit")
                except Exception as ex:
                    print(ex)
                finally:
                    if connection:
                        connection.close()
                        print("Tipo de servicios eliminado con éxito")

#------------------ MODULOS SERVICIOS------------------##
def verServiciosTipoServivios(op):
    print("OPCIÓN NO DISPONIBLE")

####################################################### Modulo Compras #######################################################

# Función para mostrar los productos disponibles
def mostrar_productos_disponibles():
    # Establecer la conexión a la base de datos
    connection = conexion()
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

    except cx_Oracle.DatabaseError as e:
        print("Error al obtener los datos de la vista Vista_LeerProductos:", e)
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

def mostrar_resumen_compras():
    try:
        # Establecer la conexión a la base de datos
        connection = conexion()

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
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()


def mostrar_resumen_compras_por_estatus(estatus):
    try:
        # Establecer la conexión a la base de datos
        connection = conexion()

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
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()



# Función para realizar una compra
def realizar_compra():
    # Establecer la conexión a la base de datos
    connection = conexion()

    mostrar_productos_disponibles()

    try:
        # Pedir al usuario los datos para realizar la compra
        while True:
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
        connection.commit()

        print("¡Compra realizada con éxito!")

    except ValueError:
        print("Error: Ingrese un valor numérico válido.")
    except cx_Oracle.DatabaseError as e:
        print("Error al realizar la compra:", e)
        
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

# Procedimiento para agregar un producto a una compra existente
def agregar_producto_a_compra():
    try:
        # Establecer la conexión a la base de datos
        connection = conexion()

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
        connection.commit()

        print("Producto agregado a la compra exitosamente.")

    except ValueError:
        print("Error: Ingrese un valor numérico válido.")
    except cx_Oracle.DatabaseError as e:
        print("Error al agregar el producto a la compra:", e)
        
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
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
        connection = conexion()

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
        # Cerrar la conexión
        connection.close()



# Función para obtener el total de compras por usuario
def obtener_total_compras_usuario():
    try:
        # Pedir al usuario el ID del usuario para obtener el total de compras
        while True:
            id_usuario_input = input("Ingrese el ID del usuario (Escriba 'q' para cancelar): ")
            if id_usuario_input.lower() == 'q':
                print("Operación cancelada.")
                return menu_compras()
            elif not id_usuario_input.isdigit():
                print("Error: Ingrese un valor numérico válido.")
            else:
                id_usuario = int(id_usuario_input)
                break

        # Establecer la conexión a la base de datos
        connection = conexion()

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

        print(f"Datos del cliente con ID {id_usuario}:")
        print(f"Nombre: {nombre_cliente}")
        print(f"Correo: {correo_cliente}")
        print(f"El total de compras del cliente son: {total_compras}")
        print("\n")
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
        connection = conexion()

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

def obtener_total_productos_compra():
    try:
        # Establecer la conexión a la base de datos
        connection = conexion()

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
        connection = conexion()

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
        connection = conexion()

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
        connection = conexion()

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

# Función para mostrar el menú de compras
def menu_compras():
    op = ""
    while op != "0":
        print(
            "********** MENÚ DE COMPRAS **********\n"
            "1. Realizar Compra\n"
            "2. Agregar Producto a Compra Existente\n"
            "3. Eliminar Producto de Compra Existente\n"
            "4. Actualizar Estatus de Compra Existente\n"
            "5. Cancelar Compra Existente\n"
            "6. Obtener Total de Productos en una Compra\n"
            "7. Obtener Total de Compras por Usuario\n"
            "8. Obtener Detalle de Compra Específica\n"
            "9. Consultar compras por estatus\n"
            "0. SALIR\n"
            "************************************\n"
        )
        op = input("Ingrese una opción: ")
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
            print("Saliendo del menú de compras...")
        else:
            print("Opción no válida. Intente nuevamente.")

menu_compras()

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
            insertarTipoProducto()
        elif op=="2":
            verTipoProducto()
        elif op=="3":
            verTipoProductoEspecifico()
        elif op=="4":
            editarTipoProducto()
        elif op=="5":
            eliminarTipoProducto()

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

def MENUTIPOSERVICIO():
    op=""
    while op!="0":
        print(
            "********** MENU DE TIPO SERVICIO**********\n"
            "1. CREAR TIPO SERVICIO\n"
            "2. VER TIPO SERVICIO\n"
            "3. VER TIPO SERVICIO ESPECIFICO\n"
            "4. EDITAR TIPO SERVICIO\n"
            "5. ELIMINAR TIPO SERVICIO\n"
            "0. SALIR\n"
        )
        op=input("Ingrese una opción: ")
        
        if op=="1":
            insertarTipoServicio()
        elif op=="2":
            verTipoServicio()
        elif op=="3":
            verTipoServicioEspecifico()
        elif op=="4":
            editarTipoServicio()
        elif op=="5":
            eliminarTipoServicio()

def MENUSERVICIOS():
    print("OPCIÓN NO DISPONIBLE")

def MENUPRINCIPAL():
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
            MENUROLES()
        elif op=="2":
            MENUUSUARIOS()
        elif op=="3":
            MENUTIPOPRODUCTO()
        elif op=="4":
            MENUPRODUCTOS()
        elif op=="5":
            MENUTIPOSERVICIO()
        elif op=="6":
            MENUSERVICIOS()


# -----PROGRAMA PRINCIPAL-----
MENUPRINCIPAL()