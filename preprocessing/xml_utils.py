import xml.etree.ElementTree as ET

########################################################################################################################

def resize_xml_labels(in_xml_path, new_size, original_size, crop_box, mode="classic_vision", scale=None, padding=(0, 0)):
    """
    Ajusta las coordenadas de las etiquetas en un archivo XML (formato Pascal VOC)
    cuando la imagen ha sido recortada y/o redimensionada.

    Parámetros:
        in_xml_path (str): Ruta al archivo XML original.
        new_size (tuple): Nueva resolución de la imagen (ancho, alto).
        original_size (tuple): Resolución original de la imagen (ancho, alto).
        crop_box (tuple[int, int, int, int] | None): Coordenadas del recorte en formato (x0, y0, ancho, alto).
        mode (str): Modo de procesamiento. Puede ser "classic_vision" o "deep_learning".
        scale (float | None): Escala aplicada en letterbox (solo para deep_learning).
        padding (tuple): Padding aplicado en letterbox (pad_x, pad_y).

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
        xmin = int(float(bb.find("xmin").text)) - crop_x
        xmax = int(float(bb.find("xmax").text)) - crop_x
        ymin = int(float(bb.find("ymin").text)) - crop_y
        ymax = int(float(bb.find("ymax").text)) - crop_y

        xmin = max(0, min(xmin, crop_w))
        xmax = max(0, min(xmax, crop_w))
        ymin = max(0, min(ymin, crop_h))
        ymax = max(0, min(ymax, crop_h))

        if mode == "classic_vision":
            bb.find("xmin").text = str(int(xmin * sx))
            bb.find("xmax").text = str(int(xmax * sx))
            bb.find("ymin").text = str(int(ymin * sy))
            bb.find("ymax").text = str(int(ymax * sy))
        elif mode == "deep_learning":
            pad_x, pad_y = padding
            xmin = xmin * scale + pad_x
            xmax = xmax * scale + pad_x
            ymin = ymin * scale + pad_y
            ymax = ymax * scale + pad_y
            bb.find("xmin").text = str(int(xmin))
            bb.find("xmax").text = str(int(xmax))
            bb.find("ymin").text = str(int(ymin))
            bb.find("ymax").text = str(int(ymax))
        else:
            raise ValueError(f"Modo '{mode}' no reconocido")
    return tree


def xml_to_txt(tree, out_label_path, img_size, mode="classic_vision"):
    """
    Convierte un árbol XML a un archivo txt compatible con visión
    clásica o con YOLO (deep learning), filtrando solo D00, D10, D20, D40.

    Parámetros:
        tree (ElementTree): Árbol XML.
        out_label_path (Path): Ruta al archivo txt de salida.
        mode (str): 'clasica' para formato xmin,ymin,xmax,ymax,
                    'deep learning' para formato YOLO normalizado.
        img_size (tuple): Tamaño de la imagen final (ancho, alto).
    """
    CLASS_MAPPING = {
        'D00': 0,
        'D10': 1,
        'D20': 2,
        'D40': 3
    }

    root = tree.getroot()
    w, h = img_size
    lines = []

    for obj in root.findall("object"):
        name = obj.find("name").text
        if name not in CLASS_MAPPING:
            continue
        class_id = CLASS_MAPPING[name]
        bndbox = obj.find("bndbox")
        xmin = int(bndbox.find("xmin").text)
        xmax = int(bndbox.find("xmax").text)
        ymin = int(bndbox.find("ymin").text)
        ymax = int(bndbox.find("ymax").text)

        if mode == "classic_vision":
            lines.append(f"{class_id} {xmin} {ymin} {xmax} {ymax}")
        elif mode == "deep_learning":
            x_center = (xmin + xmax) / 2 / w
            y_center = (ymin + ymax) / 2 / h
            width    = (xmax - xmin) / w
            height   = (ymax - ymin) / h
            lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
        else:
            raise ValueError(f"Modo '{mode}' no reconocido")

    with open(out_label_path, "w") as f:
        f.write("\n".join(lines))