# from PIL import Image
from flask import Blueprint, redirect, render_template, url_for, request
from database.db_setup import get_db
from logs import logger
import repositories.rep_producto as productoDB
import repositories.rep_categoria as categoriaDB
from routes.auth_routes import access_required

# Blueprint
producto = Blueprint("producto", __name__)


@producto.before_request
def cargar():
    global conexion
    conexion = get_db()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@producto.route("/mostrar_productos", methods=["GET"], endpoint="mostrar_productos")
@access_required('trabajador')
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
  
@producto.route("/mostrar_producto_detalle/<int:id_producto>", methods=["GET", "POST"], endpoint="mostrar_producto_detalle")
def mostrar_producto_detalle(id_producto):
    try:
        producto = productoDB.obtener_producto_id(id_producto)
        if producto:
            logger.info(f"PRODUCTO DETALLE PARA CLIENTE O ADMIN: {producto['nombre_producto']}")
            return render_template(
                "producto/producto_detalle.html",
                producto=producto,
                id_producto=id_producto,  # id_producto explícitamente
                editando=False
            ), 200
        else:
            logger.warning(f"No se encontró el producto con ID {id_producto}")
            return render_template("index.html", mensaje="Producto no encontrado"), 404
    except Exception as e:
        logger.error(f"Error OBTENIENDO DETALLE PRODUCTO con ID {id_producto}: {e}")
        return render_template("index.html", mensaje="Error al obtener los detalles del producto"), 500
    
@producto.route('/ruta_crear_producto', methods=['GET', 'POST'], endpoint="ruta_crear_producto")
@access_required('trabajador')
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
            precio_unidad = request.form.get('precio_unidad')
            imagen = request.files.get('imagen')
            id_categoria_FK = request.form.get('id_categoria_FK')

            # Validar datos
            if not (nombre and descripcion and precio_unidad and id_categoria_FK):
                logger.error("Faltan campos requeridos.", error="Todos los campos son obligatorios."), 404
                return redirect (url_for("producto.mostrar_productos"))

            try:
                precio_unidad = float(precio_unidad)
            except ValueError:
                logger.error("Precio inválido.", error="El precio debe ser un número."), 400
                

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
                    logger.error(f"Error al guardar la imagen: {e}", error="Error al cargar la imagen."), 400
                    return redirect (url_for("producto.mostrar_productos"))
            else:
                logger.info("No se proporcionó imagen. Campo 'imagen' quedará como NULL.")


            # Validar categoría
            if not categoriaDB.obtener_categoria_id(id_categoria_FK):
                logger.error(f"Categoría ID {id_categoria_FK} no válida.", error="Categoría no válida."), 400
                return redirect (url_for("producto.mostrar_productos"))

            logger.info(f"Ruta de la imagen antes del INSERT: {ruta_imagen}")
            logger.info(f"Llamando a crear_producto con: {nombre}, {descripcion}, {precio_unidad}, {nombre_imagen}, {id_categoria_FK}")
            # Insertar el producto
            productoDB.crear_producto(nombre, descripcion, precio_unidad, nombre_imagen, id_categoria_FK)
            logger.info(f"Producto creado: {nombre}, {descripcion}, {precio_unidad}, {nombre_imagen}, {id_categoria_FK}"), 200

            return redirect (url_for("producto.mostrar_productos"))
        

    except Exception as e:
        logger.error(f"Error en la ruta: {e}")
        return render_template('producto/producto_nuevo.html', error="Error al procesar el formulario.")

@producto.route("/editar_producto/<int:id_producto>", methods=["GET", "POST"], endpoint="ruta_editar_producto")
@access_required('trabajador')
def ruta_editar_producto(id_producto):
    try:
        if request.method == "GET":
            producto = productoDB.obtener_producto_id(id_producto)
            categorias = categoriaDB.obtener_categorias()
            if producto:
                logger.info(f"PRODUCTO OBTENIDO POR 'ID': {id_producto}")
                return render_template('producto/producto_editar.html', producto=producto, categorias=categorias)
            else:
                logger.warning(f"Producto con ID {id_producto} no encontrado.")
                return render_template("error/404.html"), 404

        elif request.method == "POST":
            nombre_producto = request.form.get("nombre_producto")
            descripcion = request.form.get("descripcion")
            precio_unidad = request.form.get("precio_unidad")
            imagen = request.form.get("imagen")
            id_categoria_FK = request.form.get("id_categoria_FK")            

            if not all([nombre_producto, id_categoria_FK, precio_unidad]):
                logger.warning("Datos incompletos para actualizar el producto.", extra={"error": "Faltan datos obligatorios"})
                return redirect(url_for("producto.mostrar_productos")), 400

            # Validar categoría
            if not categoriaDB.obtener_categoria_id(id_categoria_FK):
                logger.error(f"Categoría ID {id_categoria_FK} no válida.", error="Categoría no válida."), 400
                return redirect (url_for("producto.mostrar_productos"))
            
            producto_actualizado = productoDB.actualizar_producto(
                id_producto,
                nombre_producto,
                descripcion,
                float(precio_unidad),
                imagen,
                int(id_categoria_FK),
            )
            
            if producto_actualizado:
                logger.info(f"PRODUCTO ACTUALIZADO EXITOSAMENTE: {producto_actualizado['nombre_producto']}", extra={"success": "Producto actualizado"})
                return redirect(url_for("producto.mostrar_productos"))
            else:
                logger.error(f"Error al actualizar el producto con ID {id_producto}.", extra={"error": "Producto no actualizado"})
                return render_template("error/404.html"), 404

    except Exception as e:
        logger.error(f"Error al ACTUALIZAR PRODUCTO: {e}")
        return render_template("error/500.html"), 500

@producto.route("/borrar_producto", methods=["GET", "POST"], endpoint="ruta_borrar_producto")
@access_required('trabajador')
def ruta_borrar_producto():
    try:
        if request.method == "POST":
            producto_id = request.form.get("id_producto")
            producto = productoDB.obtener_producto_id(producto_id)
            if producto:
                productoDB.borrar_producto(producto_id)
                logger.info(f"PRODUCTO BORRADO: {producto['nombre_producto']}"), 200
                return redirect (url_for("producto.mostrar_productos"))
            else:
                logger.warning(f"Producto con ID {producto_id} no encontrado."), 404
                return redirect (url_for("producto.mostrar_productos"))
    except Exception as e:
        logger.error(f"Error al BORRAR PRODUCTO: {e}"), 500
        return redirect (url_for("producto.mostrar_productos"))