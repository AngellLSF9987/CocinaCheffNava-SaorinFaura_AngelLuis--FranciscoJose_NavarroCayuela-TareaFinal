from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from functools import wraps
from database.db_setup import get_db
from logs import logger
from repositories.rep_cliente import obtener_cliente_por_id_usuario
from repositories.rep_trabajador import obtener_trabajador_por_id_usuario
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
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not password:
            flash("Ingresa tu correo y contraseña.", "warning")
            return render_template("auth/login.html")

        usuario = obtener_rol_usuario_logueado(email, password)
        if usuario:
            try:
                nombre_rol = usuario.get("nombre_rol")
                id_usuario = usuario.get("id_usuario")

                if not nombre_rol:
                    flash("Error al obtener el rol del usuario.", "danger")
                    return redirect(url_for("auth.login"))

                # Guardar información básica en la sesión
                session.clear()  # Limpiar sesión anterior
                session["user_role"] = nombre_rol
                session["user_email"] = email
                session["id_usuario"] = id_usuario

                # Verificar rol y agregar datos específicos
                if nombre_rol == "cliente":
                    cliente = obtener_cliente_por_id_usuario(id_usuario)
                    if cliente:
                        session["id_cliente"] = cliente.get("id_cliente")
                    else:
                        flash("No se encontró información del cliente.", "warning")
                        return redirect(url_for("auth.login"))

                elif nombre_rol == "trabajador":
                    trabajador = obtener_trabajador_por_id_usuario(id_usuario)
                    if trabajador:
                        session["id_trabajador"] = trabajador.get("id_trabajador")
                    else:
                        flash("No se encontró información del trabajador.", "warning")
                        return redirect(url_for("auth.login"))

                # Redirigir al índice
                return redirect(url_for("index"))

            except Exception as e:
                flash("Hubo un error al procesar tu solicitud.", "danger")
                return redirect(url_for("auth.login"))
        else:
            flash("Credenciales incorrectas.", "danger")
    return render_template("auth/login.html")


# Ruta de logout
@auth.route("/logout", methods=["GET"], endpoint="logout")
def logout():
    session.clear()  # Elimina todos los datos de la sesión
    flash("Has cerrado sesión exitosamente.", "success")
    return redirect(url_for("auth.login"))


# Ruta de reset password
@auth.route("/reset_password", methods=["GET", "POST"], endpoint="reset_password")
def reset_password():
    # Lógica para el restablecimiento de la contraseña
    return render_template("auth/reset_password.html")