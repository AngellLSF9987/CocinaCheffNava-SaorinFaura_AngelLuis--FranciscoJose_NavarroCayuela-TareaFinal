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
        cursor.execute(
            "SELECT 1 FROM Productos WHERE id_producto = %s", (id_producto_FK,)
        )
        if not cursor.fetchone():
            raise ValueError(f"Producto con ID {id_producto_FK} no encontrado.")

        # Validar carrito
        cursor.execute("SELECT 1 FROM Carrito WHERE id_carrito = %s", (id_carrito_FK,))
        if not cursor.fetchone():
            raise ValueError(f"Carrito con ID {id_carrito_FK} no encontrado.")

        # Si todo está bien, se pueden devolver los resultados
        return True
    except Error as e:
        logger.error(f"Error al validar claves foráneas: {e}")
        return False  # Devolvemos False si hay un error
    finally:
        cursor.close()


def obtener_pedidos():
    """
    Obtiene todos los pedidos con información cruzada de cliente, carrito y cantidad de productos.

    :return: Lista de diccionarios con los datos de los pedidos.
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
                SELECT 
                    c.nombre_cliente,
                    c.dni_cliente,
                    pp.cantidad,
                    pp.cantidad * pp.precio_unitario AS precio_total
                FROM Pedidos p
                INNER JOIN Clientes c ON p.id_cliente_FK = c.id_cliente
                INNER JOIN Pedidos_Productos pp ON p.id_pedido = pp.id_pedido_FK
                INNER JOIN Productos pr ON pp.id_producto_FK = pr.id_producto;
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

    :param id_pedido: ID del pedido a buscar.
    :return: Un diccionario con los datos del pedido o None si no existe.
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
                SELECT 
                    p.id_pedido, p.num_pedido, p.id_cliente_FK, p.fecha_pedido,
                    c.nombre_cliente, c.apellido1, c.apellido2, c.dni_cliente,
                    c.telefono, c.direccion, c.email,
                    pr.nombre_producto, pr.imagen, pr.precio AS precio_unitario,
                    pp.cantidad, pp.precio_unitario * pp.cantidad AS precio_total
                FROM Pedidos p
                INNER JOIN Clientes c ON p.id_cliente_FK = c.id_cliente
                INNER JOIN Pedidos_Productos pp ON p.id_pedido = pp.id_pedido_FK
                INNER JOIN Productos pr ON pp.id_producto_FK = pr.id_producto
                WHERE p.id_pedido = %s;
        """
        cursor.execute(query, (id_pedido,))
        resultados = cursor.fetchall()

        if not resultados:
            return None

        # Organizar los resultados en una estructura jerárquica
        pedido = {
            "id_pedido": resultados[0]["id_pedido"],
            "num_pedido": resultados[0]["num_pedido"],
            "fecha_pedido": resultados[0]["fecha_pedido"],
            "cliente": {
                "id_cliente": resultados[0]["id_cliente_FK"],
                "nombre": resultados[0]["nombre_cliente"],
                "apellido1": resultados[0]["apellido1"],
                "apellido2": resultados[0]["apellido2"],
                "dni": resultados[0]["dni_cliente"],
                "telefono": resultados[0]["telefono"],
                "direccion": resultados[0]["direccion"],
                "email": resultados[0]["email"],
            },
            "productos": [],
        }

        for row in resultados:
            if row["nombre_producto"]:
                pedido["productos"].append(
                    {
                        "nombre_producto": row["nombre_producto"],
                        "imagen": row["imagen"],
                        "precio_unitario": row["precio_unitario"],
                        "cantidad": row["cantidad"],
                        "precio_total": row["precio_total"],
                    }
                )

        return pedido

    except Error as e:
        logger.error(f"Error obtener pedido por ID: {e}")
        return None  # Devolvemos None en caso de error
    finally:
        cursor.close()


def obtener_pedido_con_productos():
    """
    Obtiene todos los pedidos con sus productos asociados y la información del cliente.
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT 
                p.id_pedido, p.num_pedido, p.id_cliente_FK, p.fecha_pedido,
                ca.id_carrito, pr.nombre_producto, pr.imagen, pp.cantidad, pp.precio_carrito,
                c.nombre_cliente, c.apellido1, c.apellido2, c.dni_cliente, c.telefono, 
                c.direccion, c.email
            FROM Pedidos p
            LEFT JOIN Carrito ca ON p.id_carrito_FK = ca.id_carrito
            LEFT JOIN Productos pr ON pr.id_producto = ca.id_producto_FK
            LEFT JOIN Pedido_Productos pp ON p.id_pedido = pp.id_pedido_FK
            LEFT JOIN Clientes c ON p.id_cliente_FK = c.id_cliente
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
                    "cliente": {
                        "nombre": row["nombre_cliente"],
                        "apellido1": row["apellido1"],
                        "apellido2": row["apellido2"],
                        "dni": row["dni_cliente"],
                        "telefono": row["telefono"],
                        "direccion": row["direccion"],
                        "email": row["email"],
                    },
                    "productos": [],
                }
            if row["nombre_producto"]:
                pedidos[id_pedido]["productos"].append(
                    {
                        "nombre": row["nombre_producto"],
                        "imagen": row["imagen"],
                        "cantidad": row["cantidad"],
                        "precio_carrito": row["precio_carrito"],
                    }
                )

        return list(pedidos.values())

    except Error as e:
        logger.error(f"Error al obtener todos los pedidos: {e}")
        return []
    finally:
        cursor.close()


def crear_pedido_con_productos(num_pedido, id_cliente_FK, productos, fecha_pedido):
    conn = get_db()
    cursor = conn.cursor()
    try:
        # Insertar en la tabla Pedidos
        cursor.execute(
            """
            INSERT INTO Pedidos (num_pedido, id_cliente_FK, fecha_pedido) 
            VALUES (%s, %s, %s)
            """,
            (num_pedido, id_cliente_FK, fecha_pedido),
        )
        id_pedido = cursor.lastrowid

        # Insertar los productos en la tabla Pedidos_Productos
        for producto in productos:
            cursor.execute(
                """
                INSERT INTO Pedidos_Productos (id_pedido_FK, id_producto_FK, cantidad, precio_unitario) 
                VALUES (%s, %s, %s, %s)
                """,
                (
                    id_pedido,
                    producto["id_producto"],
                    producto["cantidad"],
                    producto["precio_unitario"],
                ),
            )
        conn.commit()
        return id_pedido
    except Error as e:
        logger.error(f"Error al crear pedido: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()


def actualizar_pedido(id_pedido, num_pedido, id_cliente_FK, id_producto_FK, id_carrito_FK, cantidad, fecha_pedido):
    """
    Actualiza un pedido en la tabla Pedidos y devuelve los detalles completos del pedido actualizado,
    incluyendo la información del cliente y los productos.

    :param id_pedido: ID del pedido a buscar.
    :param conn: Conexión a la base de datos.
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        # Obtener el valor actual de la cantidad para verificar si ha cambiado
        cursor.execute(
            "SELECT cantidad FROM Pedidos WHERE id_pedido = %s", (id_pedido,)
        )
        resultado = cursor.fetchone()

        if resultado:
            cantidad_actual = resultado[0]

            if cantidad != cantidad_actual:
                # Crear un nuevo número de pedido si la cantidad ha cambiado
                num_pedido = generar_numero_pedido()  # Función que genera un nuevo num_pedido

            # Actualizar el pedido
            cursor.execute(
                """
                UPDATE Pedidos 
                SET num_pedido = %s, id_cliente_FK = %s, id_producto_FK = %s, id_carrito_FK = %s, 
                    cantidad = %s, fecha_pedido = %s
                WHERE id_pedido = %s
                """,
                (
                    num_pedido, id_cliente_FK, id_producto_FK, id_carrito_FK, cantidad, fecha_pedido, id_pedido,
                ),
            )
            conn.commit()

            # Obtener los detalles del pedido actualizado con los datos del cliente y productos
            query = """
                SELECT 
                    p.id_pedido, p.num_pedido, p.fecha_pedido,
                    c.nombre_cliente, c.apellido1, c.apellido2, c.dni_cliente,
                    c.telefono, c.direccion, c.email,
                    pr.nombre_producto, pr.precio AS precio_unitario,
                    pp.cantidad, pp.precio_unitario * pp.cantidad AS precio_total
                FROM Pedidos p
                INNER JOIN Clientes c ON p.id_cliente_FK = c.id_cliente
                INNER JOIN Pedidos_Productos pp ON p.id_pedido = pp.id_pedido_FK
                INNER JOIN Productos pr ON pp.id_producto_FK = pr.id_producto
                WHERE p.id_pedido = %s;
            """
            cursor.execute(query, (id_pedido,))
            resultados = cursor.fetchall()

            if not resultados:
                return None  # No se encuentra el pedido

            # Organizar los resultados en una estructura jerárquica
            pedido_actualizado = {
                "id_pedido": resultados[0]["id_pedido"],
                "num_pedido": resultados[0]["num_pedido"],
                "fecha_pedido": resultados[0]["fecha_pedido"],
                "cliente": {
                    "id_cliente": resultados[0]["id_cliente_FK"],
                    "nombre": resultados[0]["nombre_cliente"],
                    "apellido1": resultados[0]["apellido1"],
                    "apellido2": resultados[0]["apellido2"],
                    "dni": resultados[0]["dni_cliente"],
                    "telefono": resultados[0]["telefono"],
                    "direccion": resultados[0]["direccion"],
                    "email": resultados[0]["email"]
                },
                "productos": []
            }

            for row in resultados:
                if row["nombre_producto"]:
                    pedido_actualizado["productos"].append({
                        "nombre_producto": row["nombre_producto"],
                        "precio_unitario": row["precio_unitario"],
                        "cantidad": row["cantidad"],
                        "precio_total": row["precio_total"]
                    })

            return pedido_actualizado

        else:
            print("❌ Pedido no encontrado con id_pedido:", id_pedido)
            return None
    except Error as e:
        logger.error(f"Error al ACTUALIZAR PEDIDO: {e}")
        return None  # Devolvemos None en caso de error
    finally:
        cursor.close()

def borrar_pedido(id_pedido):
    conn = get_db()
    cursor = conn.cursor()
    try:
        # Verificar si el pedido existe antes de borrarlo
        cursor.execute("SELECT 1 FROM Pedidos WHERE id_pedido = %s", (id_pedido,))
        if cursor.fetchone() is None:
            logger.error(f"Pedido con id_pedido {id_pedido} no encontrado.")
            return None  # Si no existe, no hace nada y devuelve None

        # Si el pedido existe, lo eliminamos
        cursor.execute(
            "DELETE FROM Pedidos WHERE id_pedido = %s",
            (id_pedido,),
        )
        conn.commit()
        return {"status": "success", "message": f"Pedido {id_pedido} borrado correctamente."}
    except Error as e:
        logger.error(f"Error al BORRAR PEDIDO: {e}")
        return {"status": "error", "message": str(e)}  # Devolver un error detallado
    finally:
        cursor.close()


# Generar número de pedido aleatorio
def generar_numero_pedido():
    import random

    return f"PED-{random.randint(1000, 9999)}"  # Número de pedido aleatorio
