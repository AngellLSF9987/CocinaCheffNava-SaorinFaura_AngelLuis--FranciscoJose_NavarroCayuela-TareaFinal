from copy import Error
from database.db_setup import get_db
from logs import logger

# Mostrar trabajadores
def obtener_trabajadores():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Trabajadores")
        clientes = cursor.fetchall()
        return clientes
    except Error as e:
        logger.error(f"Error al obtener trabajadores: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error    

# Mostrar trabajadores por id
def obtener_trabajador_id(id_trabajador):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT 1 FROM Trabajadores WHERE id_trabajador = %s", (id_trabajador,)
        )
        trabajador = cursor.fetchone()
        return trabajador
    except Error as e:
        logger.error(f"Error al obtener trabajador por ID: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error       

# Mostrar trabajadores por DNI
def obtener_trabajador_dni(dni_trabajador):
    conn = get_db()
    cursor = conn.cursor(dni_trabajador)
    try:
        cursor.execute(
            "SELECT 1 FROM Trabajadores WHERE dni_trabajador = %s", (dni_trabajador)
        )
        trabajador = cursor.fetchone()
        return trabajador
    except Error as e:
        logger.error(f"Error al obtener trabajador por DNI: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error     
