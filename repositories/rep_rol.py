from copy import Error
from database.db_setup import get_db
from logs import logger

# Mostrar roles
def obtener_roles():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Roles")
        clientes = cursor.fetchall()
        return clientes
    except Error as e:
        logger.error(f"Error al obtener roles: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error


# Mostrar rol por ID
def obtener_rol_por_id(id_rol):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Roles WHERE id_rol = %s", (id_rol,))
        rol = cursor.fetchone()
        return rol
    except Error as e:
        logger.error(f"Error al obtener rol por ID: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error    


# Mostrar rol por nombre
def obtener_rol_por_nombre(conn, nombre_rol):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Roles WHERE nombre_rol = %s", (nombre_rol,))
        rol = cursor.fetchone()
        return rol
    except Error as e:
        logger.error(f"Error al obtener rol por NOMBRE: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error
