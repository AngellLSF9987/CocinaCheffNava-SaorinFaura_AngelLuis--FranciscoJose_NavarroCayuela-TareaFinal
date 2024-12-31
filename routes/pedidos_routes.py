from flask import Blueprint, render_template, redirect, session, url_for, request, jsonify
from database.db_setup import get_db
import repositories.rep_carrito as carritoDB
import repositories.rep_cliente as clienteDB
import repositories.rep_usuario as usuarioDB
import repositories.rep_pedido as pedidoDB
import repositories.rep_producto as productoDB
from logs import logger
import repositories.rep_usuario
from routes.auth_routes import access_required
import routes.usuario_routes

# Blueprint
pedido = Blueprint("pedido", __name__)

@pedido.before_request
def cargar():
    global conexion
    conexion = get_db()

def obtener_productos_del_formulario(request):
    """
    Recoge y retorna los productos seleccionados en el formulario.
    """
    productos = []
    ids_productos = request.form.getlist("id_producto_FK")
    cantidades = request.form.getlist("cantidad")
    precios_carrito = request.form.getlist("precio_carrito")

    # Asegúrate de que las listas tengan la misma longitud
    if len(ids_productos) == len(cantidades) == len(precios_carrito):
        for i in range(len(ids_productos)):
            productos.append({
                "id_producto": ids_productos[i],
                "cantidad": cantidades[i],
                "precio_carrito": precios_carrito[i],
            })
    else:
        logger.warning("Las listas de productos no coinciden en longitud.")

    return productos


@pedido.route("/mostrar_pedidos", methods=["GET"], endpoint="mostrar_pedidos")
@access_required('trabajador')
def mostrar_pedidos():
    try:
        # Obtener todos los pedidos con sus productos
        pedidos = pedidoDB.obtener_pedidos()
        
        if pedidos:
            logger.info("OBTENIENDO LISTADO DE TODOS LOS PEDIDOS")
            return render_template("pedido/pedido_tabla.html", pedidos=pedidos)
        else:
            logger.warning("No se encontraron pedidos en la base de datos.")
            return render_template("pedido/pedido_tabla.html", pedidos=[]), 404

    except Exception as e:
        logger.error(f"Error al MOSTRAR TODOS LOS PEDIDOS: {e}")
        return render_template("error/404.html"), 500


@pedido.route("/listar_pedidos", methods=["GET"], endpoint="listar_pedidos")
@access_required('cliente')
def listar_pedidos():
    try:
        # Obtener el email del usuario autenticado desde la sesión
        email = session.get('user_email', None)

        # Agregar log para depurar
        logger.info(f"Sesion activa para el usuario con email: {email}")

        if not email:
            logger.warning("No se ha encontrado un usuario autenticado.")
            return render_template("error/404.html"), 404

        # Log para verificar el valor exacto del rol
        logger.info(f"Rol del usuario desde la sesión: {session.get('user_role')}")

        # Verificar si el rol es el esperado
        if session.get("user_role") != "cliente":
            logger.warning(f"El usuario con email {email} no tiene el rol de 'cliente'.")
            return render_template("error/404.html"), 404

        # Obtener la contraseña del formulario (en una implementación real no la debes usar directamente)
        password = 'password_placeholder'  # Aquí puedes obtener la contraseña de un formulario si es necesario

        # Autenticar al usuario y obtener su id_usuario y rol
        usuario = usuarioDB.obtener_rol_usuario_logueado(email, password)

        # Obtener el id_cliente asociado al id_usuario
        cliente = clienteDB.obtener_cliente_por_id_usuario(usuario["id_usuario"])

        if not cliente:
            logger.warning(f"No se encontró el cliente asociado al usuario con id {usuario['id_usuario']}.")
            return render_template("error/404.html"), 404

        id_cliente = cliente["id_cliente"]

        # Obtener los pedidos del cliente
        pedidos = pedidoDB.obtener_pedidos_por_cliente(id_cliente)

        if pedidos:
            logger.info(f"OBTENIENDO LISTADO DE PEDIDOS PARA EL CLIENTE {id_cliente}")
            return render_template("pedido/pedido.html", pedidos=pedidos)
        else:
            logger.warning(f"No se encontraron pedidos para el cliente {id_cliente}.")
            return render_template("error/404.html"), 404
    except Exception as e:
        logger.error(f"Error al MOSTRAR LOS PEDIDOS DEL CLIENTE: {e}")
        return render_template("error/404.html"), 500


@pedido.route("/mostrar_pedido_detalle/<int:id_pedido>", methods=["GET"], endpoint="mostrar_pedido_detalle")
def mostrar_pedido_detalle(id_pedido):
    try:
        # Obtener el detalle del pedido con los productos asociados
        detalles_pedido = pedidoDB.obtener_pedido_con_productos()

        # Filtrar solo el pedido específico
        pedido_detalle = next((pedido for pedido in detalles_pedido if pedido["id_pedido"] == id_pedido), None)

        if pedido_detalle:
            logger.info(f"Mostrando detalle del pedido {id_pedido}")
            return render_template("pedido/pedido_detalle.html", pedido=pedido_detalle)
        else:
            logger.warning(f"No se encontró el detalle del pedido {id_pedido}.")
            return render_template("error/404.html"), 404
    except Exception as e:
        logger.error(f"Error al obtener el detalle del pedido {id_pedido}: {e}")
        return render_template("error/500.html"), 500


@pedido.route("/ruta_crear_pedido", methods=["GET", "POST"], endpoint="ruta_crear_pedido")
@access_required('cliente')
def ruta_crear_pedido():
    try:
        productos = []  # Inicializar para evitar problemas de acceso
        if request.method == "POST":
            n_pedido = request.form.get("num_pedido")
            id_carrito_FK = request.form.get("id_carrito_FK")
            fecha_pedido = request.form.get("fecha_pedido")

            # Recoger los productos seleccionados
            productos = obtener_productos_del_formulario(request)

            # Ahora `productos` siempre está definido aquí
            cantidad_productos = len(productos)  # Contamos el número de productos seleccionados

            # Crear un nuevo pedido con productos asociados
            nuevo_pedido = pedidoDB.crear_pedido_con_productos(
                n_pedido,
                id_carrito_FK,
                productos,
                fecha_pedido,
            )

            if nuevo_pedido:
                logger.info("PEDIDO REALIZADO - POST")
                return render_template('pedido/pedido.html', mensaje="Pedido realizado con éxito.")

        if request.method == "GET":
            # Si la solicitud es GET, simplemente renderiza el formulario vacío
            clientes = clienteDB.obtener_clientes()  # Obtener los clientes
            productos = productoDB.obtener_productos()  # Obtener los productos
            carritos = carritoDB.obtener_carritos()  # Obtener los carritos
            logger.info("SOLICITUD GET - FORMULARIO VACÍO")
            return render_template("pedido/pedido_nuevo.html", clientes=clientes, productos=productos, carritos=carritos)

    except Exception as e:
        logger.error(f"Error al CREAR PEDIDO: {e}")
        return render_template('pedido/pedido.html', error="Error al crear el pedido.")

@pedido.route("/ruta_editar_pedido/<int:id_pedido>", methods=["GET", "POST"], endpoint="ruta_editar_pedido")
@access_required('cliente')
@access_required
def editar_pedido(id_pedido):
    try:
        if request.method == "GET":
            try:
                pedido = pedidoDB.obtener_pedido_id(id_pedido)
                if pedido:
                    id_carrito = pedido["id_carrito_FK"]
                    carrito = carritoDB.obtener_carritos(id_carrito)
                    logger.info("CARRITO DEL PEDIDO OBTENIDO POR ID")
                    return render_template('pedido/pedido_editar.html', pedido=pedido, carrito=carrito)
                else:
                    logger.warning("No se encontró el pedido.")
                    return render_template('pedido/pedido.html', error="Pedido no encontrado.")
            except Exception as e:
                logger.error(f"Error al OBTENER PEDIDO POR 'ID': {e}")
                return render_template('error/404.html'), 500

        if request.method == "POST":
            num_pedido = request.form["num_pedido"]
            id_cliente_FK = request.form["id_cliente_FK"]
            id_carrito_FK = request.form["id_carrito_FK"]
            productos = obtener_productos_del_formulario(request)
            fecha_pedido = request.form["fecha_pedido"]

            # Llamar a la función para actualizar el pedido
            pedido_actualizado = pedidoDB.actualizar_pedido(
                conexion,
                id_pedido,
                num_pedido,
                id_cliente_FK,
                id_carrito_FK,
                productos,
                fecha_pedido,
            )
            if pedido_actualizado:
                logger.info("PEDIDO ACTUALIZADO")
                return render_template("pedido/pedido.html", mensaje="Pedido actualizado con éxito.")
            else:
                logger.warning("No se pudo ACTUALIZAR EL PEDIDO.")
                return render_template("pedido/pedido.html", error="No se pudo actualizar el pedido.")
    except Exception as e:
        logger.error(f"Error al ACTUALIZAR PEDIDO: {e}")
        return render_template('pedido/pedido.html', error="Error al actualizar el pedido.")

@pedido.route("/ruta_borrar_pedido", methods=["GET", "POST"], endpoint="ruta_borrar_pedido")
@access_required
def borrar_pedido():
    try:
        id_pedido = request.form.get("id_pedido")
        pedido_borrado = pedidoDB.borrar_pedido(id_pedido)
        if pedido_borrado:
            logger.info("PEDIDO BORRADO")
            return jsonify({"id_pedido": id_pedido}), 200
        else:
            logger.warning("No se encontraron pedidos para BORRAR en la base de datos.")
            return render_template("pedido/pedido.html", error="No se pudo borrar el pedido.")
    except Exception as e:
        logger.error(f"Error al BORRAR PEDIDO: {e}")
        return render_template('pedido/pedido.html', error="Error al borrar el pedido.")
