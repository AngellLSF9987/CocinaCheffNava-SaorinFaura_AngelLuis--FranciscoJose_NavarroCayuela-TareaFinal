import repositories.rep_categoria as categoriaDB

from copy import Error
from database.db_setup import get_db
from logs import logger


# Obtener todos los productos
def obtener_productos():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT p.id_producto, p.nombre_producto, p.descripcion, p.precio, p.imagen, 
                c.nombre_categoria 
            FROM Productos p
            INNER JOIN Categorias c ON p.id_categoria_FK = c.id_categoria
            """
        )
        productos = cursor.fetchall()
        # Convertir a una lista de diccionarios para facilitar el manejo en templates
        return [
            {
                "id_producto": producto["id_producto"],
                "nombre_producto": producto["nombre_producto"],
                "descripcion": producto["descripcion"],
                "precio": producto["precio"],
                "imagen": producto["imagen"],
                "nombre_categoria": producto["nombre_categoria"],
            }
            for producto in productos
        ]
    except Error as e:
        logger.error(f"Error al obtener productos: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error


# Obtener producto por ID
def obtener_producto_id(id_producto):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT p.id_producto, p.nombre_producto, p.descripcion, p.precio, p.imagen, 
                c.nombre_categoria AS nombre_categoria
            FROM Productos p
            INNER JOIN Categorias c ON p.id_categoria_FK = c.id_categoria
            WHERE p.id_producto = %s
            """,
            (id_producto,),
        )
        producto = cursor.fetchone()
        if not producto:
            return None
        else:
            logger.info(f"Producto obtenido: {producto}")
            return producto
    except Error as e:
        logger.error(f"Error al obtener producto por ID: {e}")
        return None  # Devolver None en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error


# Crear producto
def crear_producto(nombre, descripcion, precio, imagen, id_categoria_FK):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Productos (nombre_producto, descripcion, precio, imagen, id_categoria_FK) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            (nombre, descripcion, precio, imagen, id_categoria_FK),
        )
        conn.commit()
        logger.info("Producto creado exitosamente.")
        return cursor.lastrowid  # Devuelve el ID del producto creado
    except Error as e:
        logger.error(f"Error al crear producto: {e}")
        return None  # Retorna None en caso de error
    finally:
        cursor.close()


# Modificar producto con categorías
def obtener_producto_y_categorias(id_producto, id_categoria_FK, id_categoria):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        producto = obtener_producto_id(conn, id_producto, id_categoria_FK)
        categorias = categoriaDB.obtener_categorias(conn, id_categoria)
        return producto, categorias
    except Error as e:
        logger.error(f"Error al obtener producto y categoria: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error


# Modificar categoria
def actualizar_producto(
    id_producto, nombre_producto, descripcion, precio, imagen, id_categoria_FK
):
    conn = get_db()
    try:
        # Obtener el producto y las categorías
        producto, categorias = obtener_producto_y_categorias(conn, id_producto)

        # Validar si el id_categoria_FK es válido
        categoria_ids = [
            categoria["id_categoria"] for categoria in categorias
        ]  # Suponiendo que 'id_categoria' es la clave del ID de cada categoría
        if id_categoria_FK not in categoria_ids:
            raise ValueError(f"El id_categoria_FK {id_categoria_FK} no es válido")

        # Realizar la actualización
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            UPDATE Productos 
            SET nombre_producto = %s, descripcion = %s, precio = %s, imagen = %s, id_categoria_FK = %s
            WHERE id_producto = %s
            """,
            (
                nombre_producto,
                descripcion,
                precio,
                imagen,
                id_categoria_FK,
                producto["id_producto"],
            ),  # Suponiendo que 'id_producto' es la clave del producto
        )
        conn.commit()
    except Error as e:
        logger.error(f"Error al actualizar producto y categoria: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error


# Borrar producto
def borrar_producto(id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Productos WHERE id_producto=%s", (id,))
        conn.commit()
    except Error as e:
        logger.error(f"Error al borrar: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error
