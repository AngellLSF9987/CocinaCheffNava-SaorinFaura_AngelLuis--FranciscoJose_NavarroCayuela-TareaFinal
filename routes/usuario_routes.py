from copy import error
from flask import Blueprint, redirect, render_template, url_for, request
from database.db_setup import get_db
from logs import logger
import repositories.rep_cliente as clienteDB
import repositories.rep_trabajador as trabajadorDB
import repositories.rep_usuario as usuarioDB

# Blueprint
usuario = Blueprint("usuario", __name__)

@usuario.before_request
def cargar():
    global conexion
    conexion = get_db()


@usuario.route("/ruta_registro_usuario", methods=["GET", "POST"], endpoint="registro")
def alta_usuarios():
    """Ruta Alta Usuarios - Formulario de Registro."""
    
    try:
        if request.method == "GET":
            # Obtener el rol del usuario logueado
            rol_usuario = usuarioDB.obtener_rol_usuario_logueado()  # Lógica para obtener el rol
            es_trabajador = rol_usuario == "Trabajador"
            
            logger.info("Mostrando formulario altas usuarios.")
            return render_template('auth/register.html', es_trabajador=es_trabajador), 200
        
        if request.method == "POST":
            logger.info("Procesando formulario de registro/altas usuarios...")

            # Obtener los datos del formulario
            email = request.form.get("email")
            contraseña = request.form.get("password")
            rol = request.form.get("rol")  # Obtener el rol del formulario
            
            if rol == "Cliente":
                nombre = request.form.get("nombre_cliente")
                apellido1 = request.form.get("apellido1_cliente")
                apellido2 = request.form.get("apellido2_cliente")
                dni = request.form.get("dni_cliente")
                telefono = request.form.get("telefono_cliente")
                direccion = request.form.get("direccion_cliente")
                
                # Crear usuario y cliente
                id_usuario = usuarioDB.crear_usuario(email, contraseña, rol)
                clienteDB.crear_cliente(id_usuario, nombre, apellido1, apellido2, dni, telefono, direccion)
            
            elif rol == "Trabajador":
                nombre = request.form.get("nombre_trabajador")
                apellido1 = request.form.get("apellido1_trabajador")
                apellido2 = request.form.get("apellido2_trabajador")
                dni = request.form.get("dni_trabajador")
                telefono = request.form.get("telefono_trabajador")
                direccion = request.form.get("direccion_trabajador")
                
                # Crear usuario y trabajador
                id_usuario = usuarioDB.crear_usuario(email, contraseña, rol)
                trabajadorDB.crear_trabajador(id_usuario, nombre, apellido1, apellido2, dni, telefono, direccion)
            
            return redirect(url_for("auth.login"))
    
    except Exception as e:
        logger.error(f"Error en la ruta: {e}", extra={"error": "Error al procesar el formulario."})
        return redirect(url_for("index"))