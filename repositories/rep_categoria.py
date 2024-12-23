from copy import Error
from database.db_setup import get_db
from logs import logger


# Obtener todos los categorias
def obtener_categorias():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Categorias")
        categorias = cursor.fetchall()
        return [
            {
                "id_categoria": categoria["id_categoria"],
                "nombre_categoria": categoria["nombre_categoria"],
                "descripcion": categoria["descripcion"],
                "imagen": categoria["imagen"],
            }
            for categoria in categorias
        ]
    except Error as e:
        logger.error(f"Error al obtener categorias: {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error

# Obtener categoría por ID
def obtener_categoria_id(id_categoria):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            SELECT id_categoria, nombre_categoria, descripcion, imagen 
            FROM Categorias 
            WHERE id_categoria = %s
            """,
            (id_categoria,),
        )
        categoria = cursor.fetchone()
        if not categoria:
            logger.warning(f"No se encontró categoría con ID {id_categoria}")
            return None
        else:
            logger.info(f"Categoría obtenida: {categoria}")
            return categoria
    except Error as e:
        logger.error(f"Error al obtener categoría por ID {id_categoria}: {e}")
        return None  # Devolver None en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error


# Crear categoria
def crear_categoria(nombre_categoria, descripcion, imagen):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Categorias (nombre_categoria, descripcion, imagen) 
            VALUES (%s, %s, %s)
        """,
            (nombre_categoria, descripcion, imagen),
        )  # Se pasa id_categoria_FK aquí
        conn.commit()
    except Error as e:
        logger.error(f"Error al CREAR categoría {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error


# Modificar categoria
def actualizar_categoria(nombre_categoria, descripcion, imagen, id_categoria):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            UPDATE Categorias 
            SET nombre_categoria =  %s, descripcion =  %s, imagen =  %s 
            WHERE id_categoria =  %s""",
            (nombre_categoria, descripcion, imagen, id_categoria),
        )
        conn.commit()
        categoria_actualizadda = cursor.fetchone()
        return categoria_actualizadda
    except Error as e:
        logger.error(f"Error al ACTUALIZAR categoría {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error


# Borrar categoria
def borrar_categoria(id_categoria):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE 1 FROM Categorias WHERE id_categoria= %s", (id_categoria,)
        )
        conn.commit()
    except Error as e:
        logger.error(f"Error al BORRAR categoría {e}")
        return []  # Devolvemos una lista vacía en caso de error
    finally:
        cursor.close()  # Cerramos el cursor siempre, incluso si ocurre un error
