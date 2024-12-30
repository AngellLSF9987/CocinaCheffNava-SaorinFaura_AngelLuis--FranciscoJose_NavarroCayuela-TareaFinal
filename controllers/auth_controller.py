# auth_controller.py
from flask import g
import mysql.connector
from repositories.rep_cliente import obtener_cliente_id
from repositories.rep_trabajador import obtener_trabajador_id
from repositories.rep_usuario import obtener_usuario_id
import database.db_setup as setupDB
import logging
from routes.clientes_routes import conexion

# Configuración básica de logging
logging.basicConfig(level=logging.DEBUG)


def cargar():
    global conexion
    conexion = setupDB.get_db()


def autenticar_usuario(email, password, conexion):
    """Autentica a un usuario como cliente, trabajador o usuario general."""
    try:
        # Establecer conexión con la base de datos
        g.rep_usuario = obtener_usuario_id(conexion)
        logging.debug(f"🔍 Intentando autenticar al usuario con email: {email}")

        # Llamada al repositorio para obtener el usuario y su rol
        usuario = g.rep_usuario.autenticar_usuario(email, password, conexion)

        if usuario:
            logging.debug(f"✅ Usuario autenticado: {usuario}")
            # Aseguramos que estamos extrayendo 'id_rol_FK' de forma correcta
            nombre_rol = usuario.get(
                "id_rol_FK", ""
            ).lower()  # Devuelve "" si no existe
            if nombre_rol:
                logging.debug(f"🔑 Rol del usuario: {nombre_rol}")

                # Diccionario para mapear roles a sus respectivas funciones
                roles = {
                    "cliente": obtener_cliente_id,
                    "trabajador": obtener_trabajador_id,
                }

                if nombre_rol in roles:
                    g.rep_rol = roles[nombre_rol](
                        conexion
                    )  # Asignamos el repositorio según el rol
                    logging.debug(
                        f"🔍 Obteniendo {nombre_rol} con ID: {usuario['id_usuario']}"
                    )
                    # Obtener datos del usuario dependiendo del rol
                    persona = g.rep_rol(usuario["id_usuario"])
                    if persona:
                        logging.debug(
                            f"👨‍🍳 {nombre_rol.capitalize()} encontrado: {persona['nombre_' + nombre_rol]}"
                        )
                        return {
                            "usuario": persona["nombre_" + nombre_rol],
                            "rol": nombre_rol,
                        }
                else:
                    logging.error(
                        f"❌ Rol desconocido para el usuario con email: {email}"
                    )
            else:
                logging.error(
                    f"❌ Error: 'id_rol_FK' no encontrado para el usuario con email: {email}"
                )
        else:
            logging.warning("⚠️ Usuario no encontrado o credenciales incorrectas.")

        return None
    except mysql.connector.Error as e:
        logging.error(f"❌ Error de conexión a la base de datos: {e}")
        return None
    except Exception as e:
        logging.error(f"❌ Error inesperado al autenticar usuario: {e}")
        return None
