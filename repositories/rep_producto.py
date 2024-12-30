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
def obtener_producto_y_categorias(conn, id_producto):
    """
    Obtiene un producto específico y todas las categorías disponibles.
    """
    try:
        # Obtener el producto por ID
        producto = obtener_producto_id(conn, id_producto)
        if not producto:
            raise ValueError(f"El producto con ID {id_producto} no existe")

        # Obtener todas las categorías
        categorias = categoriaDB.obtener_categorias(conn)
        if not categorias:
            raise ValueError("No se encontraron categorías en la base de datos")

        return producto, categorias
    except Error as e:
        logger.error(f"Error al obtener producto y categorías: {e}")
        raise

def actualizar_producto(
    id_producto, nombre_producto, descripcion, precio, imagen, id_categoria_FK
):
    conn = get_db()
    try:
        # Obtener el producto y las categorías
        categorias = obtener_producto_y_categorias(conn, id_producto)

        # Validar si el id_categoria_FK es válido
        categoria_ids = [categoria.get("id_categoria") for categoria in categorias if "id_categoria" in categoria]
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
                id_producto,
                nombre_producto,
                descripcion,
                precio,
                imagen,
                id_categoria_FK,
            ),
        )
        conn.commit()

        # Confirmar el producto actualizado (opcional)
        cursor.execute("SELECT * FROM Productos WHERE id_producto = %s", (id_producto,))
        producto_actualizado = cursor.fetchone()
        return producto_actualizado
    except Error as e:
        logger.error(f"Error al actualizar producto y categoría: {e}")
        return None  # Devolvemos None en caso de error
    finally:
        cursor.close()


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