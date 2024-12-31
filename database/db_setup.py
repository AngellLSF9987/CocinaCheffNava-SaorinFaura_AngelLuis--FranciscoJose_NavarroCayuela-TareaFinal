# database/db_setup.py

from flask import g
import mysql.connector
from config.config import Config
from mysql.connector import Error
import logging

logger = logging.getLogger(__name__)


def get_db():
    """Obtiene una conexión a MySQL y la almacena en `g`."""
    if "db" not in g:
        try:
            db_config = Config.MYSQL_CONFIG
            if db_config is not None:
                logger.info("Creando conexión a MySQL con la base de datos seleccionada.")
                g.db = mysql.connector.connect(**db_config)
            else:
                logger.error("Configuración de base de datos no encontrada.")
                raise ValueError("No se encontró la configuración de base de datos.")
        except Error as e:
            logger.error(f"Error al conectar a MySQL: {e}")
            raise e
    return g.db

def close_db(e=None):
    """Cierra la conexión a la base de datos si existe."""
    db = g.pop("db", None)

    if db is not None:
        db.close()
        logger.info("Conexión a MySQL cerrada correctamente")

def registrar_y_mostrar(mensaje, nivel="info"):
    """Registra un mensaje y lo imprime."""
    niveles = {
        "info": logger.info,
        "warning": logger.warning,
        "error": logger.error,
    }
    # print(mensaje)
    niveles.get(nivel, logger.info)(mensaje)

def comprobar_o_crear_base_de_datos():
    """Comprueba si existe la base de datos, si no existe la crea."""
    conn = get_db()
    cursor = conn.cursor()
    nombre_base_datos = Config.MYSQL_CONFIG.get("database")
    try:
        logger.info("LISTADO de todas las bases de datos MYSQL en phpMyAdmin")
        # print("LISTADO de todas las bases de datos MYSQL en phpMyAdmin")

        # Comprobar si la base de datos existe
        cursor.execute("SHOW DATABASES")
        bases_de_datos = [db[0] for db in cursor.fetchall()]

        if nombre_base_datos not in bases_de_datos:
            mensaje = f"La base de datos '{nombre_base_datos}' no existe. Creándola..."
            registrar_y_mostrar(mensaje, nivel="info")
            cursor.execute(f"CREATE DATABASE {nombre_base_datos}")
            registrar_y_mostrar(f"Base de datos '{nombre_base_datos}' creada exitosamente.", nivel="info")
        else:
            registrar_y_mostrar(f"La base de datos '{nombre_base_datos}' ya existe.", nivel="info")

        # Seleccionar la base de datos
        conn.database = nombre_base_datos
    except Exception as e:
        registrar_y_mostrar(f"Error al comprobar o crear la base de datos: {e}", nivel="warning")
    finally:
        cursor.close()

def crear_tablas():
    """Controlador principal que verifica la creación de tablas y datos iniciales."""
    conn = get_db()
    try:
        cursor = conn.cursor()
        funciones_creacion = [
            crear_tabla_roles,
            crear_tabla_usuarios,
            crear_tabla_clientes,
            crear_tabla_trabajadores,
            crear_tabla_categorias,
            crear_tabla_productos,
            crear_tabla_carrito,
            crear_tabla_pedidos,
            crear_tabla_pedidos_productos
        ]
        for funcion in funciones_creacion:
            funcion(cursor)
        conn.commit()
        registrar_y_mostrar("✅ Tablas y datos iniciales procesados correctamente.", nivel="info")
    except Exception as e:
        registrar_y_mostrar(f"❌ Error al procesar las tablas o datos: {e}", nivel="error")
        conn.rollback()
    finally:
        cursor.close()
        close_db()

def crear_tabla_roles(cursor):
    """Crea la tabla Roles."""
    try:
        mensaje = "Creando tabla Roles."
        registrar_y_mostrar(mensaje, nivel="info")
        cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Roles (
                            id_rol INT AUTO_INCREMENT PRIMARY KEY,
                            nombre_rol VARCHAR(255) UNIQUE NOT NULL,
                            fecha_registro DATE DEFAULT CURRENT_DATE,
                            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP                            
                    );
            """
            )
        registrar_y_mostrar("Tabla Roles creada exitosamente.", nivel="info")
    except Exception as e:
        registrar_y_mostrar(f"Error al crear la tabla Roles: {e}", nivel="error")

def crear_tabla_usuarios(cursor):
    """Crea la tabla Usuarios."""
    try:
        mensaje = "Creando tabla Usuarios."
        registrar_y_mostrar(mensaje, nivel="info")
        cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Usuarios (
                            id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                            email VARCHAR(255) NOT NULL UNIQUE,
                            contraseña VARCHAR(255) NOT NULL UNIQUE,
                            fecha_registro DATE DEFAULT CURRENT_DATE,
                            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                            id_rol_FK INT,
                        
                        FOREIGN KEY (id_rol_FK) REFERENCES Roles(id_rol)
                );
            """
            )
        registrar_y_mostrar("Tabla Usuarios creada exitosamente.", nivel="info")
    except Exception as e:
        registrar_y_mostrar(f"Error al crear la tabla Usuarios: {e}", nivel="error")

def crear_tabla_clientes(cursor):
    """Crea la tabla Clientes."""
    try:
        mensaje = "Creando tabla Clientes."
        registrar_y_mostrar(mensaje, nivel="info")
        cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Clientes (
                            id_cliente INT AUTO_INCREMENT PRIMARY KEY,
                            nombre_cliente VARCHAR(255) NOT NULL,
                            apellido1 VARCHAR(255) NOT NULL,
                            apellido2 VARCHAR(255) NOT NULL,
                            dni_cliente VARCHAR(9) UNIQUE NOT NULL,       
                            telefono VARCHAR(9) NOT NULL,
                            direccion VARCHAR(255) NOT NULL,
                            email VARCHAR(255) NOT NULL,
                            fecha_registro DATE DEFAULT CURRENT_DATE,
                            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,                            
                            id_usuario_FK INT,
                        
                        FOREIGN KEY (id_usuario_FK) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE
                    );
            """
            )
        registrar_y_mostrar("Tabla Clientes creada exitosamente.", nivel="info")
    except Exception as e:
        registrar_y_mostrar(f"Error al crear la tabla Clientes: {e}", nivel="error")

def crear_tabla_trabajadores(cursor):
    """Crea la tabla Trabajadores."""
    try:
        mensaje = "Creando tabla Trabajadores."
        registrar_y_mostrar(mensaje, nivel="info")
        cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Trabajadores (
                            id_trabajador INT AUTO_INCREMENT PRIMARY KEY,
                            nombre_trabajador VARCHAR(255) NOT NULL,
                            apellido1 VARCHAR(255) NOT NULL,
                            apellido2 VARCHAR(255) NOT NULL,
                            dni_trabajador VARCHAR(9) UNIQUE NOT NULL,
                            telefono VARCHAR(9) NOT NULL,
                            direccion VARCHAR(255) NOT NULL,
                            email VARCHAR(255) NOT NULL,
                            fecha_registro DATE DEFAULT CURRENT_DATE,
                            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,                            
                            id_usuario_FK INT,
                        
                        FOREIGN KEY (id_usuario_FK) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE                  
                    );
            """
            )
        registrar_y_mostrar("Tabla Trabajadores creada exitosamente.", nivel="info")
    except Exception as e:
        registrar_y_mostrar(f"Error al crear la tabla Trabajadores: {e}", nivel="error")

def crear_tabla_categorias(cursor):
    """Crea la tabla Categorias."""
    try:
        mensaje = "Creando tabla Categorias."
        registrar_y_mostrar(mensaje, nivel="info")
        cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Categorias (
                            id_categoria INT AUTO_INCREMENT PRIMARY KEY,
                            nombre_categoria VARCHAR(255),
                            descripcion TEXT,
                            imagen VARCHAR(255),
                            fecha_registro DATE DEFAULT CURRENT_DATE,
                            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP                            
                    );
            """
            )
        registrar_y_mostrar("Tabla Categorias creada exitosamente.", nivel="info")
    except Exception as e:
        registrar_y_mostrar(f"Error al crear la tabla Categorias: {e}", nivel="error")

def crear_tabla_productos(cursor):
    """Crea la tabla Productos."""
    try:
        mensaje = "Creando tabla Productos."
        registrar_y_mostrar(mensaje, nivel="info")
        cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Productos (
                                id_producto INT AUTO_INCREMENT PRIMARY KEY,
                                nombre_producto TEXT,
                                descripcion TEXT,
                                precio_unidad DECIMAL(10, 2) NOT NULL,
                                imagen VARCHAR(255),
                                id_categoria_FK INT,
                                fecha_registro DATE DEFAULT CURRENT_DATE,
                                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                            FOREIGN KEY (id_categoria_FK) REFERENCES Categorias(id_categoria)   
                    );
            """
            )
        registrar_y_mostrar("Tabla Productos creada exitosamente.", nivel="info")
    except Exception as e:
        registrar_y_mostrar(f"Error al crear la tabla Productos: {e}", nivel="error")

            
def crear_tabla_carrito(cursor):
    """Crea la tabla Carrito."""
    try:
        mensaje = "Creando tabla Carrito."
        registrar_y_mostrar(mensaje, nivel="info")            
        cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Carrito (
                                id_carrito INT AUTO_INCREMENT PRIMARY KEY,
                                id_cliente_FK INT NOT NULL,
                                id_producto_FK INT NOT NULL,
                                cantidad_por_producto INT NOT NULL,
                                precio_carrito DECIMAL(10, 2) NOT NULL,
                                fecha_registro DATE DEFAULT CURRENT_DATE,
                                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                            FOREIGN KEY (id_cliente_FK) REFERENCES Clientes(id_cliente),
                            FOREIGN KEY (id_producto_FK) REFERENCES Productos(id_producto)
                    );
            """
            )
        registrar_y_mostrar("Tabla Carrito creada exitosamente.", nivel="info")
    except Exception as e:
        registrar_y_mostrar(f"Error al crear la tabla Carrito: {e}", nivel="error")

def crear_tabla_pedidos(cursor):
    """Crea la tabla Pedidos."""
    try:
        mensaje = "Creando tabla Pedidos."
        registrar_y_mostrar(mensaje, nivel="info") 
        cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Pedidos (
                                id_pedido INT AUTO_INCREMENT PRIMARY KEY,
                                num_pedido INT,
                                id_cliente_FK INT,
                                cantidad_productos INT,
                                fecha_registro DATE DEFAULT CURRENT_DATE,
                                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                            FOREIGN KEY (id_cliente_FK) REFERENCES Clientes(id_cliente)
                    );
            """
            )
        registrar_y_mostrar("Tabla Pedidos creada exitosamente.", nivel="info")
    except Exception as e:
        registrar_y_mostrar(f"Error al crear la tabla Pedidos: {e}", nivel="error")


def crear_tabla_pedidos_productos(cursor):
    """Crea la tabla Pedidos_Productos."""
    try:
        mensaje = "Creando tabla Pedidos_Productos."
        registrar_y_mostrar(mensaje, nivel="info")
        cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Pedidos_Productos (
                                id_pedido_FK INT NOT NULL,
                                id_producto_FK INT NOT NULL,
                                cantidad_por_producto INT NOT NULL,
                                precio_total DECIMAL(10, 2) NOT NULL,
                                fecha_registro DATE DEFAULT CURRENT_DATE,
                                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                            PRIMARY KEY (id_pedido_FK, id_producto_FK),
                            FOREIGN KEY (id_pedido_FK) REFERENCES Pedidos(id_pedido) ON DELETE CASCADE,
                            FOREIGN KEY (id_producto_FK) REFERENCES Productos(id_producto) ON DELETE CASCADE
                    );
            """
        )
        registrar_y_mostrar("Tabla Pedidos_Productos creada exitosamente.", nivel="info")
    except Exception as e:
        registrar_y_mostrar(f"Error al crear la tabla Pedidos_Productos: {e}", nivel="error")
