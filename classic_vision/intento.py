import glob
import os

import cv2
import numpy as np

from skimage import io, segmentation, color

from sklearn.cluster import MeanShift, estimate_bandwidth


def preprocess_images(input_folder, output_folder, target_size=(512, 512)):
    os.makedirs(output_folder, exist_ok=True)
    image_paths = glob.glob(os.path.join(input_folder, '*'))

    for path in image_paths:
        filename = os.path.basename(path)
        output_path = os.path.join(output_folder, filename)

        # Si ya está procesada, saltarla
        if os.path.exists(output_path):
            continue

        img = cv2.imread(path)
        if img is None:
            print(f"Error al cargar la imagen: {path}")
            continue

        # Recorte para imágenes de norway
        if 'norway' in filename.lower():
            h, w = img.shape[:2]
            img = img[:, :w // 2]

        # Resize solo si es necesario
        h, w = img.shape[:2]
        if (w, h) != target_size:
            img = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)

        # Guardar imagen procesada
        cv2.imwrite(output_path, img)

def load_preprocessed_images(output_folder):
    image_paths = glob.glob(os.path.join(output_folder, '*'))
    images = []

    for path in image_paths:
        img = cv2.imread(path)
        if img is not None:
            images.append(img)

    return images

def clahe(imagen_color):
    """
    Normaliza la iluminación de una imagen a color aplicando CLAHE
    al canal de luminosidad (L) en el espacio de color Lab.

    Args:
        imagen_color (numpy.ndarray): La imagen de entrada a color (BGR).

    Returns:
        numpy.ndarray: La imagen con iluminación normalizada.
    """
    # 1. Convertir la imagen al espacio de color Lab
    lab = cv2.cvtColor(imagen_color, cv2.COLOR_BGR2Lab)

    # 2. Aplicar CLAHE al canal L (luminosidad)
    l_canal, a_canal, b_canal = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=0.25, tileGridSize=(8, 8))
    l_canal_clahe = clahe.apply(l_canal)

    # 3. Fusionar los canales
    lab_clahe = cv2.merge((l_canal_clahe, a_canal, b_canal))

    # 4. Convertir de vuelta a BGR
    imagen_normalizada = cv2.cvtColor(lab_clahe, cv2.COLOR_Lab2BGR)

    return imagen_normalizada

def seg_mean_shift(img, kernel_size=1.25, max_dist=2, ratio=0.15):
    segments = segmentation.quickshift(img, kernel_size=kernel_size, max_dist=max_dist, ratio=ratio)
    segmented_image = color.label2rgb(segments, img, kind='avg')
    return segmented_image

def corregir_sombras(imagen_bgr, brillo_aumento=20, sombra_umbral=100):
    """
    Corrige sombras realzando las zonas oscuras sin saturar colores.

    Parámetros:
    - imagen_bgr: imagen original en formato BGR (cv2.imread()).
    - brillo_aumento: cuánto aumentar la luminosidad en zonas de sombra.
    - sombra_umbral: umbral para considerar que un píxel está en sombra.

    Retorna:
    - imagen_corregida: imagen BGR corregida.
    """

    # Convertir imagen a espacio LAB (luminosidad separada del color)
    lab = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # Crear una máscara donde los píxeles están debajo del umbral (es decir, en sombra)
    sombra_mask = l < sombra_umbral

    # Crear una copia de la L para modificar
    l_corregido = l.copy()

    # Aumentar el brillo sólo en las zonas de sombra
    l_corregido[sombra_mask] = np.clip(l[sombra_mask] + brillo_aumento, 0, 255)

    # Recomponer la imagen
    lab_corregido = cv2.merge((l_corregido, a, b))
    imagen_corregida = cv2.cvtColor(lab_corregido, cv2.COLOR_LAB2BGR)

    return imagen_corregida

def filtrar_colores_grisaceos_por_gama(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # -------------------------
    # Grises puros (negros a grises claros)
    # -------------------------
    lower_gray = np.array([0, 0, 20])
    upper_gray = np.array([180, 40, 200])

    # -------------------------
    # Marrón-grisáceo (previamente definido)
    # -------------------------
    lower_brown_gray = np.array([5, 20, 40])
    upper_brown_gray = np.array([25, 50, 150])

    # -------------------------
    # Rojo-grisáceo
    # (rojo puro es 0°/180°, limitamos saturación)
    lower_red_gray1 = np.array([0, 20, 40])
    upper_red_gray1 = np.array([10, 50, 160])
    lower_red_gray2 = np.array([170, 20, 40])
    upper_red_gray2 = np.array([180, 50, 160])

    # -------------------------
    # Verde-grisáceo (~60-90°)
    lower_green_gray = np.array([50, 20, 40])
    upper_green_gray = np.array([90, 50, 160])

    # -------------------------
    # Azul-grisáceo (~100-130°)
    lower_blue_gray = np.array([100, 20, 40])
    upper_blue_gray = np.array([130, 50, 160])

    # -------------------------
    # Cian-grisáceo (~80-100°)
    lower_cyan_gray = np.array([80, 20, 40])
    upper_cyan_gray = np.array([100, 50, 160])

    # -------------------------
    # Magenta-grisáceo (~140-160°)
    lower_magenta_gray = np.array([140, 20, 40])
    upper_magenta_gray = np.array([160, 50, 160])

    # -------------------------
    # Amarillo-grisáceo (~25-45°)
    lower_yellow_gray = np.array([25, 20, 40])
    upper_yellow_gray = np.array([45, 50, 160])

    # Crear máscaras por cada gama
    masks = [
        cv2.inRange(hsv, lower_gray, upper_gray),
        cv2.inRange(hsv, lower_brown_gray, upper_brown_gray),
        cv2.inRange(hsv, lower_red_gray1, upper_red_gray1),
        cv2.inRange(hsv, lower_red_gray2, upper_red_gray2),
        cv2.inRange(hsv, lower_green_gray, upper_green_gray),
        cv2.inRange(hsv, lower_blue_gray, upper_blue_gray),
        cv2.inRange(hsv, lower_cyan_gray, upper_cyan_gray),
        cv2.inRange(hsv, lower_magenta_gray, upper_magenta_gray),
        cv2.inRange(hsv, lower_yellow_gray, upper_yellow_gray)
    ]

    # Combinar todas las máscaras
    combined_mask = masks[0]
    for m in masks[1:]:
        combined_mask = cv2.bitwise_or(combined_mask, m)

    # Aplicar máscara sobre imagen original
    result = cv2.bitwise_and(image, image, mask=combined_mask)

    # Poner blanco donde no cumpla
    result[combined_mask == 0] = [255, 255, 255]

    return result

def filtrar_ruido(imagen):
    # Convertir la imagen a escala de grises
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Definir el rango de grises (de gris claro a negro)
    umbral_bajo = 50  # Ajusta este valor según lo que consideres gris claro
    umbral_alto = 150  # Ajusta este valor según el gris más oscuro que aceptes

    # Crear una máscara para las áreas grisáceas (desde gris claro hasta negro)
    mascara = cv2.inRange(imagen_gris, umbral_bajo, umbral_alto)

    # Aplicar una operación morfológica de apertura para eliminar ruido
    # La apertura ayuda a eliminar pequeños puntos de ruido
    kernel = np.ones((5, 5), np.uint8)  # Kernel de 5x5, puedes ajustarlo
    mascara_sin_ruido = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)

    # Mantener los píxeles negros intactos y filtrar los grises
    imagen_filtrada = imagen.copy()
    imagen_filtrada[mascara_sin_ruido == 0] = 0  # Poner a negro los píxeles no deseados

    return imagen_filtrada


def detect_road(img):
    img = seg_mean_shift(img)
    img = clahe(img)
    img = corregir_sombras(img)
    img = cv2.pyrMeanShiftFiltering(img, 25, 15)

    #img = filtrar_colores_grisaceos_por_gama(img)
    #img = filtrar_ruido(img)
    return img

# --- Ejemplo de uso ---
if __name__ == "__main__":
    input_folder_train = '../data/train/img'        # Cambia esto
    output_folder_train = 'imagenes_procesadas_train'              # Carpeta de salida
    input_folder_test = '../data/test/img'  # Cambia esto
    output_folder_test = 'imagenes_procesadas_test'

    # Procesar y guardar si no existen
    #preprocess_images(input_folder_train, output_folder_train)
    #preprocess_images(input_folder_test, output_folder_test)

    # Cargar todas las imágenes procesadas
    imagenes = load_preprocessed_images(output_folder_train)

    resultado = detect_road(imagenes[785])


    # Mostrar la imagen original
    cv2.imshow("Imagen Original", imagenes[785])
    # Mostrar la imagen filtrada (resultado)
    cv2.imshow("Imagen Filtrada", resultado)

    cv2.waitKey(0)
    cv2.destroyAllWindows()