from flask import Blueprint, render_template, redirect
from database.db_setup import get_db
from logs import logger
import repositories.rep_trabajador as trabajadorDB
import repositories.rep_producto as productoDB
import repositories.rep_cliente as clienteDB
import repositories.rep_categoria as categoriaDB

# Blueprint
trabajador = Blueprint("trabajador", __name__)

@trabajador.before_request
def cargar():
    global conexion
    conexion = get_db()

@trabajador.route("/mostrar_trabajadores")
def mostrar_trabajadores():
    try:
        trabajadores = trabajadorDB.obtener_trabajadores()
        if trabajador in trabajadores:
            logger.info("REDIRECCIONANDO A LISTADO DE TRABAJADORES DESDE AMDIN"), 200
            return render_template("trabajador/trabajador_tabla.html", trabajadores=trabajadores)
        else:
            logger.error("ERROR OBTENIENDO TRABAJADORES - GESTIÓN DE TRABAJADORES"), 404
            redirect("/")            
    except Exception as e:
        logger.error(f"Error al MOSTRAR TRABAJADORES DESDE ADMIN: {e}"), 500
        redirect("/")      
      

@trabajador.route("/gestion_productos", methods=["GET"], endpoint="gestion_productos")
def gestion_productos():
    try:
        productos = productoDB.obtener_productos()
        if productos:
            logger.info("OBTENIENDO PRODUCTOS DESDE ADMIN"), 200
            return render_template('producto/producto_tabla.html', productos=productos)
        else:
            logger.warning("No se encontraron productos"), 404
            return redirect("/")
    except Exception as e:
        logger.error(f"Error OBTENIENDO PRODUCTOS DESDE ADMIN: {e}"), 500
        return redirect("/") 


@trabajador.route("/gestionar_categorias", methods=["GET"], endpoint="gestionar_categorias")
def gestionar_categorias():
    try:
        categorias = categoriaDB.obtener_categorias()
        if categorias:
            logger.info("OBTENIENDO CATEGORÍAS - GESTIÓN DE CATEGORÍAS"), 200
            return redirect("categoria/categoria_tabla.html")
        else:
            logger.error("ERROR OBTENIENDO CATEGORÍAS - GESTIÓN DE CATEGORÍAS"), 404
            redirect("/")
    except Exception as e:
        logger.error(f"Error OBTENIENDO CATEGORÍAS DESDE ADMIN: {e}"), 500
        redirect("/")        


@trabajador.route("/gestionar_clientes", methods=["GET"], endpoint="gestionar_clientes")
def gestionar_clientes():
    try:
        clientes = clienteDB.obtener_clientes()
        if clientes:
            logger.info("OBTENIENDO CLIENTES - GESTIÓN DE CLIENTES"), 200
            return render_template("cliente/cliente_tabla.html")
        else:
            logger.error("ERROR OBTENIENDO CATEGORÍAS - GESTIÓN DE CATEGORÍAS"), 404
            redirect("/")
    except Exception as e:
        logger.error(f"Error OBTENIENDO PRDOCUTOS DESDE ADMIN: {e}"), 500
        redirect("/")         
