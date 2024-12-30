from flask import Blueprint, render_template, redirect, request, url_for, jsonify
from database.db_setup import get_db
import repositories.rep_categoria as categoriaDB
from logs import logger
from routes.auth_routes import access_required


# Blueprint
categoria = Blueprint("categoria", __name__)


@categoria.before_request
def cargar():
    global conexion
    conexion = get_db()


@categoria.route("/categoria_template")
def categoria_template():
    return render_template("categoria/categoria.html")


@categoria.route("/mostrar_categorias", methods=["GET"], endpoint="mostrar_categorias")
@access_required('trabajador')
def mostrar_categorias():
    """Ruta para listar todas las Categorías desde ADMIN."""
    try:
        categorias = categoriaDB.obtener_categorias()
        logger.info("OBTENIENDO LISTADO DE CATEGORÍAS DESDE ADMIN")
        return render_template("categoria/categoria_tabla.html", categorias=categorias), 200
    except Exception as e:
        logger.error(f"Error al MOSTRAR CATEGORÍAS DESDE ADMIN: {e}")
        return render_template("categoria/categoria_tabla.html", mensaje="Error al obtener las categorías"), 500

@categoria.route("/listar_categorias", methods=["GET"], endpoint="listar_categorias")
def listar_categorias():
    """Ruta para listar todas las Categorías desde CLIENTE."""
    try:
        categorias = categoriaDB.obtener_categorias()
        if categorias:
            logger.info("OBTENIENDO LISTADO DE CATEGORIAS DESDE AMDIN"), 200
            return render_template("categoria/categoria.html", categorias=categorias), 200
        else:
            logger.error(f"Error al MOSTRAR CATEGORÍAS DESDE ADMIN: {e}"), 404            
            return redirect("/")
    except Exception as e:
        logger.error(f"Error al MOSTRAR CATEGORÍAS DESDE ADMIN: {e}"), 500
        return redirect("/")

@categoria.route("/mostrar_categoria_detalle/<int:id_categoria>", methods=["GET", "POST"], endpoint="mostrar_categoria_detalle")
def mostrar_categoria_detalle(id_categoria):
    try:
        categoria = categoriaDB.obtener_categoria_id(id_categoria)
        if categoria:
            logger.info(f"CATEGORÍA DETALLE PARA CLIENTE O ADMIN: {categoria['nombre_categoria']}")
            logger.info(f"Valor de categoria.imagen: {categoria['imagen']}")
            return render_template(
                "categoria/categoria_detalle.html",
                categoria=categoria,
                id_categoria=id_categoria,  # Pasamos id_categoria explícitamente
                editando=False
            ), 200
        else:
            logger.warning(f"No se encontró la categoría con ID {id_categoria}")
            return render_template("categoria/categoria_tabla.html", mensaje="Categoría no encontrada"), 404
    except Exception as e:
        logger.error(f"Error al MOSTRAR CATEGORÍA DETALLE PARA CLIENTE O ADMIN con ID {id_categoria}: {e}")
        return render_template("categoria/categoria_tabla.html", mensaje="Error al obtener los detalles de la categoría"), 500

@categoria.route('/ruta_crear_categoria', methods=['GET', 'POST'], endpoint="ruta_crear_categoria")
@access_required('trabajador')
def ruta_crear_categoria():
    try:
        # Manejo explícito de GET: mostrar el formulario para crear una categoría
        if request.method == 'GET':
            logger.info("Mostrando formulario para crear una categoría.")
            return render_template('categoria/categoria_nueva.html')

        # Manejo de POST: procesar el formulario
        if request.method == 'POST':
            logger.info("Procesando formulario para crear una categoría...")

            # Obtener datos del formulario
            nombre_categoria = request.form.get('nombre_categoria')
            descripcion = request.form.get('descripcion')
            imagen = request.files.get('imagen')

            # Validar datos
            if not (nombre_categoria and descripcion):
                logger.error("Faltan campos requeridos.", error="Todos los campos son obligatorios.")
                return render_template('categoria/categoria_nueva.html', error="Todos los campos son obligatorios.")

            # Guardar la imagen
            ruta_imagen = None  # Por defecto es None
            if imagen and imagen.filename != '':
                try:
                    # Guardamos solo el nombre del archivo, no la ruta completa
                    nombre_imagen = imagen.filename  # Esto extrae el nombre del archivo
                    ruta_imagen = f"static/images/categorias/{nombre_imagen}"
                    imagen.save(ruta_imagen)
                    logger.info(f"Imagen guardada correctamente: {ruta_imagen}")
                except Exception as e:
                    logger.error(f"Error al guardar la imagen: {e}", error="Error al cargar la imagen.")
                    return redirect(url_for("categoria.mostrar_categorias"))
            else:
                logger.info("No se proporcionó imagen. Campo 'imagen' quedará como NULL.")

            # Insertar la categoría en la base de datos
            categoriaDB.crear_categoria(nombre_categoria, descripcion, ruta_imagen)
            logger.info(f"Categoría creada: {nombre_categoria}, {descripcion}, {ruta_imagen}")

            return redirect(url_for("categoria.mostrar_categorias"))

    except Exception as e:
        logger.error(f"Error al crear categoría: {e}")
        return render_template('error/500.html', mensaje="Error al crear la categoría")

@categoria.route('/ruta_editar_categoria/<int:id_categoria>', methods=['GET', 'POST'], endpoint="ruta_editar_categoria")
@access_required('trabajador')
def ruta_editar_categoria(id_categoria):
    try:
        if request.method == 'GET':
            categoria = categoriaDB.obtener_categoria_id(id_categoria)
            if categoria:
                logger.info(f"Mostrando formulario para editar categoría ID {id_categoria}")
                return render_template('categoria/categoria_editar.html', categoria=categoria), 200
            else:
                logger.warning(f"Categoría con ID {id_categoria} no encontrada.")
                return render_template('categoria/categoria_tabla.html', error="Categoría no encontrada."), 404

        if request.method == 'POST':
            logger.info("Procesando formulario para editar categoría...")
            nombre_categoria = request.form.get('nombre_categoria')
            descripcion = request.form.get('descripcion')
            imagen = request.files.get('imagen')

            # Actualizar categoría
            categoria_actualizada = categoriaDB.actualizar_categoria(
                id_categoria, 
                nombre_categoria, 
                descripcion, 
                imagen,
            )
            if categoria_actualizada:
                logger.info(f"Categoría actualizada: {categoria_actualizada['nombre_categoria']}")
                return render_template('categoria/categoria_tabla.html', mensaje="Categoría actualizada exitosamente.")
            else:
                logger.error(f"No se pudo actualizar la categoría con ID {id_categoria}.")
                return render_template('categoria/categoria_tabla.html', error="Error al actualizar la categoría.")

    except Exception as e:
        logger.error(f"Error al actualizar la categoría con ID {id_categoria}: {e}")
        return render_template('categoria/categoria_tabla.html', error="Ocurrió un error inesperado.")

@categoria.route("/ruta_borrar_categoria", methods=["POST"], endpoint="ruta_borrar_categoria")
@access_required('trabajador')
def ruta_borrar_categoria():
    try:
        # Obtener ID de la categoría del formulario
        id_categoria = request.form.get("id_categoria")

        if not id_categoria:
            logger.warning("ID de categoría no proporcionado.")
            return render_template("categoria/categoria_tabla.html"), 400  # Bad Request

        # Buscar la categoría en la base de datos
        categoria = categoriaDB.obtener_categoria_id(id_categoria)
        if categoria:
            # Borrar la categoría si existe
            categoriaDB.borrar_categoria(id_categoria)
            logger.info(f"CATEGORIA BORRADA: ID {id_categoria}")
            return render_template("categoria/categoria_tabla.html"), 200  # OK
        else:
            logger.warning(f"Categoría con ID {id_categoria} no encontrada.")
            return render_template("categoria/categoria_tabla.html"), 404  # Not Found
          
    except Exception as e:
        logger.error(f"Error al BORRAR CATEGORIA DESDE ADMIN: {e}")
        return render_template("categoria/categoria_tabla.html"), 500  # Internal Server Error

