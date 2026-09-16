# codigo.py

class Direccion:
    def __init__(self, numero_lugar: int, calle: str, comuna: str, region: str, id_direccion=None):
        self.id_direccion = id_direccion
        self.numero_lugar = numero_lugar
        self.calle = calle
        self.comuna = comuna
        self.region = region

    def obtener_direccion(self) -> str:
        return f"{self.calle} {self.numero_lugar}, {self.comuna}, {self.region}"

    def guardar(self, conexion):
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO direccion (numero_lugar, calle, comuna, region) VALUES (%s, %s, %s, %s)",
            (self.numero_lugar, self.calle, self.comuna, self.region)
        )
        conexion.commit()
        self.id_direccion = cursor.lastrowid
        cursor.close()


class Categoria:
    def __init__(self, nombre: str, descripcion: str, id_categoria=None):
        self.id_categoria = id_categoria
        self.nombre = nombre
        self.descripcion = descripcion

    def guardar(self, conexion):
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO categoria (nombre, descripcion) VALUES (%s, %s)",
            (self.nombre, self.descripcion)
        )
        conexion.commit()
        self.id_categoria = cursor.lastrowid
        cursor.close()


class Proveedor:
    def __init__(self, rut: str, nombre: str, correo: str, direccion: Direccion):
        self.rut = rut
        self.nombre = nombre
        self.correo = correo
        self.direccion = direccion

    def entregar_producto(self, producto: "Producto", conexion):
        if self not in producto.proveedores:
            producto.proveedores.append(self)

        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO proveedores_producto (rut_proveedor, gtin) VALUES (%s, %s)",
            (self.rut, producto.gtin)
        )
        conexion.commit()
        cursor.close()

    def guardar(self, conexion):
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO proveedor (rut, nombre, correo, id_direccion) VALUES (%s, %s, %s, %s)",
            (self.rut, self.nombre, self.correo, self.direccion.id_direccion)
        )
        conexion.commit()
        cursor.close()


class Producto:
    def __init__(self, nombre: str, gtin: str, descripcion: str, precio_compra: float, categoria: Categoria):
        self.nombre = nombre
        self.gtin = gtin
        self.descripcion = descripcion
        self.precio_compra = precio_compra
        self.categoria = categoria
        self.proveedores = []

    def guardar(self, conexion):
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO producto (gtin, nombre_producto, descripcion_producto, precio_compra) VALUES (%s, %s, %s, %s)",
            (self.gtin, self.nombre, self.descripcion, self.precio_compra)
        )
        cursor.execute(
            "INSERT INTO categoria_producto (id_categoria, gtin) VALUES (%s, %s)",
            (self.categoria.id_categoria, self.gtin)
        )
        conexion.commit()
        cursor.close()


class Almacen:
    def __init__(self, nombre: str, direccion: Direccion, stock: float = 0.0, id_almacen=None):
        self.id_almacen = id_almacen
        self.nombre = nombre
        self.direccion = direccion
        self.stock = stock
        self.productos = {}

    def registrar_producto(self, producto: Producto, stock: float, conexion):
        self.productos[producto] = stock
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO producto_almacen (id_almacen, gtin) VALUES (%s, %s)",
            (self.id_almacen, producto.gtin)
        )
        conexion.commit()
        cursor.close()

    def guardar(self, conexion):
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO almacen (nombre, stock, id_direccion) VALUES (%s, %s, %s)",
            (self.nombre, self.stock, self.direccion.id_direccion)
        )
        conexion.commit()
        self.id_almacen = cursor.lastrowid
        cursor.close()


class Inventario:
    def __init__(self, almacen: Almacen):
        self.almacen = almacen

    def sumar_producto(self, producto: Producto, cantidad: float):
        if producto in self.almacen.productos:
            self.almacen.productos[producto] += cantidad
            self.almacen.stock += cantidad

    def restar_producto(self, producto: Producto, cantidad: float):
        if producto in self.almacen.productos:
            self.almacen.productos[producto] -= cantidad
            self.almacen.stock -= cantidad

    def consultar_cantidad(self, producto: Producto) -> float:
        return self.almacen.productos.get(producto, 0.0)

    def avisar_nivel_minimo(self, producto: Producto, minimo: float) -> bool:
        return self.consultar_cantidad(producto) <= minimo

    def conocer_fecha(self):
        from datetime import date
        return date.today()