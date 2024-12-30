from copy import Error
import database.db_setup as setupDB
from logs import logger
from repositories.rep_usuario import crear_usuario


# Mostrar trabajadores
def obtener_trabajadores():
    conn = setupDB.get_db()
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
    conn = setupDB.get_db()
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
    conn = setupDB.get_db()
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

def crear_trabajador(nombre_trabajador, apellido1, apellido2, dni_trabajador, telefono, direccion, email, rol_trabajador):
    conn = setupDB.get_db()
    cursor = conn.cursor()
    try:
        # Primero, creamos el usuario (esto ya se encuentra en el repositorio de usuarios)
        id_usuario = crear_usuario(email, rol_trabajador)

        if not id_usuario:
            raise ValueError("No se pudo crear el usuario para el trabajador.")

        # Luego, insertamos al trabajador y asociamos el id_usuario_FK
        cursor.execute(
            """
            INSERT INTO Trabajadores (nombre_trabajador, apellido1, apellido2, dni_trabajador, telefono, direccion, email, id_usuario_FK)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (nombre_trabajador, apellido1, apellido2, dni_trabajador, telefono, direccion, email, id_usuario),
        )
        conn.commit()
        logger.info("Trabajador creado exitosamente.")
    except Error as e:
        logger.error(f"Error al crear trabajador: {e}")
        conn.rollback()
    finally:
        cursor.close()
        
def actualizar_trabajador(id_trabajador, nombre_trabajador=None, apellido1=None, apellido2=None, dni_trabajador=None, telefono=None, direccion=None, email=None, id_usuario_FK=None):
    conn = setupDB.get_db()
    cursor = conn.cursor()
    try:
        # Construimos dinámicamente la consulta de actualización
        campos = []
        valores = []
        
        if nombre_trabajador:
            campos.append("nombre_trabajador = %s")
            valores.append(nombre_trabajador)
        if apellido1:
            campos.append("apellido1 = %s")
            valores.append(apellido1)
        if apellido2:
            campos.append("apellido2 = %s")
            valores.append(apellido2)
        if dni_trabajador:
            campos.append("dni_trabajador = %s")
            valores.append(dni_trabajador)
        if telefono:
            campos.append("telefono = %s")
            valores.append(telefono)
        if direccion:
            campos.append("direccion = %s")
            valores.append(direccion)
        if email:
            campos.append("email = %s")
            valores.append(email)
        if id_usuario_FK:
            campos.append("id_usuario_FK = %s")
            valores.append(id_usuario_FK)

        if not campos:
            raise ValueError("No se proporcionaron campos para actualizar.")
        
        sql = f"UPDATE Trabajadores SET {', '.join(campos)} WHERE id_trabajador = %s"
        valores.append(id_trabajador)
        
        cursor.execute(sql, tuple(valores))
        conn.commit()
        return cursor.rowcount  # Devuelve el número de filas afectadas
    except Error as e:
        logger.error(f"Error al actualizar trabajador: {e}")
        return None  # Devolvemos None en caso de error
    finally:
        cursor.close()

