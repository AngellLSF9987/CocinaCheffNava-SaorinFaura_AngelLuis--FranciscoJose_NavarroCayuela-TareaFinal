from copy import Error
from database.db_setup import get_db
from logs import logger


# Mostrar clientes
def obtener_clientes():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Clientes")
        clientes = cursor.fetchall()
        return clientes
    except Error as e:
        logger.error(f"Error al obtener clientes: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error

# Mostrar cliente por id
def obtener_cliente_id(id_cliente):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Clientes WHERE id_cliente = %s", (id_cliente,))

        cliente = cursor.fetchone()
        return cliente
    except Error as e:
        logger.error(f"Error al obtener cliente por ID: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error    

# Mostrar cliente por DNI
def obtener_cliente_dni(dni_cliente):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Clientes WHERE dni_cliente = %s", (dni_cliente))
        cliente = cursor.fetchone()
        return cliente
    except Error as e:
        logger.error(f"Error al obtener cliente por DNI: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error       


def borrar_cliente(id_cliente):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE 1 FROM Clientes WHERE id_cliente = %s", (id_cliente,))
        conn.commit()
    except Error as e:
        logger.error(f"Error al BORRAR cliente: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error           
