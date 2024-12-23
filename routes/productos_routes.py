from PIL import Image
from flask import Blueprint, render_template, request, jsonify
from database.db_setup import get_db
from logs import logger
import repositories.rep_producto as productoDB
import repositories.rep_categoria as categoriaDB

# Blueprint
producto = Blueprint("producto", __name__)


@producto.before_request
def cargar():
    global conexion
    conexion = get_db()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@producto.route("/producto_template")
def producto_template():
    return render_template('producto/producto.html')

@producto.route("/mostrar_productos", methods=["GET"], endpoint="mostrar_productos")
def mostrar_productos():
    try:
        productos = productoDB.obtener_productos()
        if productos:
            logger.info("OBTENIENDO PRODUCTOS DESDE ADMIN"), 200
            return render_template('producto/producto_tabla.html', productos=productos)
        else:
            logger.warning("No se encontraron productos"), 404
            return render_template("index.html")
    except Exception as e:
        logger.error(f"Error OBTENIENDO PRODUCTOS DESDE ADMIN: {e}"), 500
        return render_template("index.html")

@producto.route("/listar_productos", methods=["GET"], endpoint="listar_productos")
def listar_productos():
    try:
        productos = productoDB.obtener_productos()
        if productos:
            logger.info("OBTENIENDO PRODUCTOS DESDE ADMIN"), 200
            return render_template('producto/producto.html', productos=productos)
        else:
            logger.warning("No se encontraron productos"), 404
            return render_template("index.html")
    except Exception as e:
        logger.error(f"Error OBTENIENDO PRODUCTOS DESDE ADMIN: {e}"), 500
        return render_template("index.html")
  
@producto.route('/ruta_crear_producto', methods=['GET', 'POST'], endpoint="ruta_crear_producto")
def ruta_crear_producto():
    try:
        # Manejo explícito de GET: renderizar el formulario para crear un producto
        if request.method == 'GET':
            logger.info("Mostrando formulario para crear un producto.")
            
            # Obtener las categorías de la base de datos
            categorias = categoriaDB.obtener_categorias()

            # Pasar las categorías al template para mostrarlas en el formulario
            return render_template('producto/producto_nuevo.html', categorias=categorias)

        # Manejo de POST: procesar el formulario
        if request.method == 'POST':
            logger.info("Procesando formulario para crear un producto...")

            # Obtener datos del formulario
            nombre = request.form.get('nombre')
            descripcion = request.form.get('descripcion')
            precio = request.form.get('precio')
            imagen = request.files.get('imagen')
            id_categoria_FK = request.form.get('id_categoria_FK')

            # Validar datos
            if not (nombre and descripcion and precio and id_categoria_FK):
                logger.error("Faltan campos requeridos.")
                return render_template('producto/producto_nuevo.html', error="Todos los campos son obligatorios.")

            try:
                precio = float(precio)
            except ValueError:
                logger.error("Precio inválido.")
                return render_template('producto/producto_nuevo.html', error="El precio debe ser un número.")

            # Guardar la imagen
            ruta_imagen = None  # Por defecto es None
            if imagen and imagen.filename != '':
                try:
                    # Guardamos solo el nombre del archivo, no la ruta completa
                    nombre_imagen = imagen.filename  # Esto extrae el nombre del archivo
                    ruta_imagen = f"static/images/productos/{nombre_imagen}"
                    imagen.save(ruta_imagen)
                    logger.info(f"Imagen guardada correctamente: {ruta_imagen}")
                except Exception as e:
                    logger.error(f"Error al guardar la imagen: {e}")
                    return render_template('producto/producto_nuevo.html', error="Error al cargar la imagen.")
            else:
                logger.info("No se proporcionó imagen. Campo 'imagen' quedará como NULL.")


            # Validar categoría
            if not categoriaDB.obtener_categoria_id(id_categoria_FK):
                logger.error(f"Categoría ID {id_categoria_FK} no válida.")
                return render_template('producto/producto_nuevo.html', error="Categoría no válida.")

            logger.info(f"Ruta de la imagen antes del INSERT: {ruta_imagen}")
            logger.info(f"Llamando a crear_producto con: {nombre}, {descripcion}, {precio}, {nombre_imagen}, {id_categoria_FK}")
            # Insertar el producto
            productoDB.crear_producto(nombre, descripcion, precio, nombre_imagen, id_categoria_FK)
            logger.info(f"Producto creado: {nombre}, {descripcion}, {precio}, {nombre_imagen}, {id_categoria_FK}")

            return render_template("producto/producto.html", mensaje="Producto creado exitosamente.")

    except Exception as e:
        logger.error(f"Error en la ruta: {e}")
        return render_template('producto/producto_nuevo.html', error="Error al procesar el formulario.")


@producto.route("/mostrar_producto_detalle/<int:id_producto>", methods=["GET", "POST"], endpoint="mostrar_producto_detalle")
def mostrar_producto_detalle(id_producto):
    try:
        producto = productoDB.obtener_producto_id(id_producto)
        if producto:
            logger.info(f"PRODUCTO DETALLE PARA CLIENTE O ADMIN: {producto['nombre_producto']}")
            return render_template(
                "producto/producto_detalle.html",
                producto=producto,
                id_producto=id_producto,  # Pasamos id_producto explícitamente
                editando=False
            ), 200
        else:
            logger.warning(f"No se encontró el producto con ID {id_producto}")
            return render_template("index.html", mensaje="Producto no encontrado"), 404
    except Exception as e:
        logger.error(f"Error OBTENIENDO DETALLE PRODUCTO con ID {id_producto}: {e}")
        return render_template("index.html", mensaje="Error al obtener los detalles del producto"), 500
      

@producto.route("/editar_producto/<int:id_producto>", methods=["GET", "POST"], endpoint="ruta_editar_producto")
def ruta_editar_producto(id_producto):
    try:
        if request.method == "GET":
            # Buscar el producto por su ID
            producto = productoDB.obtener_producto_id(id_producto)
            if producto:
                logger.info(f"PRODUCTO OBTENIDO POR 'ID': {id_producto}")
                return render_template('producto/producto_editar.html', producto=producto)
            else:
                logger.warning(f"Producto con ID {id_producto} no encontrado.")
                return render_template("error/404.html"), 404

        elif request.method == "POST":
            # Obtener datos del formulario
            nombre_producto = request.form.get("nombre_producto")
            id_categoria_FK = request.form.get("id_categoria_FK")
            descripcion = request.form.get("descripcion")
            precio = request.form.get("precio")
            imagen = request.form.get("imagen")

            # Validar que los campos obligatorios estén presentes
            if not all([nombre_producto, id_categoria_FK, precio]):
                logger.warning("Datos incompletos para actualizar el producto.")
                return render_template("producto/producto_editar.html", error="Faltan datos obligatorios"), 400
            
            # Actualizar el producto en la base de datos
            producto_actualizado = productoDB.actualizar_producto(
                id_producto,
                nombre_producto,
                descripcion,
                precio,
                imagen,
                id_categoria_FK,
            )
            
            if producto_actualizado:
                logger.info(f"PRODUCTO ACTUALIZADO: {producto_actualizado['nombre_producto']}")
                return render_template("producto/producto_tabla.html", success="Producto actualizado exitosamente"), 200
            else:
                logger.error(f"Error al actualizar el producto con ID {id_producto}.")
                return render_template("error/404.html"), 404

    except Exception as e:
        logger.error(f"Error al ACTUALIZAR PRODUCTO: {e}")
        return render_template("error/500.html"), 500

            
@producto.route("/borrar_producto", methods=["GET", "POST"], endpoint="ruta_borrar_producto")
def ruta_borrar_producto():
    try:
        if request.method == "POST":
            producto_id = request.form.get("id_producto")
            producto = productoDB.obtener_producto_id(producto_id)
            if producto:
                productoDB.borrar_producto(producto_id)
                logger.info(f"PRODUCTO BORRADO: {producto['nombre_producto']}"), 200
                return render_template("producto/producto_tabla.html")
            else:
                logger.warning(f"Producto con ID {producto_id} no encontrado."), 404
                return render_template("producto/producto_tabla.html")
    except Exception as e:
        logger.error(f"Error al BORRAR PRODUCTO: {e}"), 500
        return render_template("producto/producto_tabla.html")
