# main.py

import os
import sys
from extensions import app
from flask import render_template
from database import db_setup as setupDB
from database import db_record as recordDB
from routes.auth_routes import auth
from routes.clientes_routes import cliente
from routes.trabajadores_routes import trabajador
from routes.categorias_routes import categoria
from routes.productos_routes import producto
from routes.carrito_routes import carrito
from routes.pedidos_routes import pedido
from routes.error_routes import error
from routes.extra_routes import extra

from config.config import Config
from logs import logger

# Cargar configuración
app.config.from_object(Config)
logger.info("Configuración de Flask cargada correctamente.")

# Registrar blueprints
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(cliente, url_prefix="/cliente")
app.register_blueprint(trabajador, url_prefix="/trabajador")
app.register_blueprint(categoria, url_prefix="/categoria")
app.register_blueprint(producto, url_prefix="/producto")
app.register_blueprint(carrito, url_prefix="/carrito")
app.register_blueprint(pedido, url_prefix="/pedido")
app.register_blueprint(extra, url_prefix="/extra")
app.register_blueprint(error, url_prefix="/error")

logger.info("Blueprints registrados correctamente.")

conexion = None

def inicializar_aplicacion(app):
    # Inicializar la base de datos y las tablas una sola vez
     with app.app_context():
        setupDB.get_db()  # Asegura la conexión inicial
        setupDB.comprobar_o_crear_base_de_datos()
        setupDB.crear_tablas()
        recordDB.crear_datos()
        setupDB.close_db()  # Cierra la conexión después de la inicialización

@app.before_request
def cargar():
    # Conectar a la base de datos en cada solicitud
    setupDB.get_db()

@app.teardown_appcontext
def cerrar_conexion(e=None):
    # Cerrar la conexión después de cada solicitud
    setupDB.close_db(e)

    
@app.route("/", endpoint="index")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    try:
        # Agregar el directorio raíz al PYTHONPATH (soluciona posibles problemas de importación)
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        logger.debug("Directorio raíz añadido al PYTHONPATH.")
        
        inicializar_aplicacion(app)
        logger.info("Iniciando el servidor Flask en modo debug...")
        app.run(debug=True)
    except Exception as e:
        logger.exception("Error crítico al iniciar la aplicación Flask:")

