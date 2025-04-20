import cv2

########################################################################################################################

def letterbox(img, original_size, new_size=(512, 512), color=(114, 114, 114)):
    """
    Redimensiona una imagen manteniendo el aspect ratio y aplica padding
    para ajustarla al tamaño deseado.

    Parámetros:
        img (np.ndarray): Imagen original
        original_size (tuple): Tamaño original de la imagen (ancho, alto)
        new_size (tuple): Tamaño final deseado (ancho, alto)
        color (tuple): Color del padding

    Retorna:
        img_padded (np.ndarray): Imagen final con padding ajustada a new_size
        scale (float): Escala aplicada para redimensionar la imagen original
        padding (tuple): Padding aplicado (padding_x, padding_y)
    """
    orig_w, orig_h = original_size
    new_w, new_h = new_size
    scale = min(new_w / orig_w, new_h / orig_h)
    resize_w, resize_h = int(orig_w * scale), int(orig_h * scale)

    img_resized = cv2.resize(img, (resize_w, resize_h), interpolation=cv2.INTER_LINEAR)

    pad_w = new_w - resize_w
    pad_h = new_h - resize_h
    top = pad_h // 2
    bottom = pad_h - top
    left = pad_w // 2
    right = pad_w - left

    img_padded = cv2.copyMakeBorder(img_resized, top, bottom, left, right,
                                    borderType=cv2.BORDER_CONSTANT, value=color)
    return img_padded, scale, (left, top)