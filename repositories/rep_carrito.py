from copy import Error
from database.db_setup import get_db
from logs import logger

# Mostrar carritos
def obtener_carritos():
    conn = get_db()  # Reutilizamos la conexión gestionada por g
    cursor = conn.cursor(dictionary=True)  # Usamos dictionary=True para obtener filas como diccionarios
    try:
        cursor.execute("""
            SELECT c.id_carrito, c.id_cliente_FK, c.id_producto_FK, c.cantidad_por_producto, c.precio_carrito, p.nombre AS producto_nombre
            FROM Carrito c
            JOIN Productos p ON c.id_producto_FK = p.id_producto
        """)
        carritos = cursor.fetchall()
        return carritos  # Devolvemos una lista de carritos
    except Error as e:
        logger.error(f"Error al obtener carritos: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error


# Mostrar carrito por ID
def obtener_carrito_id(id_carrito):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT c.id_carrito, c.id_cliente_FK, c.id_producto_FK, c.cantidad_por_producto, c.precio_carrito, p.nombre AS producto_nombre
            FROM Carrito c
            JOIN Productos p ON c.id_producto_FK = p.id_producto
            WHERE c.id_carrito = %s
        """, (id_carrito,))
        carrito = cursor.fetchone()
        return carrito  # Si no se encuentra, devolverá None automáticamente
    except Error as e:
        logger.error(f"Error al obtener el carrito con ID {id_carrito}: {e}")
        return None  # Indicamos que no se pudo obtener el carrito
    finally:
        cursor.close()


def obtener_total_carrito(id_cliente_FK):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT SUM(c.cantidad_por_producto * c.precio_carrito) AS total_carrito
            FROM Carrito c
            WHERE c.id_cliente_FK = %s
        """, (id_cliente_FK,))
        resultado = cursor.fetchone()
        return resultado['total_carrito'] if resultado else 0
    except Error as e:
        logger.error(f"Error al obtener el total del carrito del cliente {id_cliente_FK}: {e}")
        return 0
    finally:
        cursor.close()


def agregar_producto_carrito(id_cliente_FK, id_producto_FK, cantidad_por_producto, precio_carrito):
    conn = get_db()
    cursor = conn.cursor()
    try:
        # Verificamos si el producto ya existe en el carrito del cliente
        cursor.execute("""
            SELECT id_carrito FROM Carrito
            WHERE id_cliente_FK = %s AND id_producto_FK = %s
        """, (id_cliente_FK, id_producto_FK))
        carrito = cursor.fetchone()

        if carrito:  # Si ya existe, actualizamos la cantidad
            id_carrito = carrito['id_carrito']
            cursor.execute("""
                UPDATE Carrito
                SET cantidad_por_producto = cantidad_por_producto + %s, precio_carrito = %s
                WHERE id_carrito = %s
            """, (cantidad_por_producto, precio_carrito, id_carrito))
            logger.info(f"✔️ Producto {id_producto_FK} actualizado en el carrito del cliente {id_cliente_FK}.")
        else:  # Si no existe, insertamos un nuevo registro
            cursor.execute("""
                INSERT INTO Carrito (id_cliente_FK, id_producto_FK, cantidad_por_producto, precio_carrito)
                VALUES (%s, %s, %s, %s)
            """, (id_cliente_FK, id_producto_FK, cantidad_por_producto, precio_carrito))
            logger.info(f"✔️ Producto {id_producto_FK} añadido al carrito del cliente {id_cliente_FK}.")
        
        conn.commit()
        return True
    except Error as e:
        logger.error(f"Error al agregar el producto al carrito: {e}")
        return False
    finally:
        cursor.close()


def actualizar_cantidad_producto(id_carrito, nueva_cantidad, nuevo_precio_carrito):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE Carrito
            SET cantidad_por_producto = %s, precio_carrito = %s
            WHERE id_carrito = %s
        """, (nueva_cantidad, nuevo_precio_carrito, id_carrito))
        conn.commit()
        if cursor.rowcount > 0:
            logger.info(f"✔️ Cantidad de producto en el carrito {id_carrito} actualizada.")
            return True
        else:
            logger.warning(f"⚠️ No se encontró el carrito con ID {id_carrito}.")
            return False
    except Error as e:
        logger.error(f"Error al actualizar la cantidad del producto en el carrito: {e}")
        return False
    finally:
        cursor.close()


def eliminar_producto_carrito(id_cliente_FK, id_producto_FK):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM Carrito
            WHERE id_cliente_FK = %s AND id_producto_FK = %s
        """, (id_cliente_FK, id_producto_FK))
        conn.commit()
        if cursor.rowcount > 0:
            logger.info(f"✔️ Producto {id_producto_FK} eliminado del carrito del cliente {id_cliente_FK}.")
            return True
        else:
            logger.warning(f"⚠️ El producto {id_producto_FK} no existe en el carrito del cliente {id_cliente_FK}.")
            return False
    except Error as e:
        logger.error(f"Error al eliminar el producto del carrito: {e}")
        return False
    finally:
        cursor.close()

def vaciar_carrito(id_cliente_FK):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM Carrito
            WHERE id_cliente_FK = %s
        """, (id_cliente_FK,))
        conn.commit()
        logger.info(f"✔️ Carrito del cliente {id_cliente_FK} vaciado.")
        return True
    except Error as e:
        logger.error(f"Error al vaciar el carrito del cliente {id_cliente_FK}: {e}")
        return False
    finally:
        cursor.close()


# Borrar un carrito completo
def borrar_carrito(id_carrito):
    conn = get_db()
    cursor = conn.cursor()
    try:
        query = "DELETE FROM Carrito WHERE id_carrito = %s"
        cursor.execute(query, (id_carrito,))
        conn.commit()
        return cursor.rowcount > 0  # Retorna True si se eliminó el carrito
    except Error as e:
        logger.error(f"Error al borrar el carrito con ID {id_carrito}: {e}")
        return False
    finally:
        cursor.close()
