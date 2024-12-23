# config.py

class Config:
    """Clase de configuración para la aplicación."""
    
    # Configuración de la base de datos MySQL
    MYSQL_CONFIG = {
        "host": "localhost",
        "user": "angelpaco",
        "password": "angelpaco",
        "database": "cocina_db",
    }
    
    # Otras configuraciones que se puedan necesitar
    SECRET_KEY = 'tu_clave_secreta'
    DEBUG = True
