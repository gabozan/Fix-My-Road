from pathlib import Path
import xml.etree.ElementTree as ET
import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob


def load_image(path):
    """
    Carga una imagen desde el disco y la convierte de BGR a RGB.

    Parámetros:
        path (str): Ruta del archivo de imagen.

    Retorna:
        img (np.ndarray): Imagen en formato RGB.
    """
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def resize_xml_labels(in_xml_path, new_size, original_size, crop_box):
    """
    Ajusta las coordenadas de las etiquetas en un archivo XML (formato Pascal VOC)
    cuando la imagen ha sido recortada y/o redimensionada.

    Parámetros:
        in_xml_path (str): Ruta al archivo XML original.
        new_size (tuple): Nueva resolución de la imagen (ancho, alto).
        original_size (tuple): Resolución original de la imagen (ancho, alto).
        crop_box (tuple[int, int, int, int] | None): Coordenadas del recorte en formato (x0, y0, ancho, alto).

    Retorna:
        tree (xml.etree.ElementTree.ElementTree): Árbol XML con las etiquetas actualizadas.
    """
    tree = ET.parse(in_xml_path)
    root = tree.getroot()

    new_w, new_h = new_size
    orig_w, orig_h = original_size

    if crop_box is None:
        crop_x, crop_y, crop_w, crop_h = 0, 0, orig_w, orig_h
    else:
        crop_x, crop_y, crop_w, crop_h = crop_box

    sx = new_w / crop_w
    sy = new_h / crop_h

    for obj in root.findall("object"):
        bb = obj.find("bndbox")
        # x -------------------------------------------------------------
        xmin = int(bb.find("xmin").text) - crop_x
        xmax = int(bb.find("xmax").text) - crop_x
        xmin = max(0, min(xmin, crop_w))
        xmax = max(0, min(xmax, crop_w))
        bb.find("xmin").text = str(int(xmin * sx))
        bb.find("xmax").text = str(int(xmax * sx))
        # y -------------------------------------------------------------
        ymin = int(bb.find("ymin").text) - crop_y
        ymax = int(bb.find("ymax").text) - crop_y
        ymin = max(0, min(ymin, crop_h))
        ymax = max(0, min(ymax, crop_h))
        bb.find("ymin").text = str(int(ymin * sy))
        bb.find("ymax").text = str(int(ymax * sy))
    return tree


def xml_to_txt(tree, out_label_path, img_size, mode="classic_vision"):
    """
    Convierte un árbol XML a un archivo txt compatible con visión 
    clásica o con YOLO (deep learning).

    Parámetros:
        tree (ElementTree): Árbol XML.
        out_label_path (Path): Ruta al archivo txt de salida.
        mode (str): 'clasica' para formato xmin,ymin,xmax,ymax,
                    'deep learning' para formato YOLO normalizado.
        img_size (tuple): Tamaño de la imagen final (ancho, alto).
    """
    root = tree.getroot()
    w, h = img_size
    lines = []

    for obj in root.findall("object"):
        name = obj.find("name").text
        bndbox = obj.find("bndbox")
        xmin = int(bndbox.find("xmin").text)
        xmax = int(bndbox.find("xmax").text)
        ymin = int(bndbox.find("ymin").text)
        ymax = int(bndbox.find("ymax").text)

        if mode == "classic_vision":
            lines.append(f"{name} {xmin} {ymin} {xmax} {ymax}")
        elif mode == "deep_learning":
            x_center = (xmin + xmax) / 2 / w
            y_center = (ymin + ymax) / 2 / h
            width    = (xmax - xmin) / w
            height   = (ymax - ymin) / h
            lines.append(f"{name} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
        else:
            raise ValueError(f"Modo '{mode}' no reconocido")

    with open(out_label_path, "w") as f:
        f.write("\n".join(lines))



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

        for image_file in in_image_dir.glob("*.jpg"):
            file_name = image_file.stem
            img = load_image(str(image_file))
            original_size = (img.shape[1], img.shape[0])

            crop_box = None
            if "norway" in file_name.lower():
                crop_w = original_size[0] // 2
                crop_box = (0, 0, crop_w, original_size[1])
                img = img[:, :crop_w]
            img_resized = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
            img_resized = cv2.cvtColor(img_resized, cv2.COLOR_RGB2BGR)
            cv2.imwrite(str(out_image_dir / image_file.name), img_resized)
            
            in_label_path = input_path / "labels" / (file_name + ".xml")
            out_label_path = output_path / "labels" / (file_name + ".txt")

            if in_label_path.exists():
                tree = resize_xml_labels(in_label_path, new_size, original_size, crop_box)
                xml_to_txt(tree, out_label_path, new_size, "classic_vision")


def preprocess_dl(input_path, output_path, new_size):
    for split in ["train", "test"]:
        in_image_dir = input_path / split
        out_image_dir = output_path / split

        for image_file in in_image_dir.glob("*.jpg"):
            file_name = image_file.stem
            img = load_image(str(image_file))
            original_size = (img.shape[1], img.shape[0])

            #img_resized = crop_and_resize_image(file_name, img, original_size, new_size)
            img_resized = cv2.cvtColor(img_resized, cv2.COLOR_RGB2BGR)
            cv2.imwrite(str(out_image_dir / image_file.name), img_resized)
            
            in_label_path = input_path / "labels" / (file_name + ".xml")
            out_label_path = output_path / "labels" / (file_name + ".txt")

            if in_label_path.exists():
                tree = resize_xml_labels(in_label_path, new_size, original_size)
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





if __name__ == "__main__":
    input_folder_cv = "../data/raw"
    output_folder_cv = "../data/processed_cv"

    print("😏 Comenzando preprocesamiento de datos 😏")
    preprocess_dataset(input_folder_cv, output_folder_cv, "classic_vision")
    print("😎 Preprocesado de datos finalizado 😎")