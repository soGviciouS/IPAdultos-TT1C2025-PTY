import sqlite3
import database

def init(seeding=False):
    conn = database.connect()
    conn.execute("BEGIN TRANSACTION")
    try:
        # Table creation
        tbl_create = "create table IF NOT EXISTS productos ( \
                id INTEGER PRIMARY KEY AUTOINCREMENT, \
                nombre      TEXT    not null, \
                descripcion TEXT, \
                cantidad    integer not null, \
                precio      REAL    not null, \
                categoria   TEXT \
            );"
        conn.execute(tbl_create)

        if seeding:
            # Seeding table
            conn.execute("INSERT INTO productos VALUES (NULL, 'Leche', 'Leche frita', 100, 1.5, 'Lacteo')")
            conn.execute("INSERT INTO productos VALUES (NULL, 'Queso', 'Queso Gruyere', 100, 2.5, 'Lacteo')")
            conn.execute("INSERT INTO productos VALUES (NULL, 'Pollo', 'Pollo Entero', 100, 3.5, 'Carniceria')")
            conn.execute("INSERT INTO productos VALUES (NULL, 'Pescado', 'Pescado Fresco', 100, 4.5, 'Pescaderia')")

        conn.commit()
    except sqlite3.Error as er:
        conn.rollback()
        print("No se pudo generar la tabla.")
        print(f"Error: {str(er)}")

    finally:
        conn.close()

def add_product(arg_nombre, arg_descripcion, arg_cantidad, arg_precio, arg_categoria):
    conn = database.connect()
    try:
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos VALUES (NULL, ?, ?, ?, ?, ?)", (arg_nombre, arg_descripcion, arg_cantidad, arg_precio, arg_categoria))
        conn.commit()
    except sqlite3.Error as er:
        conn.rollback()
        print("No se pudo agregar el producto.")
    finally:
        conn.close()

def show_products():
    conn = database.connect()
    try:
        conn.row_factory = sqlite3.Row  # Habilita acceso a columnas por nombre
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM productos")
        filas = cursor.fetchall()

        # Convertir a lista de diccionarios
        productos = [dict(fila) for fila in filas]

        return productos
    except sqlite3.Error as e:
        print("Error al consultar la base de datos:", e)
        return []
    finally:
        conn.close()

def show_product(product_findKey):
    conn = database.connect()
    try:
        conn.row_factory = sqlite3.Row  # Habilita acceso a columnas por nombre
        cursor = conn.cursor()
        if product_findKey.isnumeric():
            product_findKey = int(product_findKey)
            cursor.execute("SELECT * FROM productos WHERE id = ?", (product_findKey,))
            # fila = cursor.fetchall()
            # producto = dict(fila) if fila else []
            rows = cursor.fetchall()
            producto = [dict(row) for row in rows]

        else:
            product_findKey = f"%{product_findKey}%"
            cursor.execute("SELECT * FROM productos WHERE nombre LIKE ? OR categoria LIKE ?", (product_findKey, product_findKey))
            rows = cursor.fetchall()
            producto = [dict(row) for row in rows]

        return producto

    except sqlite3.Error as e:
        print("Error al consultar la base de datos:", e)
        return []
    finally:
        conn.close()

def mod_product(arg_id, arg_nombre, arg_descripcion, arg_cantidad, arg_precio, arg_categoria):
        conn = database.connect()
        try:
            conn.execute("BEGIN TRANSACTION")
            # Verificar si el producto existe
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM productos WHERE id = ?", (arg_id,))
            if not cursor.fetchone():
                print(f"No se encontró un producto con ID {id}.")
                return False

            # Ejecutar la actualización
            cursor.execute("""
                           UPDATE productos
                           SET nombre      = ?,
                               descripcion = ?,
                               cantidad    = ?,
                               precio      = ?,
                               categoria   = ?
                           WHERE id = ?
                           """, (arg_nombre, arg_descripcion, arg_cantidad, arg_precio, arg_categoria, arg_id))

            conn.commit()
            print(f"Producto con ID {arg_id} actualizado correctamente.")
            conn.commit()
        except sqlite3.Error as er:
            conn.rollback()
            print("No se pudo Modificar el producto.")
        finally:
            conn.close()

def remove_product(productid):
    conn = database.connect()
    try:
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (productid,))
        conn.commit()
        print("Se eliminó el producto.")
    except sqlite3.Error as er:
        conn.rollback()
        print("No se pudo eliminar el producto.")
    finally:
        conn.close()

def report_products(minCant):
    conn = database.connect()
    try:
        conn.row_factory = sqlite3.Row  # Habilita acceso a columnas por nombre
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (minCant, ))
        filas = cursor.fetchall()

        # Convertir a lista de diccionarios
        productos = [dict(fila) for fila in filas]

        return productos
    except sqlite3.Error as e:
        print("Error al consultar la base de datos:", e)
        return []
    finally:
        conn.close()