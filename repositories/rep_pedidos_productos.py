from copy import Error
from database.db_setup import get_db
from logs import logger


def agregar_producto_a_pedido(id_pedido, id_producto_FK, cantidad_por_producto, precio_unidad):
    """
    Agrega un producto al pedido en la tabla Pedidos_Productos.

    :param id_pedido: ID del pedido al que se le agregará el producto.
    :param id_producto_FK: ID del producto a agregar.
    :param cantidad_por_producto: Cantidad del producto.
    :param precio_unidad: Precio unitario del producto.
    :return: El ID del producto agregado, o None si hubo un error.
    """
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Pedidos_Productos (id_pedido_FK, id_producto_FK, cantidad_por_producto, precio_unidad)
            VALUES (%s, %s, %s, %s)
            """,
            (id_pedido, id_producto_FK, cantidad_por_producto, precio_unidad),
        )
        conn.commit()
        return cursor.lastrowid  # Retorna el ID del producto agregado
    except Error as e:
        logger.error(f"Error al agregar producto a pedido: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()


def actualizar_producto_pedido(id_pedido, id_producto_FK, cantidad_por_producto, precio_unidad):
    """
    Actualiza la cantidad y el precio unitario de un producto en un pedido.

    :param id_pedido: ID del pedido.
    :param id_producto_FK: ID del producto a actualizar.
    :param cantidad_por_producto: Nueva cantidad del producto.
    :param precio_unidad: Nuevo precio unitario del producto.
    :return: True si la actualización fue exitosa, False en caso contrario.
    """
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE Pedidos_Productos
            SET cantidad_por_producto = %s, precio_unidad = %s
            WHERE id_pedido_FK = %s AND id_producto_FK = %s
            """,
            (cantidad_por_producto, precio_unidad, id_pedido, id_producto_FK),
        )
        conn.commit()
        return cursor.rowcount > 0  # Si se actualizó al menos un registro
    except Error as e:
        logger.error(f"Error al actualizar producto en pedido: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()


def eliminar_producto_pedido(id_pedido, id_producto_FK):
    """
    Elimina un producto de un pedido.

    :param id_pedido: ID del pedido.
    :param id_producto_FK: ID del producto a eliminar.
    :return: True si la eliminación fue exitosa, False en caso contrario.
    """
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM Pedidos_Productos
            WHERE id_pedido_FK = %s AND id_producto_FK = %s
            """,
            (id_pedido, id_producto_FK),
        )
        conn.commit()
        return cursor.rowcount > 0  # Si se eliminó al menos un registro
    except Error as e:
        logger.error(f"Error al eliminar producto de pedido: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()


def obtener_productos_por_pedido(id_pedido):
    """
    Obtiene todos los productos asociados a un pedido.

    :param id_pedido: ID del pedido.
    :return: Una lista de diccionarios con los productos del pedido.
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT pr.id_producto, pr.nombre_producto, pr.precio_unidad, pp.cantidad_por_producto
            FROM Pedidos_Productos pp
            INNER JOIN Productos pr ON pp.id_producto_FK = pr.id_producto
            WHERE pp.id_pedido_FK = %s
            """,
            (id_pedido,),
        )
        productos = cursor.fetchall()
        return productos
    except Error as e:
        logger.error(f"Error al obtener productos de pedido: {e}")
        return []  # Retornar una lista vacía en caso de error
    finally:
        cursor.close()


def eliminar_productos_por_pedido(id_pedido):
    """
    Elimina todos los productos asociados a un pedido.

    :param id_pedido: ID del pedido.
    :return: True si la eliminación fue exitosa, False en caso contrario.
    """
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM Pedidos_Productos WHERE id_pedido_FK = %s
            """,
            (id_pedido,),
        )
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        logger.error(f"Error al eliminar productos de pedido: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
