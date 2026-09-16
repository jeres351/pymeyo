import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="jere",             # Cambia si usas otro usuario
            password="1324",   # Cambia por tu contraseña de MySQL
            database="pyme"  # Cambia por el nombre de tu BD
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None