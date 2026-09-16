from conexion import obtener_conexion
from codigo import Direccion, Categoria, Producto, Almacen, Inventario, Proveedor


def consultar_datos_bd(conexion):
    cursor = conexion.cursor()
    while True:
        print("\n" + "=" * 50)
        print("      CONSULTAS DE LA BASE DE DATOS (MYSQL)")
        print("=" * 50)
        print("1. Ver todas las Direcciones")
        print("2. Ver todas las Categorías")
        print("3. Ver todos los Proveedores")
        print("4. Ver todos los Productos")
        print("5. Ver todos los Almacenes")
        print("6. Ver Productos en Almacenes (Stock)")
        print("7. Ver Proveedores por Producto")
        print("8. Volver al Menú Principal")
        print("=" * 50)

        sub_op = input("Selecciona una opción de consulta (1-8): ")

        if sub_op == "1":
            cursor.execute("SELECT id_direccion, numero_lugar, calle, comuna, region FROM direccion")
            filas = cursor.fetchall()
            print("\n--- DIRECCIONES ---")
            for f in filas:
                print(f"ID: {f[0]} | Calle: {f[2]} #{f[1]}, {f[3]} ({f[4]})")

        elif sub_op == "2":
            cursor.execute("SELECT id_categoria, nombre, descripcion FROM categoria")
            filas = cursor.fetchall()
            print("\n--- CATEGORÍAS ---")
            for f in filas:
                print(f"ID: {f[0]} | Nombre: {f[1]} | Descripción: {f[2]}")

        elif sub_op == "3":
            cursor.execute("SELECT rut, nombre, correo, fk_id_direccion FROM proveedor")
            filas = cursor.fetchall()
            print("\n--- PROVEEDORES ---")
            for f in filas:
                print(f"RUT: {f[0]} | Nombre: {f[1]} | Correo: {f[2]} | ID Dirección: {f[3]}")

        elif sub_op == "4":
            cursor.execute("SELECT gtin, nombre_producto, descripcion_producto, precio_compra FROM producto")
            filas = cursor.fetchall()
            print("\n--- PRODUCTOS ---")
            for f in filas:
                print(f"GTIN: {f[0]} | Nombre: {f[1]} | Precio: ${f[3]} | Desc: {f[2]}")

        elif sub_op == "5":
            cursor.execute("SELECT id_almacen, nombre, fk_direccion FROM almacen")
            filas = cursor.fetchall()
            print("\n--- ALMACENES ---")
            for f in filas:
                print(f"ID: {f[0]} | Nombre: {f[1]} | ID Dirección: {f[2]}")

        elif sub_op == "6":
            query = """
                SELECT a.nombre, p.nombre_producto, pa.stock 
                FROM producto_almacen pa
                JOIN almacen a ON pa.fk_id_almacen = a.id_almacen
                JOIN producto p ON pa.fk_gtin = p.gtin
            """
            cursor.execute(query)
            filas = cursor.fetchall()
            print("\n--- STOCK EN ALMACENES (RELACIÓN N:M) ---")
            for f in filas:
                print(f"Almacén: {f[0]} | Producto: {f[1]} | Stock: {f[2]}")

        elif sub_op == "7":
            query = """
                SELECT pr.nombre, p.nombre_producto 
                FROM proveedores_producto pp
                JOIN proveedor pr ON pp.fk_id_proveedor = pr.rut
                JOIN producto p ON pp.fk_gtin = p.gtin
            """
            cursor.execute(query)
            filas = cursor.fetchall()
            print("\n--- PROVEEDORES POR PRODUCTO (RELACIÓN N:M) ---")
            for f in filas:
                print(f"Proveedor: {f[0]} ---> Producto Suministrado: {f[1]}")

        elif sub_op == "8":
            break
        else:
            print("❌ Opción inválida.")

    cursor.close()


def mostrar_menu():
    print("\n" + "=" * 50)
    print("      SISTEMA DE GESTIÓN DE INVENTARIO Y BODEGA")
    print("=" * 50)
    print("1. Registrar Dirección")
    print("2. Registrar Categoría")
    print("3. Registrar Proveedor")
    print("4. Registrar Producto (asociado a Categoría)")
    print("5. Registrar Almacén (asociado a Dirección)")
    print("6. Asociar Proveedor a Producto (entregar_producto)")
    print("7. Asociar Producto a Almacén (registrar_producto)")
    print("8. Gestionar Inventario (Sumar / Restar / Consultar Stock)")
    print("9. 🔍 CONSULTAR TODO EN LA BASE DE DATOS (SELECT)")
    print("10. Salir")
    print("=" * 50)


def ejecutar_menu():
    conexion = obtener_conexion()
    if not conexion:
        print("Error: No se pudo conectar a la base de datos.")
        return

    direcciones = {}
    categorias = {}
    proveedores = {}
    productos = {}
    almacenes = {}

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1-10): ")

        if opcion == "1":
            print("\n--- 1. REGISTRAR DIRECCIÓN ---")
            calle = input("Calle: ")
            numero = int(input("Número: "))
            comuna = input("Comuna: ")
            region = input("Región: ")

            d = Direccion(numero, calle, comuna, region)
            d.guardar(conexion)
            direcciones[d.id_direccion] = d
            print(f"✅ Dirección ID {d.id_direccion} guardada correctamente.")

        elif opcion == "2":
            print("\n--- 2. REGISTRAR CATEGORÍA ---")
            nombre = input("Nombre: ")
            desc = input("Descripción: ")

            c = Categoria(nombre, desc)
            c.guardar(conexion)
            categorias[c.id_categoria] = c
            print(f"✅ Categoría ID {c.id_categoria} guardada correctamente.")

        elif opcion == "3":
            print("\n--- 3. REGISTRAR PROVEEDOR ---")
            if not direcciones:
                print("⚠️ Debe registrar primero al menos una Dirección.")
                continue

            rut = input("RUT Proveedor: ")
            nombre = input("Nombre / Razón Social: ")
            correo = input("Correo electrónico: ")
            id_dir = int(input(f"ID Dirección asociada {list(direcciones.keys())}: "))

            if id_dir in direcciones:
                p = Proveedor(rut, nombre, correo, direcciones[id_dir])
                p.guardar(conexion)
                proveedores[rut] = p
                print(f"✅ Proveedor '{nombre}' guardado correctamente.")
            else:
                print("❌ ID de Dirección no válido.")

        elif opcion == "4":
            print("\n--- 4. REGISTRAR PRODUCTO ---")
            if not categorias:
                print("⚠️ Debe registrar primero al menos una Categoría.")
                continue

            gtin = input("Código GTIN: ")
            nombre = input("Nombre del Producto: ")
            desc = input("Descripción: ")
            precio = float(input("Precio de compra: "))
            id_cat = int(input(f"ID Categoría asociada {list(categorias.keys())}: "))

            if id_cat in categorias:
                prod = Producto(nombre, gtin, desc, precio, categorias[id_cat])
                prod.guardar(conexion)
                productos[gtin] = prod
                print(f"✅ Producto '{nombre}' guardado exitosamente.")
            else:
                print("❌ ID de Categoría no válido.")

        elif opcion == "5":
            print("\n--- 5. REGISTRAR ALMACÉN ---")
            if not direcciones:
                print("⚠️ Debe registrar primero al menos una Dirección.")
                continue

            nombre = input("Nombre del Almacén: ")
            id_dir = int(input(f"ID Dirección asociada {list(direcciones.keys())}: "))

            if id_dir in direcciones:
                alm = Almacen(nombre, direcciones[id_dir])
                alm.guardar(conexion)
                almacenes[alm.id_almacen] = alm
                print(f"✅ Almacén ID {alm.id_almacen} guardado exitosamente.")
            else:
                print("❌ ID de Dirección no válido.")

        elif opcion == "6":
            print("\n--- 6. ASOCIAR PROVEEDOR A PRODUCTO ---")
            if not proveedores or not productos:
                print("⚠️ Requiere al menos un Proveedor y un Producto registrados.")
                continue

            rut = input(f"RUT Proveedor {list(proveedores.keys())}: ")
            gtin = input(f"GTIN Producto {list(productos.keys())}: ")

            if rut in proveedores and gtin in productos:
                proveedores[rut].entregar_producto(productos[gtin], conexion)
                print(f"✅ Relación vinculada en la BD (proveedores_producto).")
            else:
                print("❌ RUT o GTIN no encontrado.")

        elif opcion == "7":
            print("\n--- 7. ASOCIAR PRODUCTO A ALMACÉN ---")
            if not almacenes or not productos:
                print("⚠️ Requiere al menos un Almacén y un Producto registrados.")
                continue

            id_alm = int(input(f"ID Almacén {list(almacenes.keys())}: "))
            gtin = input(f"GTIN Producto {list(productos.keys())}: ")
            stock_inicial = float(input("Stock inicial para este producto en el almacén: "))

            if id_alm in almacenes and gtin in productos:
                almacenes[id_alm].registrar_producto(productos[gtin], stock_inicial, conexion)
                print(f"✅ Producto registrado en Almacén en la BD (producto_almacen).")
            else:
                print("❌ Almacén o GTIN no encontrado.")

        elif opcion == "8":
            print("\n--- 8. GESTIONAR INVENTARIO ---")
            if not almacenes:
                print("⚠️ No hay Almacenes disponibles.")
                continue

            id_alm = int(input(f"ID Almacén a inspeccionar {list(almacenes.keys())}: "))
            if id_alm in almacenes:
                inv = Inventario(almacenes[id_alm])
                print(f"📅 Fecha del Inventario: {inv.conocer_fecha()}")
                print("1. Consultar Stock de Producto")
                print("2. Sumar Stock")
                print("3. Restar Stock")
                sub_op = input("Seleccione sub-opción (1-3): ")

                gtin = input(f"GTIN Producto {list(productos.keys())}: ")
                if gtin in productos:
                    prod = productos[gtin]
                    if sub_op == "1":
                        cant = inv.consultar_cantidad(prod)
                        print(f"📦 Stock actual de '{prod.nombre}': {cant}")
                        if inv.avisar_nivel_minimo(prod, 5.0):
                            print("⚠️ ALERTA: Nivel crítico de stock (<= 5).")

                    elif sub_op == "2":
                        cant = float(input("Cantidad a sumar: "))
                        inv.sumar_producto(prod, cant)
                        print(f"✅ Nuevo stock local: {inv.consultar_cantidad(prod)}")

                    elif sub_op == "3":
                        cant = float(input("Cantidad a restar: "))
                        inv.restar_producto(prod, cant)
                        print(f"✅ Nuevo stock local: {inv.consultar_cantidad(prod)}")
            else:
                print("❌ ID de Almacén no existe.")

        elif opcion == "9":
            consultar_datos_bd(conexion)

        elif opcion == "10":
            conexion.close()
            print("\n👋 Conexión cerrada. ¡Hasta luego!")
            break

        else:
            print("❌ Opción no válida.")


if __name__ == "__main__":
    ejecutar_menu()