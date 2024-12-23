from copy import Error
from database.db_setup import get_db
from logs import logger

# Mostrar carritos
def obtener_carritos():
    conn = get_db()  # Reutilizamos la conexión gestionada por g
    cursor = conn.cursor(dictionary=True)  # Usamos dictionary=True para obtener filas como diccionarios (opcional)
    try:
        cursor.execute("SELECT * FROM Carrito")
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
        cursor.execute("SELECT * FROM Carrito WHERE id_carrito = %s", (id_carrito,))
        carrito = cursor.fetchone()
        return carrito  # Si no se encuentra, devolverá None automáticamente
    except Error as e:
        logger.error(f"Error al obtener el carrito con ID {id_carrito}: {e}")
        return None  # Indicamos que no se pudo obtener el carrito
    finally:
        cursor.close()

# Eliminar un ítem del carrito
def eliminar_item_db(id_item):
    conn = get_db()
    cursor = conn.cursor()
    try:
        query = "DELETE FROM Items WHERE id_item = %s"
        cursor.execute(query, (id_item,))
        conn.commit()
        return cursor.rowcount > 0  # Retorna True si se eliminó al menos una fila
    except Error as e:
        logger.error(f"Error al eliminar ítem con ID {id_item}: {e}")
        return False
    finally:
        cursor.close()


# Borrar un carrito completo
def borrar_carrito_db(id_carrito):
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


# Finalizar la compra de un carrito
def finalizar_compra_db(id_carrito):
    conn = get_db()
    cursor = conn.cursor()
    try:
        # Actualiza el estado del carrito a 'finalizado'
        query = "UPDATE Carrito SET estado = 'finalizado' WHERE id_carrito = %s"
        cursor.execute(query, (id_carrito,))
        conn.commit()
        return cursor.rowcount > 0  # Retorna True si se actualizó el estado
    except Error as e:
        logger.error(f"Error al finalizar la compra del carrito con ID {id_carrito}: {e}")
        return False
    finally:
        cursor.close()
