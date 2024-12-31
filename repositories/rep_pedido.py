from copy import Error
from database.db_setup import get_db
import repositories.rep_pedidos_productos as pedido_productoDB
from logs import logger

def validar_claves_foraneas(id_cliente_FK, id_producto_FK):
    """
    Valida que las claves foráneas existan en las tablas correspondientes.
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

        return True
    except Error as e:
        logger.error(f"Error al validar claves foráneas: {e}")
        return False
    finally:
        cursor.close()

def obtener_pedidos():
    """
    Obtiene todos los pedidos con información cruzada de cliente y productos asociados.
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT 
                p.id_pedido, p.num_pedido, p.fecha_registro AS fecha_pedido,
                c.nombre_cliente, c.dni_cliente,
                SUM(pp.cantidad_por_producto) AS cantidad_total_productos,
                SUM(pp.precio_total) AS precio_total
            FROM Pedidos p
            INNER JOIN Clientes c ON p.id_cliente_FK = c.id_cliente
            INNER JOIN Pedidos_Productos pp ON p.id_pedido = pp.id_pedido_FK
            GROUP BY p.id_pedido;
        """
        cursor.execute(query)
        pedidos = cursor.fetchall()

        return pedidos
    except Error as e:
        logger.error(f"Error al obtener pedidos: {e}")
        return []
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
                p.id_pedido, p.num_pedido, p.fecha_registro AS fecha_pedido,
                c.nombre_cliente, c.apellido1, c.apellido2, c.dni_cliente,
                c.telefono, c.direccion, c.email,
                pr.nombre_producto, pr.precio_unidad, pr.imagen, 
                pp.cantidad_por_producto, pp.precio_total
            FROM Pedidos p
            INNER JOIN Clientes c ON p.id_cliente_FK = c.id_cliente
            INNER JOIN Pedidos_Productos pp ON p.id_pedido = pp.id_pedido_FK
            INNER JOIN Productos pr ON pp.id_producto_FK = pr.id_producto
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
                    "fecha_pedido": row["fecha_pedido"],
                    "cliente": {
                        "nombre_cliente": row["nombre_cliente"],
                        "apellido1": row["apellido1"],
                        "apellido2": row["apellido2"],
                        "dni_cliente": row["dni_cliente"],
                        "telefono": row["telefono"],
                        "direccion": row["direccion"],
                        "email": row["email"],
                    },
                    "productos": [],
                }
            if row["nombre_producto"]:
                pedidos[id_pedido]["productos"].append({
                    "nombre_producto": row["nombre_producto"],
                    "imagen": row["imagen"],
                    "cantidad_por_producto": row["cantidad_por_producto"],
                    "precio_total": row["precio_total"],
                })

        return list(pedidos.values())
    except Error as e:
        logger.error(f"Error al obtener todos los pedidos: {e}")
        return []
    finally:
        cursor.close()

def obtener_pedido_id(id_pedido):
    """
    Obtiene los detalles de un pedido específico, incluyendo información
    cruzada con Clientes y Productos.
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT 
                p.id_pedido, p.num_pedido, p.fecha_registro AS fecha_pedido,
                c.nombre_cliente, c.apellido1, c.apellido2, c.dni_cliente,
                c.telefono, c.direccion, c.email,
                pr.nombre_producto, pr.imagen, pr.precio_unidad,
                pp.cantidad_por_producto, pp.precio_total
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

        pedido = {
            "id_pedido": resultados[0]["id_pedido"],
            "num_pedido": resultados[0]["num_pedido"],
            "fecha_pedido": resultados[0]["fecha_pedido"],
            "cliente": {
                "nombre_cliente": resultados[0]["nombre_cliente"],
                "apellido1": resultados[0]["apellido1"],
                "apellido2": resultados[0]["apellido2"],
                "dni_cliente": resultados[0]["dni_cliente"],
                "telefono": resultados[0]["telefono"],
                "direccion": resultados[0]["direccion"],
                "email": resultados[0]["email"],
            },
            "productos": [],
        }

        for row in resultados:
            if row["nombre_producto"]:
                pedido["productos"].append({
                    "nombre_producto": row["nombre_producto"],
                    "imagen": row["imagen"],
                    "precio_unidad": row["precio_unidad"],
                    "cantidad_por_producto": row["cantidad_por_producto"],
                    "precio_total": row["precio_total"],
                })

        return pedido
    except Error as e:
        logger.error(f"Error al obtener pedido por ID: {e}")
        return None
    finally:
        cursor.close()


def obtener_pedidos_por_cliente(id_cliente):
    """
    Obtiene todos los pedidos de un cliente específico, incluyendo información
    cruzada con Productos.
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
            SELECT 
                p.id_pedido, p.num_pedido, p.fecha_registro AS fecha_pedido,
                c.nombre_cliente, c.apellido1, c.apellido2, c.dni_cliente,
                c.telefono, c.direccion, c.email,
                pr.nombre_producto, pr.imagen, pr.precio_unidad,
                pp.cantidad_por_producto, pp.precio_total
            FROM Pedidos p
            INNER JOIN Clientes c ON p.id_cliente_FK = c.id_cliente
            INNER JOIN Pedidos_Productos pp ON p.id_pedido = pp.id_pedido_FK
            INNER JOIN Productos pr ON pp.id_producto_FK = pr.id_producto
            WHERE c.id_cliente = %s;
        """
        cursor.execute(query, (id_cliente,))
        resultados = cursor.fetchall()

        if not resultados:
            return None

        pedidos = []
        pedido_actual = None

        # Agrupar los resultados por pedido
        for row in resultados:
            if not pedido_actual or pedido_actual["id_pedido"] != row["id_pedido"]:
                if pedido_actual:
                    pedidos.append(pedido_actual)
                pedido_actual = {
                    "id_pedido": row["id_pedido"],
                    "num_pedido": row["num_pedido"],
                    "fecha_pedido": row["fecha_pedido"],
                    "cliente": {
                        "nombre_cliente": row["nombre_cliente"],
                        "apellido1": row["apellido1"],
                        "apellido2": row["apellido2"],
                        "dni_cliente": row["dni_cliente"],
                        "telefono": row["telefono"],
                        "direccion": row["direccion"],
                        "email": row["email"],
                    },
                    "productos": [],
                }

            if row["nombre_producto"]:
                pedido_actual["productos"].append({
                    "nombre_producto": row["nombre_producto"],
                    "imagen": row["imagen"],
                    "precio_unidad": row["precio_unidad"],
                    "cantidad_por_producto": row["cantidad_por_producto"],
                    "precio_total": row["precio_total"],
                })

        if pedido_actual:
            pedidos.append(pedido_actual)

        return pedidos
    except Error as e:
        logger.error(f"Error al obtener los pedidos del cliente {id_cliente}: {e}")
        return None
    finally:
        cursor.close()


def crear_pedido_con_productos(num_pedido, id_cliente_FK, productos, fecha_pedido):
    conn = get_db()
    cursor = conn.cursor()
    try:
        # Insertar en la tabla Pedidos
        cursor.execute(
            """
            INSERT INTO Pedidos (num_pedido, id_cliente_FK, fecha_registro) 
            VALUES (%s, %s, %s)
            """,
            (num_pedido, id_cliente_FK, fecha_pedido),
        )
        id_pedido = cursor.lastrowid

        # Insertar los productos asociados usando la función específica
        for producto in productos:
            if not pedido_productoDB.agregar_producto_a_pedido(
                id_pedido,
                producto["id_producto"],
                producto["cantidad_por_producto"],
                producto["precio_unidad"]
            ):
                raise Error(f"Error al agregar el producto {producto['id_producto']} al pedido {id_pedido}.")

        conn.commit()
        return id_pedido
    except Error as e:
        logger.error(f"Error al crear pedido: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()


def actualizar_pedido(id_pedido, num_pedido, id_cliente_FK, productos, fecha_pedido):
    """
    Actualiza un pedido y sus productos asociados en la base de datos.
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        # Actualizar datos del pedido en la tabla Pedidos
        cursor.execute(
            """
            UPDATE Pedidos 
            SET num_pedido = %s, id_cliente_FK = %s, fecha_registro = %s
            WHERE id_pedido = %s
            """,
            (num_pedido, id_cliente_FK, fecha_pedido, id_pedido),
        )

        # Eliminar los productos asociados al pedido usando la función específica
        if not pedido_productoDB.eliminar_productos_por_pedido(id_pedido):
            raise Error("Error al eliminar productos del pedido.")

        # Agregar los productos actualizados usando la función específica
        for producto in productos:
            if not pedido_productoDB.agregar_producto_a_pedido(
                id_pedido, 
                producto["id_producto"], 
                producto["cantidad_por_producto"], 
                producto["precio_unidad"]
            ):
                raise Error(f"Error al agregar el producto {producto['id_producto']} al pedido {id_pedido}.")

        conn.commit()

        # Obtener los detalles actualizados del pedido
        return obtener_pedido_id(id_pedido)  # Reutiliza la función de consulta por ID
    except Error as e:
        logger.error(f"Error al actualizar pedido: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()


def borrar_pedido(id_pedido):
    """
    Elimina un pedido y sus productos asociados en la base de datos.
    """
    conn = get_db()
    cursor = conn.cursor()
    try:
        # Verificar si el pedido existe
        cursor.execute("SELECT 1 FROM Pedidos WHERE id_pedido = %s", (id_pedido,))
        if cursor.fetchone() is None:
            return {"status": "error", "message": f"Pedido {id_pedido} no encontrado."}

        # Eliminar los productos asociados en Pedidos_Productos
        cursor.execute("DELETE FROM Pedidos_Productos WHERE id_pedido_FK = %s", (id_pedido,))

        # Eliminar el pedido de la tabla Pedidos
        cursor.execute("DELETE FROM Pedidos WHERE id_pedido = %s", (id_pedido,))
        
        conn.commit()
        return {"status": "success", "message": f"Pedido {id_pedido} y productos asociados borrados correctamente."}
    except Error as e:
        logger.error(f"Error al borrar pedido: {e}")
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()

# Generar número de pedido aleatorio
def generar_numero_pedido():
    import random

    return f"PED-{random.randint(1000, 9999)}"  # Número de pedido aleatorio
