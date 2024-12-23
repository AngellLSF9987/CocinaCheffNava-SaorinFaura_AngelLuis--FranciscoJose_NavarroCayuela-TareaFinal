from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from database.db_setup import get_db
import repositories.rep_carrito as carritoDB
import repositories.rep_cliente as clienteDB
import repositories.rep_pedido as pedidoDB
import repositories.rep_producto as productoDB
from logs import logger

# Blueprint
pedido = Blueprint("pedido", __name__)


@pedido.before_request
def cargar():
    global conexion
    conexion = get_db()

@pedido.route("/pedido_template")
def pedido_template():
    return render_template('pedido/pedido.html')

@pedido.route("/mostrar_pedidos", methods=["GET"], endpoint="mostrar_pedidos")
def mostrar_pedidos():
    try:
        # Obtener todos los pedidos con sus productos
        pedidos = pedidoDB.obtener_pedido_con_productos()
        
        if pedidos:
            logger.info("OBTENIENDO LISTADO DE TODOS LOS PEDIDOS")
            return render_template("pedido/pedido.html", pedidos=pedidos)
        else:
            logger.warning("No se encontraron pedidos en la base de datos.")
            return render_template("pedido/pedido.html", pedidos=[]), 404

    except Exception as e:
        logger.error(f"Error al MOSTRAR TODOS LOS PEDIDOS: {e}")
        return render_template("error/404.html"), 500

@pedido.route("/ruta_crear_pedido", methods=["GET", "POST"], endpoint="ruta_crear_pedido")
def ruta_crear_pedido():
    try:
        if request.method == "POST":
            n_pedido = request.form.get("num_pedido")
            id_cliente_FK = request.form.get("id_cliente_FK")
            id_carrito_FK = request.form.get("id_carrito_FK")
            fecha_pedido = request.form.get("entrega")

            # Recoger los productos seleccionados
            productos = []
            cantidad_productos = len(request.form.getlist("id_producto_FK"))  # Contamos el número de productos seleccionados

            # Recolectar los productos y sus cantidades
            for i in range(cantidad_productos):
                id_producto_FK = request.form.getlist("id_producto_FK")[i]
                cantidad = request.form.getlist("cantidad")[i]
                precio_carrito = request.form.getlist("precio_carrito")[i]  # Si tienes el precio del producto
                productos.append({
                    "id_producto": id_producto_FK,
                    "cantidad": cantidad,
                    "precio_carrito": precio_carrito
                })

            # Crear un nuevo pedido con productos asociados
            nuevo_pedido = pedidoDB.crear_pedido_con_productos(
                n_pedido,
                id_cliente_FK,
                id_carrito_FK,
                productos,
                fecha_pedido,
            )

            if nuevo_pedido:
                logger.info("PEDIDO REALIZADO - POST")
                return render_template('pedido/pedido.html', mensaje="Pedido realizado con éxito.")

        if request.method == "GET":
            # Si la solicitud es GET, simplemente renderiza el formulario vacío
            clientes = clienteDB.obtener_clientes(conexion)  # Obtener los clientes
            productos = productoDB.obtener_productos(conexion)  # Obtener los productos
            carritos = carritoDB.obtener_carritos(conexion)  # Obtener los carritos
            logger.info("SOLICITUD GET - FORMULARIO VACÍO")
            return render_template("pedido/pedido.html", clientes=clientes, productos=productos, carritos=carritos)

    except Exception as e:
        logger.error(f"Error al CREAR PEDIDO: {e}")
        return render_template('pedido/pedido.html', error="Error al crear el pedido.")

@pedido.route("/ruta_editar_pedido/<int:id_pedido>", methods=["GET", "POST"], endpoint="ruta_editar_pedido")
def editar_pedido(id_pedido):

    try:
        if request.method == "GET":
            try:
                pedido = pedidoDB.obtener_pedido_id(id_pedido)
                if pedido:
                    try:
                        id_cliente = clienteDB.obtener_cliente_id(id_cliente)
                        logger.info("CLIENTE DEL PEDIDO OBTENIDO POR ID"), 200
                    except Exception as e:
                        logger.error(f"Error al OBTENER CLIENTE POR 'ID': {e}"), 404
                    try:   
                        id_producto = productoDB.obtener_producto_id(id_producto)
                        logger.info("PRODUCTO DEL PEDIDO OBTENIDO POR ID"), 200
                    except Exception as e:
                        logger.error(f"Error al OBTENER PRODUCTO DEL PEDIDO POR 'ID': {e}"), 404
                    try:   
                        id_carrito = carritoDB.obtener_carritos(id_carrito)
                        logger.info("CARRITO DEL PEDIDO OBTENIDO POR ID"), 200
                    except Exception as e:
                        logger.error(f"Error al OBTENER CARRITO DEL PEDIDO POR 'ID': {e}"), 404
                logger.info("OBTENIENDO PEDIDO EXISTENTE"), 200                                
                return render_template('pedido/pedido.html')
            except Exception as e:
                logger.error(f"Error al OBTENER PEDIDO POR 'ID': {e}"), 500
                return render_template('pedido/pedido.html')            
                # Obtener los clientes, productos y carritos disponibles - PETICIÓN GET

        if request.method == "POST":
            num_pedido = request.form["num_pedido"]
            id_cliente_FK = request.form["id_cliente_FK"]
            id_producto_FK = request.form["id_producto_FK"]
            id_carrito_FK = request.form["id_carrito_FK"]
            cantidad = request.form["cantidad"]
            fecha_pedido = request.form["entrega"]

            # Llamar a la función para actualizar el pedido
            pedido_actualizado = pedidoDB.actualizar_pedido(
                conexion,
                id_pedido,
                num_pedido,
                id_cliente_FK,
                id_producto_FK,
                id_carrito_FK,
                cantidad,
                fecha_pedido,
            )
            if pedido_actualizado:
                logger.info("PEDIDO ACTUALIZADO"), 200
                return render_template("pedido/pedido.html", id_cliente_FK=id_cliente, id_producto_FK=id_producto , id_carrito_FK=id_carrito)
            else:
                logger.warning("No se pudo ACTUALIZAR EL PEDIDO."), 404
                return render_template("pedido/pedido.html")                
    except Exception as e:
        logger.error(f"Error al ACTUALIZAR PEDIDO: {e}"), 500
        return render_template('pedido/pedido.html')         


@pedido.route("/ruta_borrar_pedido", methods=["GET", "POST"], endpoint="ruta_borrar_pedido")
def borrar_pedido():
    try:
        id_pedido = request.form.get("id_pedido")
        pedido = pedidoDB.borrar_pedido(id_pedido)
        if pedido:
            logger.info("PEDIDO BORRADO"), jsonify(id_pedido), 200
            return render_template('pedido/pedido.html')
        else:
            logger.warning("No se encontraron pedidos para BORRAR en la base de datos."), 404
            return render_template("pedido/pedido.html")                
    except Exception as e:
        logger.error(f"Error al BORRAR PEDIDO: {e}"), 500
        return render_template('pedido/pedido.html')        
