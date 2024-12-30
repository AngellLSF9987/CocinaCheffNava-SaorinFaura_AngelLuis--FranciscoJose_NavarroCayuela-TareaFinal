from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from functools import wraps
from database.db_setup import get_db
from logs import logger
from repositories.rep_usuario import obtener_rol_usuario_logueado

# Blueprint
auth = Blueprint("auth", __name__)


@auth.before_request
def cargar():
    global conexion
    conexion = get_db()

# Decoradores de autenticación y roles combinados
def access_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "user_role" not in session:
                flash("Por favor, inicia sesión.", "warning")
                return redirect(url_for("auth.login"))
            if role and session.get("user_role") != role:
                logger.warning(f"Acceso denegado. Rol requerido: {role}")
                flash("No tienes permisos para acceder a esta página.", "danger")
                return redirect(url_for("auth.login"))
            return f(*args, **kwargs)

        return wrapper

    return decorator


# Mapeo de roles para redirecciones (ya no se usa en el login)
def role_redirect(role):
    role_map = {
        "cliente": "auth.login",
        "trabajador": "auth.login",
    }
    return role_map.get(role, "auth.login")


# Ruta de login
@auth.route("/login", methods=["GET", "POST"], endpoint="login")
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Ingresa tu correo y contraseña.", "warning")
            return render_template("auth/login.html")

        usuario = obtener_rol_usuario_logueado(email, password)
        if usuario:
            try:
                nombre_rol = usuario.get("nombre_rol")
                if not nombre_rol:
                    flash("Error al obtener el rol del usuario.", "danger")
                    logger.error(f"Error al obtener 'nombre_rol' para el usuario: {email}")
                    return redirect(url_for("auth.login"))

                # Almacenar datos en sesión
                session["user_role"] = nombre_rol
                session["user_email"] = email
                session["id_usuario"] = usuario.get("id_usuario")  # Guardar id_usuario si es necesario
                logger.info(f"Usuario autenticado con rol: {session['user_role']}")

                # Redirigir a la página principal "index"
                return redirect(url_for("index"))
            except Exception as e:
                flash("Hubo un error al procesar tu solicitud.", "danger")
                logger.error(f"Error inesperado al procesar el login para {email}: {e}")
                return redirect(url_for("auth.login"))
        else:
            flash("Credenciales incorrectas.", "danger")
            logger.warning(f"Inicio fallido: {email}")
    return render_template("auth/login.html")


# Ruta de logout
@auth.route("/logout", methods=["GET", "POST"], endpoint="logout")
@access_required()
def logout():
    session.pop('user_role', None)  # Eliminar el rol de la sesión    
    session.pop('user_email', None)  # Eliminar el email cliente o trabajador de la sesión
    session.pop('id_usuario', None)  # Eliminar el usuario de la sesión    
    session.clear()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("index"))


# Ruta de reset password
@auth.route("/reset_password", methods=["GET", "POST"], endpoint="reset_password")
def reset_password():
    # Lógica para el restablecimiento de la contraseña
    return render_template("auth/reset_password.html")