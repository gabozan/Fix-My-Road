import cv2
import numpy as np

########################################################################################################################

def load_image(path):
    """
    Carga una imagen desde el disco y la convierte de BGR a RGB.

    Parámetros:
        path (str): Ruta del archivo de imagen.

    Retorna:
        img (np.ndarray): Imagen en formato RGB.
    """
    img = cv2.imread(str(path))
    if img is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen en la ruta: {path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def save_image(path, img):
    """
    Guarda una imagen en disco convirtiéndola de RGB a BGR para compatibilidad con OpenCV.

    Parámetros:
        path (str): Ruta donde se guardará la imagen (incluye el nombre del archivo).
        img (np.ndarray): Imagen en formato RGB que se quiere guardar.

    Retorna:
        None
    """
    cv2.imwrite(str(path), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

