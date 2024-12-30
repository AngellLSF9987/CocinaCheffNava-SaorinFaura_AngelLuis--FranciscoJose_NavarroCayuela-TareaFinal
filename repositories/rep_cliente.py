from copy import Error
from database.db_setup import get_db
from logs import logger
import repositories.rep_usuario
from repositories.rep_usuario import obtener_usuario_id



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


# Crear un nuevo cliente
def crear_cliente(nombre_cliente, apellido1, apellido2, dni_cliente, telefono, direccion, email, id_usuario_FK=None):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        sql = """
        INSERT INTO Clientes (
            nombre_cliente, apellido1, apellido2, dni_cliente, 
            telefono, direccion, email, id_usuario_FK
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (nombre_cliente, apellido1, apellido2, dni_cliente, telefono, direccion, email, id_usuario_FK)
        cursor.execute(sql, values)
        conn.commit()
        return cursor.lastrowid  # Devuelve el ID del cliente creado
    except Error as e:
        logger.error(f"Error al crear cliente: {e}")
        return None  # Devolvemos None en caso de error
    finally:
        cursor.close()

# Actualizar un cliente existente
def actualizar_cliente(
    id_cliente, nombre_cliente, apellido1, apellido2, dni_cliente, telefono, direccion, email, id_usuario_FK
):
    conn = get_db()
    try:
        # Obtener el cliente y verificar si el id_usuario_FK es válido
        usuario = obtener_usuario_id(conn, id_usuario_FK)  # Esta función debe ser creada o adaptada para obtener el usuario
        if not usuario:
            raise ValueError(f"El id_usuario_FK {id_usuario_FK} no es válido")

        # Realizar la actualización
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            UPDATE Clientes
            SET nombre_cliente = %s, apellido1 = %s, apellido2 = %s, dni_cliente = %s, telefono = %s, 
                direccion = %s, email = %s, id_usuario_FK = %s
            WHERE id_cliente = %s
            """,
            (
                nombre_cliente,
                apellido1,
                apellido2,
                dni_cliente,
                telefono,
                direccion,
                email,
                id_usuario_FK,
                id_cliente,
            ),
        )
        conn.commit()
        return cursor.rowcount  # Devuelve el número de filas afectadas
    except Error as e:
        logger.error(f"Error al actualizar cliente: {e}")
        return None  # Devolvemos None en caso de error
    finally:
        cursor.close()


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
