# repositories/rep_usuarios.py

from copy import Error
from database.db_setup import get_db
from logs import logger
import repositories.rep_cliente as clienteDB
import repositories.rep_trabajador as trabajadorDB

# Mostrar usuarios
def obtener_usuarios():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Usuarios")
        usuarios = cursor.fetchall()
        return usuarios  # Devolvemos una lista de usuarios
    except Error as e:
        logger.error(f"Error al obtener usuarios: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error


# Mostrar usuario por id
def obtener_usuario_id(id_usuario):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT 1 FROM Usuarios WHERE id_usuario=?", (id_usuario,))
        usuario = cursor.fetchone()
        return usuario
    except Error as e:
        logger.error(f"Error al obtener usuario: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error    


def crear_usuario(email, contraseña, rol="Cliente"):
    """Crea un usuario con el rol especificado, por defecto 'Cliente'."""
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Insertamos el usuario con el rol especificado
        cursor.execute(
            """
            INSERT INTO Usuarios (email, contraseña, id_rol_FK) 
            VALUES (%s, %s, (SELECT id_rol FROM Roles WHERE nombre_rol = %s))
            """,
            (email, contraseña, rol)
        )
        conn.commit()
        
        # Obtener el id del último usuario insertado
        cursor.execute("SELECT LAST_INSERT_ID()")
        id_usuario = cursor.fetchone()[0]
        
        return id_usuario  # Retorna el id_usuario recién creado
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error al crear usuario: {e}")
    finally:
        cursor.close()


def obtener_rol_usuario_logueado(email, password):
    """Autentica a un usuario y devuelve sus datos, incluido su rol, si las credenciales son correctas."""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        # Consulta para obtener usuario y su rol
        query = """
                SELECT u.id_usuario, u.email, u.contraseña, u.id_rol_FK, r.nombre_rol
                FROM Usuarios u
                JOIN Roles r ON u.id_rol_FK = r.id_rol
                WHERE u.email = %s
            """
        cursor.execute(query, (email,))
        usuario = cursor.fetchone()

        if usuario:
            # Comparar contraseñas (asegúrate de usar un sistema de hashing en producción)
            if usuario["contraseña"] == password:
                id_usuario = usuario["id_usuario"]

                # Verificar si el usuario es un Cliente o Trabajador
                cliente = clienteDB.obtener_cliente_por_id_usuario(id_usuario)
                trabajador = trabajadorDB.obtener_trabajador_por_id_usuario(id_usuario)

                # Si es cliente, asignamos el rol correspondiente
                if cliente:
                    usuario["rol"] = "cliente"
                    usuario["nombre_rol"] = "Cliente"
                # Si es trabajador, asignamos el rol correspondiente
                elif trabajador:
                    usuario["rol"] = "trabajador"
                    usuario["nombre_rol"] = "Trabajador"
                else:
                    usuario["rol"] = "desconocido"
                    usuario["nombre_rol"] = "Desconocido"

                return {
                    "id_usuario": usuario["id_usuario"],
                    "email": usuario["email"],
                    "rol": usuario["rol"],
                    "nombre_rol": usuario["nombre_rol"],
                }
            else:
                return None
        else:
            return None
    except Exception as e:
        logger.error(f"Error al autenticar al usuario: {e}")
        return None
    finally:
        cursor.close()

