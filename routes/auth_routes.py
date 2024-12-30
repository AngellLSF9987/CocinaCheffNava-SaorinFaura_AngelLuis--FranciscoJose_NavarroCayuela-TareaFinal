from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from functools import wraps
from database.db_setup import get_db
from logs import logger

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


# Mapeo de roles para redirecciones
def role_redirect(role):
    role_map = {
        "cliente": "auth.login",
        "trabajador": "auth.login",
    }
    return role_map.get(role, "auth.login")


# Ruta de login
@auth.route("/login", methods=["GET", "POST"], endpoint="login")
def login():
    from repositories.rep_usuario import obtener_rol_usuario_logueado

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Ingresa tu correo y contraseña.", "warning")
            return render_template("auth/login.html")

        usuario = obtener_rol_usuario_logueado(email, password, conexion)
        if usuario:
            try:
                nombre_rol = usuario.get("rol")
                if not nombre_rol:
                    flash("Error al obtener el rol del usuario.", "danger")
                    logger.error(
                        f"Error al obtener 'nombre_rol' para el usuario: {email}"
                    )
                    return redirect(url_for("auth.login"))

                session["user_role"] = nombre_rol.lower()
                session["user_email"] = email
                logger.info(f"Rol del usuario en sesión: {session['user_role']}")
                return redirect(url_for(role_redirect(nombre_rol.lower())))
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
    session.clear()
    flash("Has cerrado sesión.", "info")
    return render_template("/")


# Ruta de reset password
@auth.route("/reset_password", methods=["GET", "POST"], endpoint="reset_password")
def reset_password():
    # Lógica para el restablecimiento de la contraseña
    return render_template("auth/reset_password.html")
