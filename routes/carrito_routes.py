# routes/carrito_routes.py

from flask import Blueprint, jsonify, request
import repositories.rep_carrito as carritoDB
from database.db_setup import get_db
from logs import logger

# Crear Blueprint
carrito = Blueprint("carrito", __name__)

# Rutas

@carrito.before_request
def cargar():
    global conexion
    conexion = get_db()

@carrito.route("/carritos", methods=["GET"])
def listar_carritos():
    """Ruta para listar todos los carritos."""
    try:
        carritos = carritoDB.obtener_carritos()
        return jsonify(carritos), 200
    except Exception as e:
        logger.error(f"Error al listar carritos: {e}")
        return jsonify({"error": "Error al obtener los carritos"}), 500


@carrito.route("/carritos/<int:id_carrito>", methods=["GET", "POST"])
def carrito_por_id(id_carrito):
    """Ruta para obtener un carrito específico por ID."""
    try:
        carrito = carritoDB.obtener_carrito_id(id_carrito)
        if not carrito:
            return jsonify({"error": "Carrito no encontrado"}), 404
        return jsonify(carrito), 200
    except Exception as e:
        logger.error(f"Error al obtener el carrito con ID {id_carrito}: {e}")
        return jsonify({"error": "Error al obtener el carrito"}), 500
    
@carrito.route("/eliminar_item", methods=["POST"])
def eliminar_item():
    """Ruta para eliminar un ítem del carrito."""
    try:
        id_item = request.form.get("id_item")
        if not id_item or not id_item.isdigit():
            return jsonify({"error": "ID del ítem inválido"}), 400
        
        resultado = carritoDB.eliminar_item_db(int(id_item))
        if resultado:
            return jsonify({"mensaje": "Ítem eliminado exitosamente"}), 200
        else:
            return jsonify({"error": "No se pudo eliminar el ítem. Verifique el ID"}), 404
    except Exception as e:
        logger.error(f"Error al eliminar ítem del carrito: {e}")
        return jsonify({"error": "Error interno al eliminar ítem"}), 500


@carrito.route("/borrar_carrito", methods=["POST"])
def borrar_carrito():
    """Ruta para borrar un carrito completo."""
    try:
        id_carrito = request.form.get("id_carrito")
        if not id_carrito or not id_carrito.isdigit():
            return jsonify({"error": "ID del carrito inválido"}), 400
        
        resultado = carritoDB.borrar_carrito_db(int(id_carrito))
        if resultado:
            return jsonify({"mensaje": "Carrito borrado exitosamente"}), 200
        else:
            return jsonify({"error": "No se pudo borrar el carrito. Verifique el ID"}), 404
    except Exception as e:
        logger.error(f"Error al borrar carrito: {e}")
        return jsonify({"error": "Error interno al borrar carrito"}), 500


@carrito.route("/finalizar_compra", methods=["POST"])
def finalizar_compra():
    """Ruta para finalizar la compra."""
    try:
        id_carrito = request.form.get("id_carrito")
        if not id_carrito or not id_carrito.isdigit():
            return jsonify({"error": "ID del carrito inválido"}), 400
        
        resultado = carritoDB.finalizar_compra_db(int(id_carrito))
        if resultado:
            return jsonify({"mensaje": "Compra finalizada exitosamente"}), 200
        else:
            return jsonify({"error": "No se pudo finalizar la compra. Verifique el ID"}), 404
    except Exception as e:
        logger.error(f"Error al finalizar la compra: {e}")
        return jsonify({"error": "Error interno al finalizar la compra"}), 500
