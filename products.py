import sqlite3
import database

def init(seeding=False):
    """
    Inicializa la base de datos creando la tabla `productos` si no existe y, opcionalmente, siembra la tabla con datos iniciales.

    :param seeding: Determina si se deben insertar registros de ejemplo en la tabla `productos` después de su creación.
    :type seeding: bool
    :return: None
    """
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

def show_products():
    """
    Obtiene y devuelve una lista de todos los productos de la base de datos.

    :rtype: list[dict]
    :return: Una lista de diccionarios que representan los productos, o una lista vacía si se produce un error
        durante la consulta de la base de datos.
    """
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
    """
    Recuperar información de productos de la base de datos a partir de una clave de búsqueda dada. La clave de búsqueda puede ser
        un ID (numérico) o una cadena que coincida con el nombre o la categoría del producto.

    :param product_findKey: La clave utilizada para buscar productos en la base de datos. Puede ser un ID numérico
        o una cadena utilizada para buscar nombres de productos o categorías.
    :return: Una lista de diccionarios que contienen información sobre los productos de la consulta, o una lista vacía si se produce un error en
        o no se encuentra ninguna coincidencia.
    """
    conn = database.connect()
    try:
        conn.row_factory = sqlite3.Row  # Habilita acceso a columnas por nombre
        cursor = conn.cursor()
        if product_findKey.isnumeric():
            product_findKey = int(product_findKey)
            cursor.execute("SELECT * FROM productos WHERE id = ?", (product_findKey,))
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

def add_product(arg_nombre, arg_descripcion, arg_cantidad, arg_precio, arg_categoria):
    """
        Añade un producto a la base de datos con los detalles proporcionados.


    :param arg_nombre: Nombre del producto.
    :type arg_nombre: str
    :param arg_descripcion: Descripción del producto.
    :type arg_descripcion: str
    :param arg_cantidad: Cantidad del producto.
    :type arg_cantidad: int
    :param arg_precio: Precio del producto.
    :type arg_precio: float
    :param arg_categoria: Categoria del producto.
    :type arg_categoria: str
    :return: None
    """

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

def mod_product(arg_nombre, arg_descripcion, arg_cantidad, arg_precio, arg_categoria, arg_id):
    """
    Actualiza los detalles de un producto en la base de datos con los argumentos proporcionados. Si el ID del producto
     no existe, la función registra un mensaje apropiado y sale. La función garantiza la integridad transaccional de la base de datos
     consignando los datos sólo cuando no se producen excepciones, y
     deshaciendo los cambios ante cualquier error de la base de datos.

    :param arg_nombre: Nombre del producto.
    :type arg_nombre: str
    :param arg_descripcion: Descripción del producto.
    :type arg_descripcion: str
    :param arg_cantidad: Cantidad del producto.
    :type arg_cantidad: int
    :param arg_precio: Precio del producto.
    :type arg_precio: float
    :param arg_categoria: Categoria del producto.
    :type arg_categoria: str
    :param arg_id: ID del producto.
    :type arg_id: int
    :return: True si el producto se ha actualizado correctamente, False en caso contrario
    :rtype: bool
    """

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
    """
    Elimina un producto de la base de datos basándose en su identificador.

    :param productid: The identifier of the product to be removed.
    :type productid: Any
    :return: None
    """
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
    """
    Obtiene y devuelve una lista de productos de la base de datos con una cantidad inferior o igual al limite especificado

    :param int minCant: El limite de cantidad mínima por el que filtrar los productos.
    :return: Una lista de diccionarios donde cada diccionario representa un producto con atributos como claves
    y sus valores correspondientes.
    :rtype: list[dict]
    """

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

def validate_product(arg_id=None):

    """
    Valida y recoge los datos de entrada de un producto por parte del usuario. La función garantiza que todos los campos de
        proporcionados por el usuario cumplen los criterios especificados,

    :param arg_id: Optional; ID del producto a validar. Debe ser un valor numérico, si se proporciona.
    :type arg_id: Optional[int]

    :returns: Una tupla que contiene detalles del producto: nombre del producto, descripción, cantidad, precio, categoría,
        y opcionalmente el ID del producto si se proporciona `arg_id`. Los campos de la tupla devuelta, en orden,
        son:
              - productName (str): Nombre del producto. No puede estar vacío.
              - productDescription (cadena): Descripción del producto. Puede estar vacío.
              - productCant (int): Cantidad del producto. Debe ser un número entero y no estar vacío.
              - productPrice (float): Precio del producto. Debe ser un flotador positivo o un entero.
              - productCategory (cadena): Categoría del producto. No puede estar vacío.
              - productID (int, opcional): ID del producto, sólo se incluye si `arg_id` no es None.

    :rtype: tuple
    """

    if arg_id is not None:
        productID = input("Ingrese el ID del producto: ")
    productName = input("Ingrese el nombre del producto: ")
    productDescription = input("Ingrese la descripción del producto: ")
    productCant = input("Ingrese la cantidad del producto (número entero): ")
    productPrice = input("Ingrese el precio del producto (número decimal positivo:): ")
    productCategory = input("Ingrese la categoria del producto: ")

    try:
        if arg_id is not None:
            if not productID.isnumeric():
                raise ValueError("La ID debe ser un número entero positivo.")
            else:
                productID = int(productID)
        if productName != "":
            productName = productName.strip()
        if productDescription != "":
            productDescription = productDescription.strip()
        if productCant != "":
            productCant = productCant
        if productPrice != "":
            productPrice = float(productPrice)
        if productCategory != "":
            productCategory = productCategory.strip()
        if productName == "":
            raise ValueError("El nombre no puede estar vacío.")
        if productCategory == "":
            raise ValueError("La categoría no puede estar vacía.")
        if not productCant.isnumeric():
            raise ValueError("La cantidad debe ser un número entero positivo.")
        else:
            productCant = int(productCant)

        if arg_id is not None:
            return productName, productDescription, productCant, productPrice, productCategory, productID
        else:
            return productName, productDescription, productCant, productPrice, productCategory

    except ValueError as e:
        print(e, "Intente de nuevo. \n")

def show_product(arg_nombre, arg_descripcion, arg_cantidad, arg_precio, arg_categoria, arg_id=None):

    """
        If arg_id is not None, it will return the productID, productName, productDescription, productCant, productPrice, productCategory.
            else, it will return the productName, productDescription, productCant, productPrice, productCategory, productID.

        :param arg_nombre:
        :param arg_descripcion:
        :param arg_cantidad:
        :param arg_precio:
        :param arg_categoria:
        :param arg_id:

        :return: []
    """

    print(f" \
            Producto #{arg_id}: \n \
            - Nombre: {arg_nombre}\n \
            - Descripción: {arg_descripcion}\n \
            - Cantidad: {arg_cantidad}\n \
            - Precio: {arg_precio} \n \
            - Categoría: {arg_categoria} \
    ")