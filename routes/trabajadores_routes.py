from flask import Blueprint, flash, render_template, redirect, session, url_for
from database.db_setup import get_db
from logs import logger
import repositories.rep_trabajador as trabajadorDB
import repositories.rep_producto as productoDB
import repositories.rep_cliente as clienteDB
import repositories.rep_categoria as categoriaDB
from routes.auth_routes import access_required

# Blueprint
trabajador = Blueprint("trabajador", __name__)

@trabajador.before_request
def cargar():
    global conexion
    conexion = get_db()

@trabajador.route("/mostrar_trabajadores", methods=["GET"], endpoint="gestion_trabajadores")
@access_required
def mostrar_trabajadores():
    try:
        trabajadores = trabajadorDB.obtener_trabajadores()
        if trabajador in trabajadores:
            logger.info("REDIRECCIONANDO A LISTADO DE TRABAJADORES DESDE AMDIN"), 200
            return render_template("trabajador/trabajador_tabla.html", trabajadores=trabajadores)
        else:
            logger.error("ERROR OBTENIENDO TRABAJADORES - GESTIÓN DE TRABAJADORES"), 404
            render_template("index.html")             
    except Exception as e:
        logger.error(f"Error al MOSTRAR TRABAJADORES DESDE ADMIN: {e}"), 500
        render_template("index.html")       
      
# Ruta para el detalle del trabajador
@trabajador.route('/trabajador_detalle/<int:id_trabajador>', methods=["GET", "POST"], endpoint="perfil_trabajador")
@access_required('trabajador')
def trabajador_detalle(id_trabajador):
    if session.get("trabajador") and session["trabajador"]["id_trabajador"] == id_trabajador:
        trabajador = trabajadorDB.obtener_trabajador_id(id_trabajador)  # Asume que tienes una función similar en tu capa de datos
        if trabajador:
            return render_template("trabajador/trabajador_detalle.html", trabajador=trabajador, id_trabajador=id_trabajador)
    else:
        flash("No tienes acceso a este perfil.", "warning")
        return redirect(url_for("index"))


@trabajador.route("/gestion_productos", methods=["GET"], endpoint="gestion_productos")
@access_required
def gestion_productos():
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


@trabajador.route("/gestionar_categorias", methods=["GET"], endpoint="gestionar_categorias")
@access_required
def gestionar_categorias():
    try:
        categorias = categoriaDB.obtener_categorias()
        if categorias:
            logger.info("OBTENIENDO CATEGORÍAS - GESTIÓN DE CATEGORÍAS"), 200
            return redirect("categoria/categoria_tabla.html")
        else:
            logger.error("ERROR OBTENIENDO CATEGORÍAS - GESTIÓN DE CATEGORÍAS"), 404
            render_template("index.html")
    except Exception as e:
        logger.error(f"Error OBTENIENDO CATEGORÍAS DESDE ADMIN: {e}"), 500
        render_template("index.html")        


@trabajador.route("/gestionar_clientes", methods=["GET"], endpoint="gestionar_clientes")
@access_required
def gestionar_clientes():
    try:
        clientes = clienteDB.obtener_clientes()
        if clientes:
            logger.info("OBTENIENDO CLIENTES - GESTIÓN DE CLIENTES"), 200
            return render_template("cliente/cliente_tabla.html")
        else:
            logger.error("ERROR OBTENIENDO CATEGORÍAS - GESTIÓN DE CATEGORÍAS"), 404
            render_template("index.html")
    except Exception as e:
        logger.error(f"Error OBTENIENDO PRDOCUTOS DESDE ADMIN: {e}"), 500
        render_template("index.html")         
