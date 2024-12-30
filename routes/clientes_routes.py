from copy import error
from flask import Blueprint, redirect, render_template, url_for, request
from database.db_setup import get_db
from logs import logger
import repositories.rep_cliente as clienteDB
from routes.auth_routes import access_required

# Blueprint
cliente = Blueprint("cliente", __name__)

@cliente.before_request
def cargar():
    global conexion
    conexion = get_db()

@cliente.route("/mostrar_clientes", methods=["GET"], endpoint="mostrar_clientes")
@access_required('trabajador')
def mostrar_clientes():
    """Ruta para listar todos los CLIENTES DESDE ADMIN."""
    try:
        clientes = clienteDB.obtener_clientes()
        if clientes:
            logger.info("OBTENIENDO CLIENTES DESDE ADMIN"), 200
            return render_template("cliente/cliente_tabla.html", clientes=clientes)
        else:
            logger.warning("No se encontraron clientes"), 404
            return redirect(url_for("index"))            
    except Exception as e:
        logger.error(f"Error al listar CLIENTES DESDE ADMIN: {e}"), 500
        return redirect(url_for("index"))

# Ruta para el detalle del cliente
@cliente.route('/cliente_detalle/<int:id_cliente>', methods = ["GET", "POST"], endpoint ="perfil")
@access_required('cliente')  # Asegura que el usuario tenga el rol cliente
def cliente_detalle(id_cliente):
    try:
        # Obtén el ID del cliente desde el repositorio utilizando el método obtener_cliente_id()
        cliente = clienteDB.obtener_cliente_id(id_cliente)  # Asume que este método devuelve el ID del cliente autenticado
        if cliente:
            logger.info(f"CLIENTE DETALLE PARA CLIENTE: {cliente['nombre_cliente']}")
            return render_template(
                "cliente/cliente_detalle.html",
                cliente=cliente,
                id_cliente=id_cliente,  # id_cliente explícitamente
                editando=False
            ), 200
        else:
            logger.warning(f"No se encontró el cliente con ID {id_cliente}")
            return render_template("index.html", mensaje="Cliente no encontrado"), 404
    except Exception as e:
        logger.error(f"Error OBTENIENDO DETALLE CLIENTE con ID {id_cliente}: {e}")
        return render_template("index.html", mensaje="Error al obtener los detalles del cliente"), 500


@cliente.route("/editar_cliente/<int:id_cliente>", methods=["GET", "POST"], endpoint="editar_perfil")
@access_required('cliente')
def mostrar_cliente(conexion,id_cliente):
    """Ruta para DETALLE CLIENTE DESDE CLIENTE."""
    try:
        if request.method == "GET":
            cliente = clienteDB.obtener_cliente_id(conexion,id_cliente)
            if cliente:
                logger.info("REDIRECIONANDO A CLIENTE ACTUALIZAR DESDE CLIENTE"), 200
                return render_template("/cliente/cliente_editar.html", cliente=cliente)
            else:
                logger.warning(f"Cliente con ID {id_cliente} no encontrado.")
                return render_template("error/404.html"), 404
        
        elif request.method == "POST":
            nombre_cliente = request.form.get("nombre_cliente")
            apellido1 = request.form.get("apellido1")
            apellido2 = request.form.get("apellido2")
            dni_cliente = request.form.get("dni_cliente")
            telefono = request.form.get("telefono")
            direccion = request.form.get("direccion")
            email = request.form.get("email")
            id_usuario_FK = request.form.get("id_usuario_FK")
            
            if not all([nombre_cliente, apellido1, apellido2, dni_cliente, telefono, direccion, email, id_usuario_FK]):
                logger.warning("Datos incompletos para actualizar el Cliente.", extra={"error": "Faltan datos obligatorios"})
                return redirect(url_for("editar_perfil")), 400
            
            cliente_actualizado = clienteDB.actualizar_cliente(
                id_cliente,
                nombre_cliente,
                apellido1,
                apellido2,
                dni_cliente,
                telefono,
                direccion,
                email,
                int(id_usuario_FK),
            )
            
            if cliente_actualizado:
                logger.info(f"CLIENTE ACTUALIZADO EXITOSAMENTE: {cliente_actualizado['nombre_cliente']}", extra={"success": "Cliente actualizado"})
                return redirect(url_for("editar_perfil"))
            else:
                logger.error(f"Error al actualizar el CLIENTE con ID {id_cliente}.", extra={"error": "CLIENTE no actualizado"})
                return render_template("error/404.html"), 404                                          
    except Exception as e:
        logger.error(f"Error REDIRECCIÓN CLIENTE ACTUALIZAR DESDE CLIENTE: {e}"), 500
        return redirect(url_for("index"))

@cliente.route("/borrar_cliente", methods=["GET", "POST"], endpoint="borrar_cliente")
@access_required('trabajador')
def borrar_producto():
    """Ruta para BORRAR CLIENTE DESDE ADMIN."""
    try:
        if request.method == "POST":
            id_cliente = request.form.get("id_cliente")
            cliente = clienteDB.obtener_cliente_id(id_cliente)
            if cliente:
                clienteDB.borrar_cliente(id_cliente)
                logger.info("CLIENTE BORRADO"), 200
                return redirect(url_for("mostrar_clientes"))
            else:
                logger.warning(f"Cliente con ID {id_cliente} no encontrado."), 404
                return redirect (url_for("mostrar_clientes"))            
    except Exception as e:
        logger.error(f"Error al BORRAR CLIENTE DESDE ADMIN: {e}"), 500
        return redirect(url_for("mostrar_clientes"))          
