import numpy as np
import math
import cv2
import matplotlib.pyplot as plt
import glob
import os

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def load_and_convert_images_numpy(image_paths):
    grayscale_images = []
    for path in image_paths:
        image = cv2.imread(path)
        if image is not None:
            gray = convert_to_grayscale_numpy(image)
            grayscale_images.append(gray)
    return grayscale_images

# Ejemplo de uso:
folder_path = 'ruta/a/tu/carpeta'
image_paths = load_dataset(folder_path)
gray_images = load_and_convert_images_numpy(image_paths)

# Mostrar la primera imagen
if gray_images:
    plt.imshow(gray_images[0], cmap='gray')
    plt.title("Imagen en escala de grises (NumPy)")
    plt.axis('off')
    plt.show()