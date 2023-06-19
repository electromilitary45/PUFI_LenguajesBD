CREATE DATABASE aura_botanica;

USE aura_botanica;

CREATE TABLE Rol ( -- revisar
    idRol int not null identity(1,1),
    nombre varchar(20) not null,
    PRIMARY KEY(idRol)
);

CREATE TABLE Usuario (
    idUsuario int not null  identity(1,1),
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
    idDireccion int not null identity(1,1),
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
    idTipoServicio int not null identity(1,1),
    nombre varchar(45) not null,
    descripcion varchar(45) not null,
    PRIMARY KEY(idTipoServicio)
);

CREATE TABLE Servicio (
    idServicio int not null identity(1,1),
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
    idServicioUsuario int not null identity(1,1) ,
    idUsuario int not null,
    idServicio int not null,
    FOREIGN KEY(idUsuario) REFERENCES Usuario(idUsuario),
    FOREIGN KEY(idServicio) REFERENCES Servicio(idServicio),
    PRIMARY KEY(idServicioUsuario)
);

CREATE TABLE TipoProducto (
    idTipoProducto int not null identity(1,1),
    nombre varchar(45) not null,
    descripcion varchar(200) not null,
    PRIMARY KEY(idTipoProducto)
);

CREATE TABLE Producto (
    idProducto int not null identity(1,1) ,
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
    idResenna int not null IDENTITY(1,1) ,
    estatus number(1) not null,
    descripcion varchar(255) not null,
    idProducto int not null,
    idUsuario int not null,
    FOREIGN KEY(idProducto) REFERENCES Producto(idProducto),
    FOREIGN KEY(idUsuario) REFERENCES Usuario(idUsuario),
    PRIMARY KEY(idResenna)
);

CREATE TABLE Compra (
    idCompra int not null IDENTITY(1,1) ,
    numeroTracking varchar(200) not null,
    precioTotal float not null,
    estatus int not null, -- 0 = pendiente, 1 = en proceso, 2 = revision, 3 = cancelado, 4= entregado
    idUsuario int not null,
    FOREIGN KEY(idUsuario) REFERENCES Usuario(idUsuario),
    PRIMARY KEY(idCompra)
);

CREATE TABLE CompraProducto (
    idCompraProducto int not null IDENTITY(1,1) ,
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
```