import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"g:\ORACLE\instantclient")

##------------------ MODULOS USUARIOS------------------##
def InsertUsuario():
    nombre=input("Ingrese su nombre: ")
    apellido1=input("Ingrese su Primer Apellido: ")
    apellido2=input("Ingrese su Segundo Apellido: ")
    cedula=input("Ingrese su cédula: ")
    correo=input("Ingrese su correo: ")
    contrasena=input("Ingrese su contraseña: ")
    idRol=input("Ingrese su rol: ")
    idDireccion=1


    try:
        connection=cx_Oracle.connect(
            user='DBADEREK',
            password='Villaley45',
            dsn='localhost:1521/orcl',
            encoding='UTF-8'
        )

        cursor=connection.cursor()
        cursor.execute("INSERT INTO usuario (idUsuario,nombre,primapellido,segapellido,) VALUES('"+nombre+"', '"+apellido1+"', '")
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
    print("OPCIÓN EN DESARROLLO")

def ActualizarUsuario():
    print("OPCIÓN EN DESARROLLO")

def DesactivarUsuario():
    print("OPCIÓN EN DESARROLLO")

##------------------ MODULOS PRODUCTOS------------------##

##------------------ MODULOS PEDIDOS------------------##


##------------------ MENUS------------------##
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

def MENUPRINCIPAL():
    op=""
    while op!="0":
        print(
            "********** MENU **********\n"
            "1. USUARIOS\n"
            "2. PRODUCTOS\n"
            "0. SALIR\n"
        )

        op=input("Ingrese una opción: ")
        if op=="1":
            MENUUSUARIOS()
        elif op=="2":
            print("OPCIÓN EN DESARROLLO")


MENUPRINCIPAL()