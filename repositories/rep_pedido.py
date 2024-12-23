from copy import Error
from database.db_setup import get_db
from logs import logger


def validar_claves_foraneas(id_cliente_FK, id_producto_FK, id_carrito_FK):
    """
    Valida que las claves foráneas existan en las tablas correspondientes.

    :param conn: Conexión a la base de datos.
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    try:
        # Validar cliente
        cursor.execute("SELECT 1 FROM Clientes WHERE id_cliente = %s", (id_cliente_FK,))
        if not cursor.fetchone():
            raise ValueError(f"Cliente con ID {id_cliente_FK} no encontrado.")

        # Validar producto
        cursor.execute("SELECT 1 FROM Productos WHERE id_producto = %s", (id_producto_FK,))
        if not cursor.fetchone():
            raise ValueError(f"Producto con ID {id_producto_FK} no encontrado.")

        # Validar carrito
        cursor.execute("SELECT 1 FROM Carrito WHERE id_carrito = %s", (id_carrito_FK,))
        if not cursor.fetchone():
            raise ValueError(f"Carrito con ID {id_carrito_FK} no encontrado.")

        print(validar_claves_foraneas(conn, id_cliente_FK, id_producto_FK, id_carrito_FK))
        logger.info(validar_claves_foraneas(conn, id_cliente_FK, id_producto_FK, id_carrito_FK))        

    except Error as e:
        logger.error(f"Error al validar claves foráneas: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error

def obtener_pedidos():
    """
    Obtiene todos los pedidos con información cruzada de cliente, carrito y cantidad de productos.

    :param conn: Conexión a la base de datos.
    :return: Lista de diccionarios con los datos de los pedidos.
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT 
                c.nombre_cliente, 
                c.dni_cliente, 
                pe.cantidad, 
                ca.precio_total AS precio_carrito
            FROM Pedidos pe
            INNER JOIN Clientes c ON pe.id_cliente_FK = c.id_cliente
            INNER JOIN Carrito ca ON pe.id_carrito_FK = ca.id_carrito
        """
        cursor.execute(query)
        pedidos = cursor.fetchall()

        # Retornar los resultados tal cual vienen como diccionarios
        return pedidos

    except Error as e:
        logger.error(f"Error obtener pedidos: {e}")
        return []  # Devolvemos una lista vacía en caso de error

    finally:
        cursor.close()


def obtener_pedido_id(id_pedido):
    """
    Obtiene los detalles de un pedido específico, incluyendo información
    cruzada con Clientes, Productos y Carrito.

    :param conn: Conexión a la base de datos.
    :param id_pedido: ID del pedido a buscar.
    :return: Un diccionario con los datos del pedido o None si no existe.
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT 
                p.id_pedido,
                p.num_pedido,
                c.nombre_cliente,
                c.dni_cliente,
                pr.nombre_producto,
                pr.precio,
                ca.precio_total AS precio_carrito,
                p.cantidad,
                p.fecha_pedido
            FROM Pedidos p
            INNER JOIN Clientes c ON p.id_cliente_FK = c.id_cliente
            INNER JOIN Productos pr ON p.id_producto_FK = pr.id_producto
            INNER JOIN Carrito ca ON p.id_carrito_FK = ca.id_carrito
            WHERE p.id_pedido = %s
        """
        cursor.execute(query, (id_pedido,))
        pedido = cursor.fetchone()

        # Retornar los datos del pedido como un diccionario
        return {
            "id_pedido": pedido["id_pedido"],
            "num_pedido": pedido["num_pedido"],
            "nombre_cliente": pedido["nombre_cliente"],
            "dni_cliente": pedido["dni_cliente"],
            "nombre_producto": pedido["nombre_producto"],
            "precio_producto": pedido["precio_producto"],
            "precio_carrito": pedido["precio_carrito"],
            "cantidad": pedido["cantidad"],
            "fecha_pedido": pedido["fecha_pedido"],
        }
    except Error as e:
        logger.error(f"Error obtener pedido por ID: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error

def obtener_pedido_con_productos():
    """
    Obtiene todos los pedidos con sus productos asociados.
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        # Consulta para obtener los pedidos con sus productos
        query = """
            SELECT p.id_pedido, p.num_pedido, p.id_cliente_FK, p.fecha_pedido,
                   pr.nombre_producto AS producto_nombre, pp.cantidad, p.precio_carrito
            FROM Pedidos p
            LEFT JOIN Pedido_Productos pp ON p.id_pedido = pp.id_pedido_FK
            LEFT JOIN Productos pr ON pp.id_producto_FK = pr.id_producto
            ORDER BY p.id_pedido;
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        # Organizar los pedidos en una estructura jerárquica
        pedidos = {}
        for row in resultados:
            id_pedido = row["id_pedido"]
            if id_pedido not in pedidos:
                pedidos[id_pedido] = {
                    "num_pedido": row["num_pedido"],
                    "id_cliente": row["id_cliente_FK"],
                    "fecha_pedido": row["fecha_pedido"],
                    "productos": [],
                }
            if row["producto_nombre"]:
                pedidos[id_pedido]["productos"].append({
                    "nombre": row["producto_nombre"],
                    "cantidad": row["cantidad"],
                    "precio_carrito": row["precio_carrito"],
                })
        
        return list(pedidos.values())

    except Error as e:
        logger.error(f"Error al obtener todos los pedidos: {e}")
        return []
    finally:
        cursor.close()


def crear_pedido_con_productos(num_pedido, id_cliente_FK, id_carrito_FK, productos, fecha_pedido):
    """
    Crea un pedido con varios productos.
    - productos: Lista de diccionarios con id_producto y cantidad.

    :param conn: Conexión a la base de datos.
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        # Insertar en la tabla Pedidos
        cursor.execute(
            """
            INSERT INTO Pedidos (num_pedido, id_cliente_FK, id_carrito_FK, fecha_pedido) 
            VALUES (%s, %s, %s, %s)
            """,
            (num_pedido, id_cliente_FK, id_carrito_FK, fecha_pedido),
        )
        id_pedido = cursor.lastrowid  # Obtener el ID del pedido recién creado

        # Insertar los productos relacionados en la tabla Pedido_Productos
        for producto in productos:
            id_producto_FK = producto["id_producto"]
            cantidad = producto["cantidad"]
            precio_carrito = producto["precio_carrito"]
            cursor.execute(
                """
                INSERT INTO Pedido_Productos (id_pedido_FK, id_producto_FK, cantidad, precio_carrito) 
                VALUES (%s, %s, %s, %s)
                """,
                (id_pedido, id_producto_FK, cantidad, precio_carrito),
            )

        conn.commit()
        return id_pedido
    except Error as e:
        logger.error(f"Error al CREAR PEDIDO: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error



# Generar número de pedido aleatorio


def generar_numero_pedido():

    import random

    return f"PED-{random.randint(1000, 9999)}"  # Número de pedido aleatorio

# Modificar pedido


def actualizar_pedido(id_pedido, num_pedido, id_cliente_FK, id_producto_FK, id_carrito_FK, cantidad, fecha_pedido):
    """
    Actualiza un pedido en la tabla Pedidos.
    :param id_pedido: ID del pedido a buscar.
    :param conn: Conexión a la base de datos.
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        # Obtener el valor actual de la cantidad para verificar si ha cambiado
        cursor.execute("SELECT cantidad FROM Pedidos WHERE id_pedido = %s", (id_pedido,))
        resultado = cursor.fetchone()

        if resultado:
            cantidad_actual = resultado[0]

            if cantidad != cantidad_actual:
                # Crear un nuevo número de pedido si la cantidad ha cambiado
                num_pedido = (
                    generar_numero_pedido()
                )  # Función que genera un nuevo num_pedido

            # Actualizar el pedido
            cursor.execute(
                """
                UPDATE Pedidos 
                SET num_pedido = %s, id_cliente_FK = %s, id_producto_FK = %s, id_carrito_FK = %s, 
                    cantidad = %s, entrega = %s
                WHERE id_pedido = %s
                """,
                (
                    num_pedido,
                    id_cliente_FK,
                    id_producto_FK,
                    id_carrito_FK,
                    cantidad,
                    fecha_pedido,
                    id_pedido,
                ),
            )
            conn.commit()
            return resultado
        else:
            print("❌ Pedido no encontrado con id_pedido:", id_pedido)
    except Error as e:
        logger.error(f"Error al ACTUALIZAR PEDIDO: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error

# Borrar pedido
def borrar_pedido(id_pedido):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM Pedidos WHERE id_pedido = %s",
            (id_pedido),
        )
        conn.commit()
    except Error as e:
        logger.error(f"Error al BORRAR PEDIDO: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error        
