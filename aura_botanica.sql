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

--------------------(TIPO SERVICIO) SP_CrearTipoServicio -----------------------
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

---------------------(TIPOS SERVICIO) VIEW TIPOS SERVICIO----------------------
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

------------------(TIPO SERVICIO) SP_EditarTipoServicio--------------------------
CREATE OR REPLACE PROCEDURE SP_EditarTipoServicio(
    p_idTipoServicio IN TipoServicio.idTipoServicio%TYPE,
    p_nombre IN TipoServicio.nombre%TYPE,
    p_descripcion IN TipoServicio.descripcion%TYPE
) AS
    v_idTipoServicio TipoServicio.idTipoServicio%TYPE;
    v_idTipoServicioComprobacion TipoServicio.idTipoServicio%TYPE;
BEGIN

    -- Configurar la salida de mensajes del servidor
    DBMS_OUTPUT.ENABLE();

    if p_idTipoServicio IS NOT NULL THEN
        
        --VALIDAR QUE EXISTA UN TIPO DE SERVICIO CON EL MISMO ID
        BEGIN
            SELECT idTipoServicio INTO v_idTipoServicioComprobacion FROM TipoServicio WHERE idTipoServicio = p_idTipoServicio;
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                v_idTipoServicioComprobacion := NULL;
        END;

        IF v_idTipoServicioComprobacion IS NOT NULL THEN
            UPDATE TipoServicio SET
            nombre = p_nombre,
            descripcion = p_descripcion
            WHERE idTipoServicio = p_idTipoServicio;
            
            DBMS_OUTPUT.PUT_LINE('Tipo de servicio editado con éxito.');
        ELSE
            DBMS_OUTPUT.PUT_LINE('Error: El tipo de servicio no existe.');
        END IF;
    ELSE
        DBMS_OUTPUT.PUT_LINE('Error: El ID del tipo de servicio es nulo.');
    END IF;
END;

------------(TipoServicio) SP_EliminarTipoServicio------------------
CREATE OR REPLACE PROCEDURE SP_EliminarTipoServicio(
    p_idTipoServicio IN TipoServicio.idTipoServicio%TYPE
) AS
    v_idTipoServicio TipoServicio.idTipoServicio%TYPE;
    v_idTipoServicioComprobacion TipoServicio.idTipoServicio%TYPE;
    v_cantidadServicios NUMBER;
BEGIN
    -- Configurar la salida de mensajes del servidor
    DBMS_OUTPUT.ENABLE();

    --VALIDAR QUE EXISTA UN TIPO DE SERVICIO CON EL MISMO ID
    BEGIN
        SELECT idTipoServicio INTO v_idTipoServicioComprobacion FROM TipoServicio WHERE idTipoServicio = p_idTipoServicio;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            v_idTipoServicioComprobacion := NULL;
    END;

    if p_idTipoServicio IS NOT NULL THEN
        BEGIN
            --VALIDAR QUE NO EXISTAN SERVICIOS CON EL MISMO TIPO DE SERVICIO y contarlos
            SELECT COUNT(*) INTO v_cantidadServicios FROM Servicio WHERE idTipoServicio = p_idTipoServicio;
        end;
        if v_cantidadServicios > 0 THEN
            DBMS_OUTPUT.PUT_LINE('Error: No se puede eliminar el tipo de servicio porque existen servicios asociados a él.');
        ELSE
            DELETE FROM TipoServicio WHERE idTipoServicio = p_idTipoServicio;
            DBMS_OUTPUT.PUT_LINE('Tipo de servicio eliminado con éxito.');
        END IF;
    ELSE
        DBMS_OUTPUT.PUT_LINE('Error: El ID del tipo de servicio es nulo o no existe.');
    END IF;
END;



-------------\---------\----------MODULO SERVICIO------\-----------\-------------\--

-----Sp_INSERTAR SERVICIO----
CREATE OR REPLACE PROCEDURE SP_CrearServicio(
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

-----------------VIEW SERVICIOS---------------
CREATE OR REPLACE VIEW V_Servicios AS
    SELECT u.idServicio, u.nombre, u.img, u.descripcion, u.cupos, u.estatus, u.fecha, t.nombre  AS "Tipo Servicio"
    FROM Servicio u
    INNER JOIN TipoServicio t ON u.idTipoServicio = t.idTipoServicio;

----------------editar servicio----------------
CREATE OR REPLACE PROCEDURE SP_editarServicio(
    p_idServicio IN Servicio.idServicio%TYPE,
    p_nombre IN Servicio.nombre%TYPE,
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
    ---configurar la salida de mensajes del servidor
    DBMS_OUTPUT.ENABLE();

    ---VALIDAR QUE EXISTA UN SERVICIO CON EL MISMO ID
    BEGIN
        SELECT idServicio INTO v_idServicioComprobacion FROM Servicio WHERE idServicio = p_idServicio;
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

    --validar que los datos no sean nulos
    IF v_idServicioComprobacion is not null and v_idTipoServicioComprobacion is not null THEN
        UPDATE Servicio SET
        nombre = p_nombre,
        descripcion = p_descripcion,
        cupos = p_cupos,
        estatus = p_estatus,
        fecha = p_fecha,
        idTipoServicio = p_idTipoServicio
        WHERE idServicio = p_idServicio;
        
        DBMS_OUTPUT.PUT_LINE('Servicio editado con éxito.');
    ELSE
        DBMS_OUTPUT.PUT_LINE('Error: El servicio no existe o el tipo de servicio no existe.');
    END IF;
END;

CREATE OR REPLACE PROCEDURE SP_EliminarServicio(
    p_idServicio IN Servicio.idServicio%TYPE
) AS
    v_idServicio Servicio.idServicio%TYPE;
    v_idServicioComprobacion Servicio.idServicio%TYPE;
    v_cantidadServiciosUsuario NUMBER;
BEGIN
    -- Configurar la salida de mensajes del servidor
    DBMS_OUTPUT.ENABLE();

    --VALIDAR QUE EXISTA UN SERVICIO CON EL MISMO ID
    BEGIN
        SELECT idServicio INTO v_idServicioComprobacion FROM Servicio WHERE idServicio = p_idServicio;
    END;

    BEGIN 
        --VALIDAR QUE NO EXISTAN SERVICIOS ASOCIADOS A UN USUARIO
        SELECT COUNT(*) INTO v_cantidadServiciosUsuario FROM ServicioUsuario WHERE idServicio = p_idServicio;
    END;

    if v_idServicioComprobacion is not null THEN
        if v_cantidadServiciosUsuario > 0 THEN
            DBMS_OUTPUT.PUT_LINE('Error: No se puede eliminar el servicio porque existen usuarios asociados a él.');
        ELSE
            DELETE FROM Servicio WHERE idServicio = p_idServicio;
            DBMS_OUTPUT.PUT_LINE('Servicio eliminado con éxito.');
        END IF;
    ELSE
        DBMS_OUTPUT.PUT_LINE('Error: El servicio no existe.');
    END IF;

END;
-------------------------verServicioPorTipo----------------------
CREATE OR REPLACE PROCEDURE SP_verServiciosTipo(
    p_idTipoServicio IN Servicio.idTipoServicio%TYPE
) AS
    v_idTipoServicio Servicio.idTipoServicio%TYPE;
    v_idTipoServicioComprobacion Servicio.idTipoServicio%TYPE;
    v_idServicio Servicio.idServicio%TYPE;
    v_nombre Servicio.nombre%TYPE;
    v_descripcion Servicio.descripcion%TYPE;
    v_cupos Servicio.cupos%TYPE;
    v_estatus Servicio.estatus%TYPE;
    v_fecha Servicio.fecha%TYPE;
    v_nombreTipoServicio tiposervicio.nombre%TYPE;

    -- Declarar el cursor explícito
    CURSOR c_servicios IS
        SELECT s.idServicio, s.nombre, s.descripcion, s.cupos, s.estatus, s.fecha, t.nombre AS nombreTipoServicio
        FROM Servicio s
        JOIN TipoServicio t ON s.idTipoServicio = t.idTipoServicio
        WHERE t.idTipoServicio = p_idTipoServicio;
BEGIN
    -- Configurar la salida de mensajes del servidor
    DBMS_OUTPUT.ENABLE();

    --VALIDAR QUE EXISTA UN TIPO DE SERVICIO CON EL MISMO ID
    BEGIN
        SELECT idTipoServicio INTO v_idTipoServicioComprobacion FROM TipoServicio WHERE idTipoServicio = p_idTipoServicio;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            v_idTipoServicioComprobacion := NULL;
    END;

    IF v_idTipoServicioComprobacion IS NOT NULL THEN
        -- Abrir el cursor explícito
        OPEN c_servicios;

        -- Recorrer los resultados del cursor y mostrarlos
        LOOP
            FETCH c_servicios INTO v_idServicio, v_nombre, v_descripcion, v_cupos, v_estatus, v_fecha, v_nombreTipoServicio;
            EXIT WHEN c_servicios%NOTFOUND;

            -- Devolver todos los datos
            DBMS_OUTPUT.PUT_LINE('ID Servicio: ' || v_idServicio || ' Nombre: ' || v_nombre || ' Descripción: ' || v_descripcion || ' Cupos: ' || v_cupos || ' Estatus: ' || v_estatus || ' Fecha: ' || v_fecha || ' Tipo de Servicio: ' || v_nombreTipoServicio);
        END LOOP;

        -- Cerrar el cursor explícito
        CLOSE c_servicios;
    ELSE
        DBMS_OUTPUT.PUT_LINE('Error: El tipo de servicio no existe.');
    END IF;
END;

----\---------\-----------\-------MODULO Resenna-------\------\--------------\-----

--SP_CrearResenna--
-- Debe tener los siguentes parametros:
-- -[ ] estatus
-- -[ ] descripcion
-- -[ ] idProducto
-- -[ ] idUsuario

CREATE OR REPLACE PROCEDURE SP_CrearResenna(
    p_estatus IN Resenna.estatus%TYPE,
    p_descripcion IN Resenna.descripcion%TYPE,
    p_idProducto IN Resenna.idProducto%TYPE,
    p_idUsuario IN Resenna.idUsuario%TYPE;
)
AS
    v_idResenna Resenna.idResenna%TYPE;
BEGIN
    -- Configurar la salida de mensajes del servidor
    DBMS_OUTPUT.ENABLE();

    INSERT INTO Resenna(estatus, descripcion, idProducto, idUsuario) 
    VALUES (p_estatus, p_descripcion, p_idProducto, p_idUsuario)
    RETURNING idResenna INTO v_idResenna;

    DBMS_OUTPUT.PUT_LINE('La reseña se ha creado exitosamente. ID: ' || v_idResenna || ' estatus: ' || p_estatus || ' Descripción: ' || p_descripcion || ' ID Producto: ' || p_idProducto || ' ID Usuario ' || p_idUsuario);
    
    EXCEPTION
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Error al crear la reseña: ' || SQLERRM);
    END;
END;

--SP_LeerResenna (UNICO)--
-- Debe de tener como parametro:
-- -[ ] idResenna

-- Debe de mostrar los siguientes parametros:
-- -[ ] estatus
-- -[ ] descripcion
-- -[ ] idProducto
-- -[ ] idUsuario

CREATE OR REPLACE PROCEDURE SP_LeerResennaUnico(
    p_idResenna IN NUMBER
) AS
    v_cuenta NUMBER;
    v_estatus IN Resenna.estatus%TYPE;
    v_descripcion IN Resenna.descripcion%TYPE;
    v_idProducto IN Resenna.idProducto%TYPE;
    v_idUsuario IN Resenna.idUsuario%TYPE;
BEGIN
    -- Verificar si el ID de la reseña existe
    SELECT COUNT(*) INTO v_cuenta
    FROM Resenna
    WHERE idResenna = p_idResenna;
    
    IF v_cuenta = 0 THEN
        -- El ID de la reseña no existe, mostrar un mensaje de error
        DBMS_OUTPUT.PUT_LINE('Error: El ID de la reseña no existe.');
    ELSE
        -- El ID de la reseña existe, obtener el estatus, descripcion, idProducto y idUsuario
        SELECT estatus, descripcion, idProducto, idUsuario INTO v_estatus, v_descripcion, v_idProducto, v_idUsuario
        FROM Resenna
        WHERE idResenna = p_idRresenna;
        
        -- Mostrar los datos de la reseña
        DBMS_OUTPUT.PUT_LINE('ID Reseña: ' || p_idResenna || ' Estatus: ' || v_estatus || ' Descripción: ' || v_descripcion || ' ID Producto: ' || v_idProducto || ' ID Usuario: ' || v_idUsuario);
    END IF;
    EXCEPTION
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Error al leer la reseña: ' || SQLERRM);
    END;
END;

--SP_EditarResenna--
-- Debe tener los siguentes parametros:
-- -[ ] estatus
-- -[ ] descripcion
-- -[ ] idProducto
-- -[ ] idUsuario

CREATE OR REPLACE PROCEDURE SP_EditarResenna
(
    p_idResenna IN NUMERIC,
    p_estatus IN NUMBER,
    p_descripcion IN VARCHAR2,
    p_idProducto IN NUMERIC,
    p_idUsuario IN NUMERIC,
) AS
BEGIN
    --Valida ID nulo
    IF p_idResenna IS NULL THEN
        DBMS_OUTPUT.PUT_LINE('Error: El ID ingresado es nulo.');
        RETURN;
    END IF;

    -- Verifica existencia de la reseña
    DECLARE
        cuenta NUMBER;
    BEGIN
        SELECT COUNT(*) INTO cuenta FROM Resenna WHERE idRresenna = p_idResenna;
        
        IF cuenta = 0 THEN
            DBMS_OUTPUT.PUT_LINE('Error: La reseña no existe.');
        ELSE
            -- Actualiza los datos de reseña
            UPDATE Resenna SET estatus = p_estatus,
                               descripcion = p_descripcion,
                               idProducto = p_idProducto,
                               idUsuario = p_idUsuario
            WHERE idResenna = p_idResenna;
            DBMS_OUTPUT.PUT_LINE('La reseña ha sido editada exitosamente.');
        END IF;
    EXCEPTION
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Error al editar la reseña: ' || SQLERRM);
    END;
END;

--SP_LeerResenna (TODOS)--
-- Debe de mostrar los siguientes parametros de porducto:
-- -[ ] nombre

-- Debe de mostrar los siguientes parametros:
-- -[ ] estatus
-- -[ ] descripcion
-- -[ ] idProducto
-- -[ ] idUsuario

CREATE OR REPLACE PROCEDURE SP_LeerResennaTodos(
    p_idResenna IN NUMBER
) AS
    v_cuenta NUMBER;
    v_estatus IN Resenna.estatus%TYPE;
    v_descripcion IN Resenna.descripcion%TYPE;
    v_idProducto IN Resenna.idProducto%TYPE;
    v_idUsuario IN Resenna.idUsuario%TYPE;
    v_nombreP IN Producto.nombre%TYPE;
BEGIN    
    -- El ID de la reseña existe, obtener el estatus, descripcion, idProducto y idUsuario
    SELECT r.estatus, r.descripcion, r.idProducto, r.idUsuario, p.nombre INTO v_estatus, v_descripcion, v_idProducto, v_idUsuario, v_nombreP
    FROM Resenna r
    INNER JOIN Producto p ON r.idProducto = p.idProducto;
        
    -- Mostrar los datos de la reseña
    DBMS_OUTPUT.PUT_LINE('ID Reseña: ' || p_idResenna || ' Estatus: ' || v_estatus || ' Descripción: ' || v_descripcion || ' ID Producto: ' || v_idProducto || ' ID Usuario: ' || v_idUsuario || ' Nombre Producto ' || v_nombreP);
    END IF;
    EXCEPTION
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Error al leer la reseña: ' || SQLERRM);
    END;
END;

--View_LeerResennaInactiva (TODAS)
-- Debe de recibir como parametro de resennas:
-- -[ ] estatus

-- Debe de mostrar los siguientes parametros de porducto:
-- -[ ] nombre

-- Debe de mostrar los siguientes parametros de resennas:
-- -[ ] estatus
-- -[ ] descripcion
-- -[ ] idProducto
-- -[ ] idUsuario

CREATE OR REPLACE VIEW View_LeerResennaInactiva AS
SELECT r.estatus, r.descripcion, r.idProducto, r.idUsuario, p.nombre
FROM Resenna r
JOIN Producto p ON r.idProducto = p.idProducto
WHERE r.estatus = 0;

SELECT * FROM View_LeerResennaInactiva;

--View_LeerResennaActiva (TODAS)
-- Debe de recibir como parametro de resennas:
-- -[ ] estatus

-- Debe de mostrar los siguientes parametros de porducto:
-- -[ ] nombre

-- Debe de mostrar los siguientes parametros de resennas:
-- -[ ] estatus
-- -[ ] descripcion
-- -[ ] idProducto
-- -[ ] idUsuario

CREATE OR REPLACE VIEW View_LeerResennaActiva AS
SELECT r.estatus, r.descripcion, r.idProducto, r.idUsuario, p.nombre
FROM Resenna r
JOIN Producto p ON r.idProducto = p.idProducto
WHERE r.estatus = 1;

SELECT * FROM View_LeerResennaActiva;

------------------------------FIN MODULO Resenna------------------------------

--------------------------------MODULO Direcciones--------------------------------

--SP_EditarDireccion
-- Debe recibir como parametros
-- -[ ] idUsuario
-- -[ ] provincia
-- -[ ] canton
-- -[ ] distrito
-- -[ ] codPostal
-- -[ ] senalesExactas

-- y actualizar el usuario

CREATE OR REPLACE PROCEDURE SP_EditarDireccion
(
    p_idDireccion IN NUMERIC,
    p_provincia IN VARCHAR2,
    p_caton IN VARCHAR2,
    p_distrito IN VARCHAR2,
    p_codPostal IN NUMERIC,
    p_senalesExactas IN VARCHAR2,
    p_idUsuario in NUMERIC
) AS
BEGIN
    --Valida ID nulo
    IF p_idDireccion IS NULL THEN
        DBMS_OUTPUT.PUT_LINE('Error: El ID ingresado es nulo.');
        RETURN;
    END IF;

    -- Verifica existencia de la direccion
    DECLARE
        cuenta NUMBER;
    BEGIN
        SELECT COUNT(*) INTO cuenta FROM Direccion WHERE idDireccion = p_idDireccion;
        
        IF cuenta = 0 THEN
            DBMS_OUTPUT.PUT_LINE('Error: La direccion no existe.');
        ELSE
            -- Actualiza los datos de reseña
            UPDATE Direccion SET provincia = p_provincia,
                                 canton = p_canton,
                                 distrito = p_distrito,
                                 codPostal = p_codPostal,
                                 senalesExactas = p_senalesExactas,
                                 idUsuario = p_idUsuario
            WHERE idDireccion = p_idDireccion;
            DBMS_OUTPUT.PUT_LINE('La direccion ha sido editada exitosamente.');
        END IF;
    EXCEPTION
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Error al editar la direccion: ' || SQLERRM);
    END;
END;

--SP_LeerDireccion (UNICO)
-- debe de recibir por parámetro:
-- -[ ] idUsuario

-- retornar todos los datos de direcciones:
-- -[ ] idUsuario
-- -[ ] idDireccion
-- -[ ] provincia
-- -[ ] canton
-- -[ ] distrito
-- -[ ] codPostal
-- -[ ] senalesExtras

-- ademas mostrar los siguientes datos de la tabla usuarios:
-- -[ ] nombre
-- -[ ] primApellido
-- -[ ] segApellido

CREATE OR REPLACE PROCEDURE SP_LeerDireccionUnico(
    p_idDireccion IN NUMBER,
    p_idUsuario IN NUMERIC
) AS
    v_cuenta NUMBER;
    --Datos Direccion
    v_idUsuario IN Direccion.idUsuario%TYPE;
    v_provincia IN Direccion.provincia%TYPE;
    v_canton IN Direccion.canton%TYPE;
    v_distrito IN Direccion.distrito%TYPE;
    v_codPostal IN Direccion.codPostal%TYPE;
    v_senalesExactas IN Resenna.senalesExactas%TYPE;
    --Datos Usuario
    v_nombreUser IN Usuario.nombre%TYPE;
    v_primApellido IN Usuario.primApellido%TYPE;
    v_segApellido IN Usuario.segApellido%TYPE;
BEGIN
    -- Verificar si el ID de la direccion existe
    SELECT COUNT(*) INTO v_cuenta
    FROM Direccion
    WHERE idDireccion = p_idDireccion;
    
    IF v_cuenta = 0 THEN
        -- El ID de la direccion no existe, mostrar un mensaje de error
        DBMS_OUTPUT.PUT_LINE('Error: El ID de la direccion no existe.');
    ELSE
        -- El ID de la direccion existe
        SELECT d.idUsuario, d.provincia, d.canton, d.distrito, d.codPostal, d.senalesExactas, u.nombre, u.primApellido, u.segApellido 
        INTO v_idUsuario, v_provincia, v_canton, v_distrito, v_codPostal, v_senalesExactas, v_nombreUser, v_primApellido, v_segApellido
        FROM Direccion d
        JOIN Usuario u ON d.idUsuario = u.idUsuario
        WHERE u.idUsuario = p_idUsuario;
        
        -- Mostrar los datos de la direccion
        DBMS_OUTPUT.PUT_LINE('ID Usuario: ' || p_idUsuario || ' Nombre Usuario: ' || v_nombre || ' Primer Apellido: ' || v_primApellido || ' Segundo Apellido: ' || v_segApellido || ' ID Direccion: ' || p_idDireccion || ' Provincia: ' || v_provincia || ' Canton: ' || v_canton || ' Distrito: ' || v_distrito || ' Codigo Postal: ' || v_codPostal || ' Señales Exactas: ' || v_senalesExactas);
    END IF;
    EXCEPTION
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Error al leer la direccion: ' || SQLERRM);
    END;
END;

--View_LeerDireccion (TODOS)
-- retornar todos los datos de direccion:
-- -[ ] idUsuario
-- -[ ] idDireccion
-- -[ ] provincia
-- -[ ] canton
-- -[ ] distrito
-- -[ ] codPostal
-- -[ ] senalesExtras

-- ademas mostrar los siguientes datos de la tabla usuarios:
-- -[ ] nombre
-- -[ ] primApellido
-- -[ ] segApellido

CREATE OR REPLACE VIEW View_LeerDireccionTodos AS
SELECT d.idUsuario, d.idDireccion, d.provincia, d.canton, d.distrito, d.codPostal, d.senalesExactas, u.nombre, u.primApellido, u.segApellido
FROM Direccion d
JOIN Usuario u ON d.idUsuario = u.idUsuario
WHERE u.idUsuario = p_idUsuario;

SELECT * FROM View_LeerDireccionTodos;

--Trigger_VerDireccionCreada
-- Se debe de mostrar la direccion creada anteriormente

SET SERVEROUTPUT ON;

CREATE OR REPLACE TRIGGER Trigger_VerDireccionCreada
AFTER INSERT ON Direccion
FOR EACH ROW
DECLARE
BEGIN
    DBMS_OUTPUT.PUT_LINE('--- Dirección creada anteriormente ---');
    DBMS_OUTPUT.PUT_LINE('ID Usuario: ' || Direccion.idUsuario);
    DBMS_OUTPUT.PUT_LINE('ID Direccion: ' || Direccion.idDireccion);
    DBMS_OUTPUT.PUT_LINE('Provincia: ' || Direccion.provincia);
    DBMS_OUTPUT.PUT_LINE('Canton: ' || Direccion.canton);
    DBMS_OUTPUT.PUT_LINE('Distrito: ' || Direccion.distrito);
    DBMS_OUTPUT.PUT_LINE('CodPostal: ' || Direccion.codPostal);
    DBMS_OUTPUT.PUT_LINE('Senales Extras: ' || Direccion.senalesExactas);
    DBMS_OUTPUT.PUT_LINE('------------------------------------');
END;

--Trigger_VerDireccionEditada
-- Se debe de mostrar la direccion creada anteriormente

SET SERVEROUTPUT ON;

CREATE OR REPLACE TRIGGER Trigger_VerDireccionCreada
AFTER UPDATE ON Direccion
FOR EACH ROW
DECLARE
BEGIN
    DBMS_OUTPUT.PUT_LINE('--- Dirección editada anteriormente ---');
    DBMS_OUTPUT.PUT_LINE('ID Usuario: ' || Direccion.idUsuario);
    DBMS_OUTPUT.PUT_LINE('ID Direccion: ' || Direccion.idDireccion);
    DBMS_OUTPUT.PUT_LINE('Provincia: ' || Direccion.provincia);
    DBMS_OUTPUT.PUT_LINE('Canton: ' || Direccion.canton);
    DBMS_OUTPUT.PUT_LINE('Distrito: ' || Direccion.distrito);
    DBMS_OUTPUT.PUT_LINE('CodPostal: ' || Direccion.codPostal);
    DBMS_OUTPUT.PUT_LINE('Senales Extras: ' || Direccion.senalesExactas);
    DBMS_OUTPUT.PUT_LINE('------------------------------------');
END;

------------------------------Fin MODULO Direcciones------------------------------