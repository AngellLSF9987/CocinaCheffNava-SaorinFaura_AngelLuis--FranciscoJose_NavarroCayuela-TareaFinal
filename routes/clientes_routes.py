from flask import Blueprint, render_template, redirect, request, jsonify
from database.db_setup import get_db
from logs import logger
import repositories.rep_cliente as clienteDB

# Blueprint
cliente = Blueprint("cliente", __name__)

@cliente.before_request
def cargar():
    global conexion
    conexion = get_db()

@cliente.route("/mostrar_clientes", methods=["GET"])
def mostrar_clientes():
    """Ruta para listar todos los CLIENTES DESDE ADMIN."""
    try:
        clientes = clienteDB.obtener_clientes(conexion)
        return render_template("cliente/cliente.html", clientes=clientes, editando=False), jsonify(clientes), 200
    except Exception as e:
        logger.error(f"Error al listar CLIENTES DESDE ADMIN: {e}")
        return render_template("/"),jsonify({"error": "Error al obtener los CLIENTES DESDE ADMIN"}), 500

@cliente.route("/editar_cliente/<int:id_cliente>", methods=["GET", "POST"])
def mostrar_cliente(conexion,id_cliente):
    """Ruta para DETALLE CLIENTE DESDE CLIENTE."""
    try:
        cliente = clienteDB.obtener_cliente_id(conexion,id_cliente)
        logger.info("REDIRECIONANDO A CLIENTE ACTUALIZAR DESDE CLIENTE")
        return render_template("/cliente/cliente_editar.html", cliente=cliente), jsonify(cliente), 200
    except Exception as e:
        logger.error(f"Error REDIRECCIÓN CLIENTE ACTUALIZAR DESDE CLIENTE: {e}")
        return render_template("index.html"),jsonify({"error": "Error al obtener los CLIENTES DESDE ADMIN"}), 500    


@cliente.route("/borrar_cliente", methods=["GET", "POST"])
def borrar_producto():
    """Ruta para BORRAR CLIENTE DESDE ADMIN."""
    try:    
        id_cliente = request.form.get("id_cliente")
        clienteDB.borrar_cliente(id_cliente)
        logger.info("CLIENTE BORRADO")
        return redirect("/mostrar_clientes"), 200
    except Exception as e:
        logger.error(f"Error al BORRAR CLIENTE DESDE ADMIN: {e}")
        return redirect("/mostrar_clientes"), jsonify({"error": "Error al BORRAR CLIENTE DESDE ADMIN"}), 500            
