from flask import Blueprint, render_template, redirect, request, url_for, jsonify, flash
from logs import logger
from database.db_setup import get_db

# Blueprint
extra = Blueprint("extra", __name__)


@extra.before_request
def cargar():
    global conexion
    conexion = get_db()

# Ruta de contacto
@extra.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        nombre_cliente = request.form["nombre_cliente"]
        dni_cliente = request.form["dni_cliente"]
        email = request.form["email"]
        asunto = request.form["asunto"]
        mensaje = request.form["mensaje"]

        # Procesar los datos (enviar un correo, guardar en base de datos, etc.)

        flash("Gracias por ponerte en contacto. Te responderemos pronto.", "success")
        return redirect(
            url_for("/contacto")
        )  # Redirigir al mismo formulario o a otra página de agradecimiento
    return render_template("contacto/contacto.html")


# Ruta de privacidad, términos y servicios
@extra.route("/privacidad")
def privacidad():
    return render_template("/privacidad/privacidad.html")


@extra.route("/terminos")
def terminos():
    return render_template("/privacidad/terminos.html")


@extra.route("/servicio")
def servicio():
    return render_template("servicios/servicios.html")
