#base de datos,usar los comandos tal cual como estan create database pyme; use pyme; CREATE TABLE direccion (

id_direccion INT AUTO_INCREMENT PRIMARY KEY,

numero_lugar INT,

calle VARCHAR(100) NOT NULL,

comuna VARCHAR(100) NOT NULL,

region VARCHAR(100) NOT NULL

);

CREATE TABLE categoria (

id_categoria INT AUTO_INCREMENT PRIMARY KEY,

nombre VARCHAR(100) NOT NULL,

descripcion VARCHAR(255)

);

CREATE TABLE producto (

gtin VARCHAR(14) PRIMARY KEY,

nombre_producto VARCHAR(150) NOT NULL,

descripcion_producto VARCHAR(255),

precio_compra FLOAT

);

CREATE TABLE proveedor (

rut VARCHAR(12) PRIMARY KEY,

nombre VARCHAR(150) NOT NULL,

correo VARCHAR(150),

id_direccion INT,

FOREIGN KEY (id_direccion) REFERENCES direccion(id_direccion)

);

CREATE TABLE almacen (

id_almacen INT AUTO_INCREMENT PRIMARY KEY,

nombre VARCHAR(100) NOT NULL,

stock FLOAT,

id_direccion INT UNIQUE,

FOREIGN KEY (id_direccion) REFERENCES direccion(id_direccion)

);

CREATE TABLE direccion_proveedor (

id_direccion_proveedor INT AUTO_INCREMENT PRIMARY KEY,

rut_proveedor VARCHAR(12) NOT NULL,

id_direccion INT NOT NULL,

FOREIGN KEY (rut_proveedor) REFERENCES proveedor(rut),

FOREIGN KEY (id_direccion) REFERENCES direccion(id_direccion)

);

CREATE TABLE proveedores_producto (

id_proveedor_productos INT AUTO_INCREMENT PRIMARY KEY,

rut_proveedor VARCHAR(12) NOT NULL,

gtin VARCHAR(14) NOT NULL,

FOREIGN KEY (rut_proveedor) REFERENCES proveedor(rut),

FOREIGN KEY (gtin) REFERENCES producto(gtin)

);

CREATE TABLE producto_almacen (

id_producto_almacen INT AUTO_INCREMENT PRIMARY KEY,

id_almacen INT NOT NULL,

gtin VARCHAR(14) NOT NULL,

FOREIGN KEY (id_almacen) REFERENCES almacen(id_almacen),

FOREIGN KEY (gtin) REFERENCES producto(gtin)

);

CREATE TABLE categoria_producto (

id_categoria_producto INT AUTO_INCREMENT PRIMARY KEY,

id_categoria INT NOT NULL,

gtin VARCHAR(14) NOT NULL,

FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria),

FOREIGN KEY (gtin) REFERENCES producto(gtin)

);