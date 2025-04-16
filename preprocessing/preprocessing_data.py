import numpy as np
import math
import cv2
import matplotlib.pyplot as plt
import glob
import os

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

# --- Ejemplo de uso ---
if __name__ == "__main__":
    input_folder_train = '../data/train/img'        # Cambia esto
    output_folder_train = 'imagenes_procesadas_train'              # Carpeta de salida
    input_folder_test = '../data/test/img'  # Cambia esto
    output_folder_test = 'imagenes_procesadas_test'

    # Procesar y guardar si no existen
    preprocess_images(input_folder_train, output_folder_train)
    preprocess_images(input_folder_test, output_folder_test)

    # Cargar todas las imágenes procesadas
    imagenes = load_preprocessed_images(output_folder_train)

    # Mostrar una por una
    for i, img in enumerate(imagenes):
        cv2.imshow(f"Imagen {i+1}", img)
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()
        if key == ord('q') or key == 27:
            break
