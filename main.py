from conexion import obtener_conexion
from codigo import Direccion, Categoria, Producto, Almacen, Inventario, Proveedor

def ejecutar():
    print("Iniciando prueba completa...")
    conexion = obtener_conexion()

    if conexion:
        try:
            # 1. Crear y guardar Dirección
            dir1 = Direccion(456, "Aníbal Pinto", "Concepción", "Biobío")
            dir1.guardar(conexion)
            print(f"Dirección guardada con ID: {dir1.id_direccion}")

            # 2. Crear y guardar Categoría
            cat1 = Categoria("Bebidas", "Jugos y gaseosas")
            cat1.guardar(conexion)
            print(f"Categoría guardada con ID: {cat1.id_categoria}")

            # 3. Crear y guardar Almacén
            almacen1 = Almacen("Bodega Concepción", dir1)
            almacen1.guardar(conexion)
            print(f"Almacén guardado con ID: {almacen1.id_almacen}")

            # 4. Crear y guardar Producto
            prod1 = Producto("Jugo de Naranja 1L", "7801234567890", "Jugo natural", 1500.0, cat1)
            prod1.guardar(conexion)
            print(f"Producto '{prod1.nombre}' guardado exitosamente.")

            # 5. Asociar Producto al Almacén
            almacen1.registrar_producto(prod1, 100.0, conexion)

            # 6. Probar Proveedor
            prov1 = Proveedor("12345678-9", "Distribuidora del Sur", "contacto@delsur.cl", dir1)
            prov1.guardar(conexion)
            prov1.entregar_producto(prod1, conexion)

            # 7. Operaciones de Inventario
            inv = Inventario(almacen1)
            print(f"Fecha de operación: {inv.conocer_fecha()}")
            print(f"Stock de {prod1.nombre}: {inv.consultar_cantidad(prod1)}")

        except Exception as e:
            print(f"Error durante el proceso: {e}")
        finally:
            conexion.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    ejecutar()