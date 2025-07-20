import sqlite3

def connect():
    try:
        conexion = sqlite3.connect("inventario.db")
        return conexion
    except sqlite3.Error as er:
        print("No se pudo conectar a la base de datos.")
        print(f"Error: {str(er)}")