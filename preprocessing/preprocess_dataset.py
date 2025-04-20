from pathlib import Path
import cv2
import numpy as np
import glob
from utils import load_image, save_image
from preprocessing.letterbox import letterbox
from preprocessing.xml_utils import resize_xml_labels, xml_to_txt

########################################################################################################################

def preprocess_cv(input_path, output_path, new_size):
    """
    Preprocesa las imágenes y sus etiquetas para técnicas clásicas de visión por computador.

    Parámetros:
        input_path (Path): Ruta al directorio de entrada que contiene las carpetas "train" y "test".
        output_path (Path): Ruta al directorio de salida donde se guardarán las imágenes procesadas.
        new_size (tuple): Tamaño de redimensionado final (ancho, alto).
    """
    for split in ["train", "test"]:
        in_image_dir = input_path / split
        out_image_dir = output_path / split
        out_label_dir = output_path / "labels"
        out_image_dir.mkdir(parents=True, exist_ok=True)
        out_label_dir.mkdir(parents=True, exist_ok=True)

        for image_file in in_image_dir.glob("*.jpg"):
            file_name = image_file.stem
            try:
                img = load_image(image_file)
            except FileNotFoundError as e:
                print(e)
                continue
            original_size = (img.shape[1], img.shape[0])

            crop_box = None
            if "norway" in file_name.lower():
                crop_w = original_size[0] // 2
                crop_box = (0, 0, crop_w, original_size[1])
                img = img[:, :crop_w]
            img_resized = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
            save_image((out_image_dir / image_file.name), img_resized)
            
            in_label_path = input_path / "labels" / (file_name + ".xml")
            out_label_path = out_label_dir / (file_name + ".txt")

            if in_label_path.exists():
                tree = resize_xml_labels(in_label_path, new_size, original_size, crop_box, "classic_vision")
                xml_to_txt(tree, out_label_path, new_size, "classic_vision")


def preprocess_dl(input_path, output_path, new_size):
    """
        Preprocesa las imágenes y sus etiquetas para deep learning.

        Parámetros:
            input_path (Path): Ruta al directorio de entrada que contiene las carpetas "train" y "test".
            output_path (Path): Ruta al directorio de salida donde se guardarán las imágenes procesadas.
            new_size (tuple): Tamaño de redimensionado final (ancho, alto).
        """
    for split in ["train", "test"]:
        in_image_dir = input_path / split
        out_image_dir = output_path / split
        out_label_dir = output_path / "labels"
        out_image_dir.mkdir(parents=True, exist_ok=True)
        out_label_dir.mkdir(parents=True, exist_ok=True)

        for image_file in in_image_dir.glob("*.jpg"):
            file_name = image_file.stem
            try:
                img = load_image(image_file)
            except FileNotFoundError as e:
                print(e)
                continue
            original_size = (img.shape[1], img.shape[0])

            crop_box = None
            img_resized, scale, (pad_x, pad_y) = letterbox(img, original_size)
            save_image((out_image_dir / image_file.name), img_resized)
            
            in_label_path = input_path / "labels" / (file_name + ".xml")
            out_label_path = out_label_dir / (file_name + ".txt")

            if in_label_path.exists():
                tree = resize_xml_labels(in_label_path, new_size, original_size, crop_box, "deep_learning", scale, (pad_x, pad_y))
                xml_to_txt(tree, out_label_path, new_size, "deep_learning")


def preprocess_dataset(input_folder, output_folder, mode="classic_vision", new_size=(512, 512)):
    """
    Preprocesa un dataset de imágenes según el modo especificado.

    Parámetros:
        input_folder (str): Ruta al directorio de datos de entrada (raw).
        output_folder (str): Ruta donde se guardarán los datos procesados.
        mode (str): Tipo de preprocesamiento. Puede ser "classic_vision" o "deep_learning".
        new_size (tuple): Tamaño al que se redimensionarán las imágenes (ancho, alto).
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)

    if mode == "classic_vision":
        preprocess_cv(input_path, output_path, new_size)
    elif mode == "deep_learning":
        preprocess_dl(input_path, output_path, new_size)
    else:
        raise ValueError(f"Modo '{mode}' no reconocido")

########################################################################################################################
#                                                                                                                      #
#                                     FLUJO PRINCIPAL DE PREPROCESAMIENTO DE DATOS                                     #
#                                                                                                                      #
########################################################################################################################

if __name__ == "__main__":
    input_folder = "../data/raw"
    output_folder_cv = "../data/processed_cv"
    output_folder_dl = "../data/processed_dl"
    mode = "all"

    print("Comenzando preprocesamiento de datos")
    if mode == "classic_vision":
        preprocess_dataset(input_folder, output_folder_cv, mode)
    elif mode == "deep_learning":
        preprocess_dataset(input_folder, output_folder_dl, mode)
    elif mode == "all":
        preprocess_dataset(input_folder, output_folder_cv, "classic_vision")
        preprocess_dataset(input_folder, output_folder_dl, "deep_learning")
    else:
        raise ValueError(f"Modo '{mode}' no reconocido")
    print("Preprocesado de datos finalizado")