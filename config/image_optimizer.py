from PIL import Image
import os

def optimize_image(image_path, output_path, max_width=800, quality=85):
    """
    Optimiza una imagen reduciendo su tamaño y calidad.

    Args:
        image_path (str): Ruta de la imagen original.
        output_path (str): Ruta donde se guardará la imagen optimizada.
        max_width (int, optional): Ancho máximo permitido para la imagen. Por defecto, 800 píxeles.
        quality (int, optional): Calidad de la imagen optimizada (1-100). Por defecto, 85.
    """
    try:
        # Abrir la imagen
        with Image.open(image_path) as img:
            # Redimensionar manteniendo la relación de aspecto si es necesario
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.ANTIALIAS)

            # Guardar la imagen optimizada
            img.save(output_path, optimize=True, quality=quality)
            print(f"Imagen optimizada guardada en: {output_path}")

    except Exception as e:
        print(f"Error al optimizar la imagen: {e}")
