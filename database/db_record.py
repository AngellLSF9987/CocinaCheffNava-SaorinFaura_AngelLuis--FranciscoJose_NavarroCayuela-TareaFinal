# database/db_record.py
import database.db_setup as setupDB
import logging
from logs import logger

logger = logging.getLogger(__name__)


def crear_datos():
    """
    Controlador principal para insertar datos iniciales en la base de datos.
    """
    conn = setupDB.get_db()
    try:
        cursor = conn.cursor()
        insertar_roles(cursor)
        insertar_usuarios(cursor)
        insertar_clientes(cursor)
        insertar_trabajadores(cursor)
        insertar_categorias(cursor)
        insertar_productos(cursor)

        conn.commit()
        # print("✅ Datos iniciales insertados correctamente.")
        logger.info("✅ Datos iniciales insertados correctamente.")
    except Exception as e:
        conn.rollback()
        # print(f"❌ Error al insertar datos iniciales: {e}")
        logger.error(f"❌ Error al insertar datos iniciales: {e}")
    finally:
        # The above code is calling the `setupDBclose_db()` function in Python. This function is
        # likely responsible for setting up a database connection and then closing it after performing
        # some operations.
        setupDB.close_db()


def insertar_roles(cursor):
    datos_roles = [
        (1, "cliente"),
        (2, "trabajador"),
    ]
    for id_rol, nombre_rol in datos_roles:
        cursor.execute("SELECT 1 FROM Roles WHERE nombre_rol = %s", (nombre_rol,))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO Roles (id_rol, nombre_rol) VALUES (%s, %s);",
                (id_rol, nombre_rol),
            )
            # print(f"✔️ Rol '{nombre_rol}' insertado.")            
            logger.info(f"✔️ Rol '{nombre_rol}' insertado.")
        else:
            # print(f"⚠️ Rol '{nombre_rol}' ya existe.")            
            logger.info(f"⚠️ Rol '{nombre_rol}' ya existe.")


def insertar_usuarios(cursor):

    # Insertar usuarios en la tabla Usuarios
    datos_usuarios = [
        ("paco@nava.com", "paco123", 1),
        ("angel@saorin.com", "angel123", 1),
        ("paco@trabajador.com", "paco456", 2),
        ("angel@trabajador.com", "angel456", 2),
    ]
    print(f"Listado Usuarios: {datos_usuarios}")
    logger.info(f"Listado Usuarios: {datos_usuarios}")

    for email, contraseña, id_rol_FK in datos_usuarios:
        cursor.execute("SELECT 1 FROM Usuarios WHERE email = %s", (email,))
        if not cursor.fetchone():
            cursor.execute(
                """INSERT INTO Usuarios (email, contraseña, id_rol_FK) VALUES (%s, %s, %s);""",
                (email, contraseña, id_rol_FK),
            )
            # print(f"✔️ Usuario {email} insertado.")
            logger.info(f"✔️ Usuario {email} insertado.")
        else:
            # print(f"⚠️ Usuario {email} ya existe, no se insertó.")
            logger.info(f"⚠️ Usuario {email} ya existe, no se insertó.")


def insertar_clientes(cursor):
    # Insertar clientes en la tabla Clientes
    datos_clientes = [
        (
            "Francisco José",
            "Cayuela",
            "Navarro",
            "12345678A",
            "600123456",
            "Calle Luna, 6",
            "paco@nava.com",
        ),
        (
            "Angel Luis",
            "Saorin",
            "Faura",
            "12345678C",
            "610654321",
            "Calle Sol, 8",
            "angel@saorin.com",
        ),
    ]
    # print(f"Listado Clientes: {datos_clientes}")
    logger.info(f"Listado roles: {datos_clientes}")
    for (
        nombre_cliente,
        apellido1,
        apellido2,
        dni_cliente,
        telefono,
        direccion,
        email,
    ) in datos_clientes:
        cursor.execute("SELECT id_usuario FROM Usuarios WHERE email = %s", (email,))
        resultado = cursor.fetchone()
        if resultado:
            id_usuario = resultado[0]
            cursor.execute("SELECT 1 FROM Clientes WHERE email = %s", (email,))
            if not cursor.fetchone():
                cursor.execute(
                    """INSERT INTO Clientes 
                            (nombre_cliente, apellido1, apellido2, dni_cliente, telefono, direccion, email, id_usuario_FK)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                    (
                        nombre_cliente,
                        apellido1,
                        apellido2,
                        dni_cliente,
                        telefono,
                        direccion,
                        email,
                        id_usuario,
                    ),
                )
                # print(f"✔️ Cliente {nombre_cliente} insertado.")
                logger.info(f"✔️ Cliente {nombre_cliente} insertado.")
            else:
                # print(f"⚠️ Cliente {email} ya existe.")
                logger.info(f"⚠️ Cliente {email} ya existe.")
        else:
            # print(f"⚠️ Usuario {email} no encontrado para el cliente.")
            logger.info(f"⚠️ Usuario {email} no encontrado para el cliente.")


def insertar_trabajadores(cursor):
    # Insertar trabajadores en la tabla Trabajadores
    datos_trabajadores = [
        (
            "Paco",
            "Lopez",
            "Garcia",
            "12345678D",
            "620987654",
            "Calle Estrella, 10",
            "paco@trabajador.com",
        ),
        (
            "Angel",
            "Martinez",
            "Perez",
            "12345678F",
            "630456789",
            "Calle Cometa, 12",
            "angel@trabajador.com",
        ),
    ]
    print(f"Listado Trabajadores: {datos_trabajadores}")
    logger.info(f"Listado Trabajadores: {datos_trabajadores}")
    for (
        nombre_trabajador,
        apellido1,
        apellido2,
        dni_trabajador,
        telefono,
        direccion,
        email,
    ) in datos_trabajadores:
        cursor.execute("SELECT id_usuario FROM Usuarios WHERE email = %s", (email,))
        resultado = cursor.fetchone()
        if resultado:
            id_usuario = resultado[0]
            cursor.execute("SELECT 1 FROM Trabajadores WHERE email = %s", (email,))
            if not cursor.fetchone():
                cursor.execute(
                    """INSERT INTO Trabajadores 
                            (nombre_trabajador, apellido1, apellido2, dni_trabajador, telefono, direccion, email, id_usuario_FK)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                    (
                        nombre_trabajador,
                        apellido1,
                        apellido2,
                        dni_trabajador,
                        telefono,
                        direccion,
                        email,
                        id_usuario,
                    ),
                )
                # print(f"✔️ Trabajador {nombre_trabajador} insertado.")
                logger.info(f"✔️ Trabajador {nombre_trabajador} insertado.")
            else:
                # print(f"⚠️ Trabajador {email} ya existe.")
                logger.info(f"⚠️ Trabajador {email} ya existe.")
        else:
            # print(f"⚠️ Usuario {email} no encontrado para el trabajador.")
            logger.warning(f"⚠️ Usuario {email} no encontrado para el trabajador.")


def insertar_categorias(cursor):
    # Insertar categorías en la tabla Categorias
    datos_categorias = [
        ("Carnes", "Carnes a la parrilla y guisos de carne.", "carnes.png"),
        ("Pastas", "Platos de pasta italiana y fideos.", "pastas.png"),
        (
            "Comidas de Puchero",
            "Platos tradicionales de puchero.",
            "puchero.png",
        ),
        (
            "Pizzas",
            "Pizzas artesanales con ingredientes frescos.",
            "pizzas.png",
        ),
        ("Arroces", "Platos de arroz como paellas y risottos.", "arroces.png"),
        ("Asados", "Carnes y vegetales asados al horno.", "asados.png"),
        ("Ensaladas", "Ensaladas frescas y saludables.", "ensaladas.png"),
        ("Cervezas", "Cervezas nacionales e internacionales.", "cervezas.png"),
        (
            "Vinos",
            "Selección de vinos tintos, blancos y rosados.",
            "vinos.png",
        ),
        (
            "Refrescos con Gas y Sin Gas",
            "Refrescos variados con y sin gas.",
            "refrescos.png",
        ),
        (
            "Aguas, zumos y batidos",
            "Aguas minerales, zumos naturales y batidos.",
            "bebidas.png",
        ),
        ("Postres", "Dulces y postres caseros.", "postres.png"),
        ("Cafés", "Cafés calientes y fríos.", "cafes.png"),
    ]
    # print(f"Listado Categorías: {datos_categorias}")
    logger.info(f"Listado Categorías: {datos_categorias}")

    for nombre_categoria, descripcion, imagen in datos_categorias:
        cursor.execute(
            "SELECT 1 FROM Categorias WHERE nombre_categoria = %s",
            (nombre_categoria,),
        )
        if not cursor.fetchone():
            cursor.execute(
                """INSERT INTO Categorias (nombre_categoria, descripcion, imagen) 
                        VALUES (%s, %s, %s);""",
                (nombre_categoria, descripcion, imagen),
            )
            # print(f"✔️ Categoría '{nombre_categoria}' insertada.")
            logger.info(f"✔️ Categoría '{nombre_categoria}' insertada.")
        else:
            # print(f"⚠️ Categoría '{nombre_categoria}' ya existe, no se insertó.")
            logger.warning(
                f"⚠️ Categoría '{nombre_categoria}' ya existe, no se insertó."
            )


def insertar_productos(cursor):
    # Insertar productos en la tabla Productos
    datos_productos = [
        # Carnes
        (
            "Entrecot",
            "Entrecot a la parrilla con guarnición de papas.",
            15.99,
            "entrecot.png",
            1,
        ),
        (
            "Albóndigas en Salsa",
            "Albóndigas de carne en salsa casera.",
            9.50,
            "albondigas.png",
            1,
        ),
        # Pastas
        (
            "Espaguetis Carbonara",
            "Espaguetis con salsa carbonara casera.",
            8.99,
            "spagueti_carbonara.png",
            2,
        ),
        (
            "Lasaña de Verduras",
            "Lasaña vegetariana con capas de verduras frescas.",
            9.75,
            "lasana_verduras.png",
            2,
        ),
        # Comidas de Puchero
        (
            "Cocido Madrileño",
            "Cocido con garbanzos, carne y verduras.",
            12.50,
            "cocido.png",
            3,
        ),
        (
            "Lentejas con Chorizo",
            "Lentejas guisadas con chorizo.",
            10.00,
            "lentejas.png",
            3,
        ),
        # Pizzas
        (
            "Pizza Margarita",
            "Pizza clásica con tomate, queso y albahaca.",
            7.99,
            "margarita.png",
            4,
        ),
        (
            "Pizza 4 Quesos",
            "Pizza con mezcla de cuatro quesos italianos.",
            9.50,
            "4quesos.png",
            4,
        ),
        # Arroces
        (
            "Paella de Marisco",
            "Paella de mariscos recién preparada.",
            13.99,
            "paella_marisco.png",
            5,
        ),
        (
            "Risotto de Setas",
            "Risotto cremoso con setas variadas.",
            11.50,
            "risotto.png",
            5,
        ),
        # Asados
        (
            "Pollo Asado",
            "Pollo asado al horno con especias.",
            12.00,
            "pollo_asado.png",
            6,
        ),
        (
            "Costillas BBQ",
            "Costillas al horno con salsa barbacoa.",
            14.00,
            "costillas.png",
            6,
        ),
        # Ensaladas
        (
            "Ensalada César",
            "Ensalada con pollo, crutones y aderezo César.",
            7.50,
            "ensalada_cesar.png",
            7,
        ),
        (
            "Ensalada Mediterránea",
            "Ensalada fresca con aceitunas, queso feta y tomate.",
            6.99,
            "ensalada_med.png",
            7,
        ),
        # Cervezas
        (
            "Cerveza Lager",
            "Botella de cerveza lager 330ml.",
            2.50,
            "cerveza_lager.png",
            8,
        ),
        (
            "Cerveza IPA",
            "Botella de cerveza IPA artesanal 330ml.",
            3.00,
            "cerveza_ipa.png",
            8,
        ),
        # Vinos
        (
            "Vino Tinto",
            "Copa de vino tinto de la casa.",
            3.50,
            "vino_tinto.png",
            9,
        ),
        (
            "Vino Blanco",
            "Copa de vino blanco fresco.",
            3.50,
            "vino_blanco.png",
            9,
        ),
        # Refrescos con Gas y Sin Gas
        (
            "Coca-Cola",
            "Refresco de cola original 330ml.",
            1.80,
            "coca_cola.png",
            10,
        ),
        (
            "Limonada",
            "Refresco de limón natural sin gas.",
            1.50,
            "fanta_limon.png",
            10,
        ),
        # Aguas, zumos y batidos
        (
            "Agua Mineral",
            "Botella de agua mineral 500ml.",
            1.20,
            "aguapet.png",
            11,
        ),
        (
            "Agua Mineral",
            "Botella de agua mineral 1l.",
            1.20,
            "agualitro.png",
            11,
        ),
        (
            "Batido de Fresa",
            "Batido natural de fresa con leche.",
            2.50,
            "batido_fresa.png",
            11,
        ),
        # Postres
        (
            "Tarta de Manzana",
            "Tarta de manzana casera con canela.",
            4.50,
            "tarta_manzana.png",
            12,
        ),
        ("Flan Casero", "Flan de huevo hecho en casa.", 3.50, "flan.png", 12),
        # Cafés
        (
            "Café Solo",
            "Café espresso recién hecho.",
            1.50,
            "cafe_solo.png",
            13,
        ),
        (
            "Café con Leche",
            "Café con leche espumosa.",
            1.80,
            "cafe_leche.png",
            13,
        ),
    ]
    # print(f"Listado Productos: {datos_productos}")
    logger.info(f"Listado roles: {datos_productos}")

    for (
        nombre_producto,
        descripcion,
        precio,
        imagen,
        id_categoria_FK,
    ) in datos_productos:
        cursor.execute(
            "SELECT 1 FROM Productos WHERE nombre_producto = %s",
            (nombre_producto,),
        )
        if not cursor.fetchone():
            cursor.execute(
                """INSERT INTO Productos (nombre_producto, descripcion, precio, imagen, id_categoria_FK) 
                        VALUES (%s, %s, %s, %s, %s);""",
                (nombre_producto, descripcion, precio, imagen, id_categoria_FK),
            )
            # print(f"✔️ Producto '{nombre_producto}' insertado.")
            logger.info(f"✔️ Producto '{nombre_producto}' insertado.")
        else:
            # print(f"⚠️ Producto '{nombre_producto}' ya existe, no se insertó.")
            logger.info(f"⚠️ Producto '{nombre_producto}' ya existe, no se insertó.")

def insertar_carrito(cursor):
    # Insertar datos de ejemplo en la tabla Carrito
    datos_carrito = [
        (1, 101, 2, 10.50),  # id_cliente_FK, id_producto_FK, cantidad, precio_unitario
        (2, 102, 1, 20.00),
        (1, 103, 3, 15.75),
        (3, 101, 1, 10.50),
    ]
    print(f"Listado Carritos: {datos_carrito}")
    logger.info(f"Listado Carritos: {datos_carrito}")

    for id_cliente_FK, id_producto_FK, cantidad, precio_unitario in datos_carrito:
        cursor.execute(
            "SELECT 1 FROM Carrito WHERE id_cliente_FK = %s AND id_producto_FK = %s",
            (id_cliente_FK, id_producto_FK)
        )
        if not cursor.fetchone():
            cursor.execute(
                """INSERT INTO Carrito (id_cliente_FK, id_producto_FK, cantidad, precio_unitario) 
                VALUES (%s, %s, %s, %s);""",
                (id_cliente_FK, id_producto_FK, cantidad, precio_unitario),
            )
            logger.info(f"✔️ Carrito para el cliente {id_cliente_FK} y producto {id_producto_FK} insertado.")
        else:
            logger.info(f"⚠️ Carrito para el cliente {id_cliente_FK} y producto {id_producto_FK} ya existe, no se insertó.")

def insertar_pedidos(cursor):
    # Insertar datos de ejemplo en la tabla Pedidos
    datos_pedidos = [
        (1001, 1, 2, 31.00),  # num_pedido, id_cliente_FK, cantidad, precio_carrito
        (1002, 2, 1, 20.00),
        (1003, 1, 3, 47.25),
        (1004, 3, 1, 10.50),
    ]
    print(f"Listado Pedidos: {datos_pedidos}")
    logger.info(f"Listado Pedidos: {datos_pedidos}")

    for num_pedido, id_cliente_FK, cantidad, precio_carrito in datos_pedidos:
        cursor.execute(
            "SELECT 1 FROM Pedidos WHERE num_pedido = %s",
            (num_pedido,)
        )
        if not cursor.fetchone():
            cursor.execute(
                """INSERT INTO Pedidos (num_pedido, id_cliente_FK, cantidad, precio_carrito) 
                VALUES (%s, %s, %s, %s);""",
                (num_pedido, id_cliente_FK, cantidad, precio_carrito),
            )
            logger.info(f"✔️ Pedido {num_pedido} insertado para el cliente {id_cliente_FK}.")
        else:
            logger.info(f"⚠️ Pedido {num_pedido} ya existe, no se insertó.")

def insertar_pedidos_productos(cursor):
    # Insertar datos de ejemplo en la tabla Pedidos_Productos
    datos_pedidos_productos = [
        (1001, 101, 2, 10.50),  # id_pedido_FK, id_producto_FK, cantidad, precio_unitario
        (1002, 102, 1, 20.00),
        (1003, 103, 3, 15.75),
        (1004, 101, 1, 10.50),
    ]
    print(f"Listado Pedidos_Productos: {datos_pedidos_productos}")
    logger.info(f"Listado Pedidos_Productos: {datos_pedidos_productos}")

    for id_pedido_FK, id_producto_FK, cantidad, precio_unitario in datos_pedidos_productos:
        cursor.execute(
            "SELECT 1 FROM Pedidos_Productos WHERE id_pedido_FK = %s AND id_producto_FK = %s",
            (id_pedido_FK, id_producto_FK)
        )
        if not cursor.fetchone():
            cursor.execute(
                """INSERT INTO Pedidos_Productos (id_pedido_FK, id_producto_FK, cantidad, precio_unitario) 
                VALUES (%s, %s, %s, %s);""",
                (id_pedido_FK, id_producto_FK, cantidad, precio_unitario),
            )
            logger.info(f"✔️ Producto {id_producto_FK} insertado en el pedido {id_pedido_FK}.")
        else:
            logger.info(f"⚠️ Producto {id_producto_FK} ya existe en el pedido {id_pedido_FK}, no se insertó.")
