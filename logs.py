import logging

def setup_logger():
    logging.basicConfig(
        level=logging.DEBUG,  # Nivel de log
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Mostrar logs en consola
            logging.FileHandler("web_cocina.log", mode='a', encoding='utf-8')  # Guardar logs en archivo
        ]
    )
    return logging.getLogger(__name__)

# Configura el logger al cargar el módulo
logger = setup_logger()
