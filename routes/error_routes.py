from flask import Blueprint, render_template
from logs import logger
import logging
from database.db_setup import get_db

# Blueprint
error = Blueprint("error", __name__)


@error.before_request
def cargar():
    global conexion
    conexion = get_db()


# Manejo de errores
@error.errorhandler(404)
def page_not_found(e):
    logger.error(f"Error interno: {logging.error}")
    return render_template("error/404.html"), 404


@error.errorhandler(403)
def forbidden(e):
    logger.error(f"Error interno: {logging.error}")
    return render_template("error/403.html"), 403


@error.errorhandler(500)
def internal_error(error):
    logger.error(f"Error interno: {error}")
    return "Ocurrió un error en el servidor", 500
