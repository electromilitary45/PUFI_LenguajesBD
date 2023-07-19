CREATE DATABASE aura_botanica;

USE aura_botanica;

CREATE TABLE Rol ( -- revisar
    idRol NUMERIC(10) GENERATED BY DEFAULT ON NULL AS IDENTITY,
    nombre varchar(20) not null,
    PRIMARY KEY(idRol)
);

CREATE TABLE Usuario (
    idUsuario NUMERIC(10) GENERATED BY DEFAULT ON NULL AS IDENTITY,
    nombre varchar(45) not null,
    primApellido varchar(45) not null,
    segApellido varchar(45) not null,
    cedula varchar(45) not null,
    correo varchar(45) not null,
    contrasenna varchar(45) not null,
    idRol int not null,
    idDireccion int not null,
    FOREIGN KEY(idRol) REFERENCES Rol(idRol),
    PRIMARY KEY(idUsuario)
);

CREATE TABLE Direccion (
    idDireccion NUMERIC(10) GENERATED BY DEFAULT ON NULL AS IDENTITY,
    idUsuario int not null,
    provincia varchar(20) not null,
    canton varchar(20) not null,
    distrito varchar(20) not null,
    codPostal int not null,
    senalesExactas varchar(500) not null,
    PRIMARY KEY(idDireccion),
    FOREIGN KEY(idUsuario) REFERENCES Usuario(idUsuario)
);

CREATE TABLE TipoServicio (
    idTipoServicio NUMERIC(10) GENERATED BY DEFAULT ON NULL AS IDENTITY,
    nombre varchar(45) not null,
    descripcion varchar(45) not null,
    PRIMARY KEY(idTipoServicio)
);

CREATE TABLE Servicio (
    idServicio NUMERIC(10) GENERATED BY DEFAULT ON NULL AS IDENTITY,
    nombre varchar2(45) not null,
    img varchar(200) not null,
    descripcion varchar (45) not null,
    cupos int not null,
    estatus number(1) not null,
    fecha date not null,
    idTipoServicio int not null,
    FOREIGN KEY(idTipoServicio) REFERENCES TipoServicio(idTipoServicio),
    PRIMARY KEY(idServicio)
);

CREATE TABLE ServicioUsuario (
    idServicioUsuario NUMERIC(10) GENERATED BY DEFAULT ON NULL AS IDENTITY,
    idUsuario int not null,
    idServicio int not null,
    FOREIGN KEY(idUsuario) REFERENCES Usuario(idUsuario),
    FOREIGN KEY(idServicio) REFERENCES Servicio(idServicio),
    PRIMARY KEY(idServicioUsuario)
);

CREATE TABLE TipoProducto (
    idTipoProducto NUMERIC(10) GENERATED BY DEFAULT ON NULL AS IDENTITY,
    nombre varchar(45) not null,
    descripcion varchar(200) not null,
    PRIMARY KEY(idTipoProducto)
);

CREATE TABLE Producto (
    idProducto NUMERIC(10) GENERATED BY DEFAULT ON NULL AS IDENTITY,
    nombre varchar(45) not null,
    descripcion varchar(200) not null,
    stock int not null,
    estatus number(1) not null,
    precio float not null,
    idTipoProducto int not null,
    FOREIGN KEY(idTipoProducto) REFERENCES TipoProducto(idTipoProducto),
    PRIMARY KEY(idProducto)
);

CREATE TABLE Resenna (
    idResenna NUMERIC(10) GENERATED BY DEFAULT ON NULL AS IDENTITY,
    estatus number(1) not null,
    descripcion varchar(255) not null,
    idProducto int not null,
    idUsuario int not null,
    FOREIGN KEY(idProducto) REFERENCES Producto(idProducto),
    FOREIGN KEY(idUsuario) REFERENCES Usuario(idUsuario),
    PRIMARY KEY(idResenna)
);

CREATE TABLE Compra (
    idCompra NUMERIC(10) GENERATED BY DEFAULT ON NULL AS IDENTITY,
    numeroTracking varchar(200) not null,
    precioTotal float not null,
    estatus int not null, -- 0 = pendiente, 1 = en proceso, 2 = revision, 3 = cancelado, 4= entregado
    idUsuario int not null,
    FOREIGN KEY(idUsuario) REFERENCES Usuario(idUsuario),
    PRIMARY KEY(idCompra)
);

CREATE TABLE CompraProducto (
    idCompraProducto NUMERIC(10) GENERATED BY DEFAULT ON NULL AS IDENTITY,
    idCompra int not null,
    idProducto int not null,
    cantidad int not null,
    FOREIGN KEY(idCompra) REFERENCES Compra(idCompra),
    FOREIGN KEY(idProducto) REFERENCES Producto(idProducto),
    PRIMARY KEY(idCompraProducto)
);

select * from usuario;

--COMANDOS DEMASIADO DANGER
DROP TABLE usuario CASCADE CONSTRAINTS;
DROP TABLE rol CASCADE CONSTRAINTS;
DROP TABLE direccion CASCADE CONSTRAINTS;
DROP TABLE tipoServicio CASCADE CONSTRAINTS;
DROP TABLE servicio CASCADE CONSTRAINTS;
DROP TABLE servicioUsuario CASCADE CONSTRAINTS;
DROP TABLE tipoProducto CASCADE CONSTRAINTS;
DROP TABLE producto CASCADE CONSTRAINTS;
DROP TABLE resenna CASCADE CONSTRAINTS;
DROP TABLE compra CASCADE CONSTRAINTS;
DROP TABLE compraProducto CASCADE CONSTRAINTS;
--

--Creación de procedimientos 

--MODULO ROL--

--1
--Debe Crear un procedimiento que reciba como parametros:
--[ ] Nombre
--Y debe verificar que no exsista otro rol con ese mismo nombre, en caso de que no haya se crea
CREATE OR REPLACE PROCEDURE SP_CrearRol

(
    p_nombre IN VARCHAR2
) AS
BEGIN
        --Valida rol null o vacío
        IF p_nombre IS NULL OR p_nombre = '' THEN
            DBMS_OUTPUT.PUT_LINE('Error: El nombre del rol es nulo o vacío.');
            RETURN;
        END IF;

        --Verifica rol existente
        DECLARE
                cuenta NUMBER;
        BEGIN
        
        SELECT COUNT(*) INTO cuenta FROM Rol WHERE nombre = p_nombre;
        
        IF cuenta > 0 THEN
            DBMS_OUTPUT.PUT_LINE('Error: El rol ya existe.');
        ELSE
            INSERT INTO Rol(nombre) VALUES (p_nombre);
            DBMS_OUTPUT.PUT_LINE('El rol ha sido creado exitosamente.');
        END IF;
    EXCEPTION
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Error al crear el rol: ' || SQLERRM);
    END;
END;

--Prueba
BEGIN

    SP_CrearRol('');
END;

--2
--Debe Crear un procedimiento que reciba como parametros:
--idRol
--Nombre
CREATE OR REPLACE PROCEDURE SP_EditarRol
(
    p_idRol IN NUMERIC,
    p_nombre IN VARCHAR2
) AS
BEGIN
    --Valida ID nulo
    IF p_idRol IS NULL THEN
        DBMS_OUTPUT.PUT_LINE('Error: El ID ingresado es nulo.');
        RETURN;
    END IF;

    -- Valida rol null o vacío
    IF p_nombre IS NULL OR p_nombre = '' THEN
        DBMS_OUTPUT.PUT_LINE('Error: El nombre del rol es nulo o vacío.');
        RETURN;
    END IF;

    -- Verifica existencia del rol
    DECLARE
        cuenta NUMBER;
    BEGIN
        SELECT COUNT(*) INTO cuenta FROM Rol WHERE idRol = p_idRol;
        
        IF cuenta = 0 THEN
            DBMS_OUTPUT.PUT_LINE('Error: El rol no existe.');
        ELSE
            -- Actualiza el nombre del rol
            UPDATE Rol SET nombre = p_nombre WHERE idRol = p_idRol;
            DBMS_OUTPUT.PUT_LINE('El rol ha sido editado exitosamente.');
        END IF;
    EXCEPTION
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Error al editar el rol: ' || SQLERRM);
    END;
END;

--prueba
BEGIN
    SP_EditarRol(1,'Usuario');
END;


--(ROL) Sp_LeerRol#3

CREATE OR REPLACE PROCEDURE SP_LeerRol(
    p_idRol IN NUMBER
) AS
    v_cuenta NUMBER;
    v_nombre ROL.NOMBRE%TYPE;
BEGIN
    -- Verificar si el ID del rol existe
    SELECT COUNT(*) INTO v_cuenta
    FROM ROL
    WHERE IDROL = p_idRol;
    
    IF v_cuenta = 0 THEN
        -- El ID del rol no existe, mostrar un mensaje de error
        DBMS_OUTPUT.PUT_LINE('Error: El ID del rol no existe.');
    ELSE
        -- El ID del rol existe, obtener el nombre del rol
        SELECT NOMBRE INTO v_nombre
        FROM ROL
        WHERE IDROL = p_idRol;
        
        -- Mostrar los datos del rol
        DBMS_OUTPUT.PUT_LINE('ID Rol: ' || p_idRol || ' - Nombre: ' || v_nombre);
    END IF;
END;

--Prueba en ORACLE
SET SERVEROUTPUT ON
DECLARE 
    v_idRol NUMBER := 27;
BEGIN
    SP_LeerRol(v_idRol);
END;

--(ROL) Vista LeerRoles #4
--Debe mostrar todos los datos de los roles

CREATE OR REPLACE VIEW InfoRoles AS
SELECT IDROL "ID", NOMBRE"Rol" 
FROM ROL


SELECT * FROM INFOROLES



--SP Modulo USUARIO

--5
--Debe Crear un procedimiento que reciba como parametros:
--idRol
--Y realizar un select en usuarios donde se muestren solamente los usuarios que pertenezcan al rol creado.
--El select debe contener un INNER JOIN para mostrar el nombre del rol

--1er Alternativa / Crea una vista que muestra la info de usuarios junto con su rol, se  utiliza esta vista para filtrarla mediante un SP, el SP espera como parametro el nombre del rol.

--Vista UsuariosxRol
CREATE OR REPLACE VIEW V_UsuariosConRol AS
SELECT u.idUsuario "ID Usuario", u.nombre "Nombre", u.primApellido "Primer Apellido", u.segApellido "Segundo Apellido", u.cedula "Cédula", u.correo "Correo", u.contrasenna "Contraseña", r.nombre AS "Rol"
FROM Usuario u
INNER JOIN Rol r ON u.idRol = r.idRol;


--SP Filtra usuarios x Rol
CREATE OR REPLACE PROCEDURE SP_FiltrarUsuariosPorRol(
    p_nombreRol IN VARCHAR2
) AS
    cuenta NUMBER;
    v_rol V_UsuariosConRol%ROWTYPE; -- %ROWTYPE crea una variable con la misma estructura de columnas y topos de datos que la tabla o vista.
BEGIN
    -- Verificar si el rol existe
    SELECT COUNT(*) INTO cuenta FROM Rol WHERE nombre = p_nombreRol;
    
    IF cuenta = 0 THEN
        DBMS_OUTPUT.PUT_LINE('Error: El rol indicado no existe.');
    ELSE
        -- Filtrar usuarios por el rol especificado
        SELECT * INTO v_rol FROM V_UsuariosConRol WHERE "Rol" = p_nombreRol;
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al filtrar los usuarios por rol: ' || SQLERRM);
END;

--prueba
BEGIN
    SP_FiltrarUsuariosPorRol('');
END;

--2da Alternativa 

CREATE OR REPLACE PROCEDURE SP_UsuariosPorRol(
    p_idRol IN NUMERIC
) AS
BEGIN
    -- Verificar si el rol existe
    DECLARE
        cuenta NUMBER;
    BEGIN
END;
        SELECT COUNT(*) INTO cuenta FROM Rol WHERE idRol = p_idRol;

        IF cuenta = 0 THEN
            DBMS_OUTPUT.PUT_LINE('Error: El rol indicado no existe.');
        ELSE
            -- Filtrar usuarios por el rol especificado y mostrar el nombre del rol
            SELECT u.idUsuario "ID Usuario", u.nombre "Nombre", u.primApellido "Primer Apellido", u.segApellido "Segundo Apellido", u.cedula "Cédula", u.correo "Correo", u.contrasenna "Contraseña", r.nombre AS "Rol"
            FROM Usuario u
            INNER JOIN Rol r ON u.idRol = r.idRol;
            WHERE u.idRol = p_idRol;
        END IF;
    EXCEPTION
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Error al obtener los usuarios por rol: ' || SQLERRM);
    END;


--(USUARIO) SP_CrearUsuario #7

--Debe Crear un procedimiento que reciba como parametros:
--nombre
--primApellido
--segApellido
--cedula
--correo
--contrasena
--idRol
--Al tratar de crear se debe verificar por medio de la cedula, si existe no se debe registrar y debe retornar un mensaje 'El usuario ya fue creado previamente'

CREATE OR REPLACE PROCEDURE SP_CrearUsuario(
    p_nombre IN VARCHAR,
    p_primApellido IN VARCHAR,
    p_segApellido IN VARCHAR,
    p_cedula IN VARCHAR,
    p_correo IN VARCHAR,
    p_contrasenna IN VARCHAR,
    p_idRol IN NUMBER
)
AS
    cuentaCedula NUMBER;
    cuentaRol NUMBER;
BEGIN
    SELECT COUNT(*) INTO cuentaCedula FROM Usuario u
    WHERE u.cedula = p_cedula;
    
    SELECT COUNT(*) INTO cuentaRol FROM Rol r
    WHERE r.idrol = p_idRol;
    
    IF cuentaRol = 0 THEN
        DBMS_OUTPUT.PUT_LINE('El rol indicado no existe, no es posible crear el usuario con un rol inexistente.');
    ELSIF cuentaCedula > 0 THEN
        DBMS_OUTPUT.PUT_LINE('El usuario ya fue creado previamente.');
    ELSE
        INSERT INTO Usuario (nombre, primapellido, segapellido, cedula, correo, contrasenna, idrol, iddireccion)
        VALUES (p_nombre, p_primApellido, p_segApellido, p_cedula, p_correo, p_contrasenna, p_idRol,0);
        DBMS_OUTPUT.PUT_LINE('Usuario creado con éxito.');
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al crear el usuario: ' || SQLERRM);
END;

--Validación en Oracle
SET SERVEROUTPUT ON
DECLARE
    p_nombre VARCHAR2(100) := 'John';
    p_primApellido VARCHAR2(100) := 'Doe';
    p_segApellido VARCHAR2(100) := 'Smith';
    p_cedula VARCHAR2(100) := '123456789';
    p_correo VARCHAR2(100) := 'john.doe@example.com';
    p_contrasenna VARCHAR2(100) := 'password';
    p_idRol NUMBER := 27; -- Reemplaza con el ID del rol adecuado
BEGIN
    SP_CrearUsuario(p_nombre, p_primApellido, p_segApellido, p_cedula, p_correo, p_contrasenna, p_idRol);
END;

--(Usuario) View UsuariosPorRol #8

--Vista UsuariosxRol
CREATE OR REPLACE VIEW V_UsuariosConRol AS
SELECT u.idUsuario "ID Usuario", u.nombre "Nombre", u.primApellido "Primer Apellido", u.segApellido "Segundo Apellido", u.cedula "Cédula", u.correo "Correo", u.contrasenna "Contraseña", r.nombre AS "Rol"
FROM Usuario u
INNER JOIN Rol r ON u.idRol = r.idRol;


--(USUARIO) Editar Usuario#9
--Debe recibir como parametros
--[ ] idUsuario
--[ ] nombre
--[ ] primApellido
--[ ] segApellido
--[ ] cedula
--[ ] correo
--[ ] contrasenna
--[ ] idRol
--[ ] idDireccion
--y actualizar el usuario

CREATE OR REPLACE PROCEDURE SP_EditarUsr(
    p_idUsr IN NUMBER,
    p_nombre IN VARCHAR,
    p_primApellido IN VARCHAR,
    p_segApellido IN VARCHAR,
    p_cedula IN VARCHAR,
    p_correo IN VARCHAR,
    p_contrasenna IN VARCHAR,
    p_idRol IN NUMBER, 
    p_idDireccion IN NUMBER
)AS
    cuentaUsr NUMBER;
    cuentaCedula NUMBER;
    cuentaRol NUMBER;
BEGIN
    --Valida si el usuario existe
    SELECT COUNT(*) INTO cuentaUsr FROM Usuario u
    WHERE u.idUsuario = p_idUsr;

    --valida si la cedula existe y está asignada a otra persona
    SELECT COUNT(*) INTO cuentaCedula FROM Usuario u
    WHERE u.cedula = p_cedula AND u.idUsuario != p_idUsr;
    
    --valida existencia del rol
    SELECT COUNT(*) INTO cuentaRol FROM Rol r
    WHERE r.idrol = p_idRol;
    
    IF cuentaUsr = 0 THEN
        DBMS_OUTPUT.PUT_LINE('El usuario indicado no existe.');
    ELSIF cuentaRol = 0 THEN
        DBMS_OUTPUT.PUT_LINE('El rol indicado no existe, no es posible editar el usuario con un rol inexistente.');
    ELSIF cuentaCedula > 0 THEN
        DBMS_OUTPUT.PUT_LINE('La cédula ingresada pertenece a otro usuario existente.');
    ELSE
        UPDATE Usuario SET
        nombre = p_nombre,
        primapellido = p_primApellido,
        segapellido = p_segApellido,
        cedula = p_cedula,
        correo = p_correo,
        contrasenna = p_contrasenna,
        idrol = p_idRol
        WHERE idUsuario = p_idUsr;
        
        DBMS_OUTPUT.PUT_LINE('Usuario editado con éxito.');
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al editar el usuario: ' || SQLERRM);
END;

--Prueba
SET SERVEROUTPUT ON
DECLARE
    v_idUsr NUMBER := 3;
    v_nombre VARCHAR2(100) := 'John';
    v_primApellido VARCHAR2(100) := 'Doe';
    v_segApellido VARCHAR2(100) := 'Smith';
    v_cedula VARCHAR2(100) := '123456789';
    v_correo VARCHAR2(100) := 'john.doe@example.com';
    v_contrasenna VARCHAR2(100) := 'password';
    v_idRol NUMBER := 27;
    v_idDireccion NUMBER := 0;
BEGIN
    SP_EditarUsr(v_idUsr,v_nombre, v_primApellido, v_segApellido, v_cedula, v_correo, v_contrasenna, v_idRol, v_idDireccion);
END;

--------------------------------MODULO TIPO SERVICIO--------------------------------

--(TIPO SERVICIO) SP_CrearTipoServicio 
CREATE OR REPLACE PROCEDURE SP_CrearTipoServicio(
    p_nombre IN TipoServicio.nombre%TYPE,
    p_descripcion IN TipoServicio.descripcion%TYPE
) AS
    v_idTipoServicio TipoServicio.idTipoServicio%TYPE;
    v_idTipoServicioComprobacion TipoServicio.idTipoServicio%TYPE;
BEGIN
    -- Configurar la salida de mensajes del servidor
    DBMS_OUTPUT.ENABLE();

    --VALIDAR QUE NO EXISTA UN TIPO DE SERVICIO CON EL MISMO NOMBRE
    BEGIN
        SELECT idTipoServicio INTO v_idTipoServicioComprobacion FROM TipoServicio WHERE nombre = p_nombre;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            v_idTipoServicioComprobacion := NULL;
    END;

    IF v_idTipoServicioComprobacion IS NOT NULL THEN
        DBMS_OUTPUT.PUT_LINE('Error: El tipo de servicio ya existe.');
    ELSE
        INSERT INTO TipoServicio(nombre, descripcion) 
        VALUES (p_nombre, p_descripcion) 
        RETURNING idTipoServicio INTO v_idTipoServicio;

        DBMS_OUTPUT.PUT_LINE('El tipo de servicio ha sido creado exitosamente. ID: ' || v_idTipoServicio || ' Nombre: ' || p_nombre || ' Descripción: ' || p_descripcion);
    END IF;
END;

--(TIPOS SERVICIO) VIEW TIPOS SERVICIO
CREATE OR REPLACE VIEW V_TiposServicio AS
SELECT idTipoServicio, nombre, descripcion
FROM TipoServicio;

SET SERVEROUTPUT ON

DECLARE
    v_count NUMBER;
BEGIN
    -- Comprobar si existen datos en la vista
    SELECT COUNT(*) INTO v_count FROM TipoServicio;

    -- Mostrar mensaje según existencia de datos
    IF v_count > 0 THEN
        FOR TipoServicio IN (SELECT * FROM TipoServicio) LOOP
            DBMS_OUTPUT.PUT_LINE('ID: ' || tiposervicio.idTipoServicio || ' Nombre: ' || tiposervicio.nombre || ' Descripción: ' || tiposervicio.descripcion);
        END LOOP;
    ELSE
        DBMS_OUTPUT.PUT_LINE('No hay datos disponibles en la vista.');
    END IF;
END;


--------------------------------MODULO SERVICIO--------------------------------

-----Sp_INSERTAR SERVICIO----
CREATE PROCEDURE SP_CrearServicio(
    p_nombre IN Servicio.nombre%TYPE,
    p_img IN Servicio.img%TYPE,
    p_descripcion IN Servicio.descripcion%TYPE,
    p_cupos IN Servicio.cupos%TYPE,
    p_estatus IN Servicio.estatus%TYPE,
    p_fecha IN Servicio.fecha%TYPE,
    p_idTipoServicio IN Servicio.idTipoServicio%TYPE
) AS
    v_idServicio Servicio.idServicio%TYPE;
    v_idServicioComprobacion Servicio.idServicio%TYPE;
    v_idTipoServicioComprobacion TipoServicio.idTipoServicio%TYPE;
BEGIN
    -- Configurar la salida de mensajes del servidor
    DBMS_OUTPUT.ENABLE();

    ---VALIDAR QUE NO EXISTA UN SERVICIO CON EL MISMO NOMBRE
    BEGIN
        SELECT idServicio INTO v_idServicioComprobacion FROM Servicio WHERE nombre = p_nombre;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            v_idServicioComprobacion := NULL;
    END;

    ---VALIDAR QUE EXISTA UN TIPO DE SERVICIO CON EL MISMO ID
    BEGIN
        SELECT idTipoServicio INTO v_idTipoServicioComprobacion FROM TipoServicio WHERE idTipoServicio = p_idTipoServicio;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            v_idTipoServicioComprobacion := NULL;
    END;

    --VALIDAR QUE NO EXISTA UN SERVICIO CON EL MISMO NOMBRE Y QUE EL TIPO DE SERVICIO EXISTA
    IF v_idServicioComprobacion IS NOT NULL AND v_idTipoServicioComprobacion IS NULL THEN
        DBMS_OUTPUT.PUT_LINE('Error: El servicio ya existe o el tipo de servicio no existe.');
    ELSE
        --INSERTAR SERVICIO
        INSERT INTO Servicio(nombre, img, descripcion, cupos, estatus, fecha, idTipoServicio) 
        VALUES (p_nombre, p_img, p_descripcion, p_cupos, p_estatus, p_fecha, p_idTipoServicio) 
        RETURNING idServicio INTO v_idServicio;

        DBMS_OUTPUT.PUT_LINE('El servicio ha sido creado exitosamente. ID: ' || v_idServicio || ' Nombre: ' || p_nombre || ' Imagen: ' || p_img || ' Descripción: ' || p_descripcion || ' Cupos: ' || p_cupos || ' Estatus: ' || p_estatus || ' Fecha: ' || p_fecha || ' ID Tipo Servicio: ' || p_idTipoServicio);
    END IF;

END;

--VIEW SERVICIOS--
CREATE OR REPLACE VIEW V_Servicios AS
    SELECT u.idServicio, u.nombre, u.img, u.descripcion, u.cupos, u.estatus, u.fecha, t.nombre  AS "Tipo Servicio"
    FROM Servicio u
    INNER JOIN TipoServicio t ON u.idTipoServicio = t.idTipoServicio;
