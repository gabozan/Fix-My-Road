from pathlib import Path
import random
import shutil

########################################################################################################################

def move_files(image_list, img_dest, label_dest, labels_source):
    """
    Mueve imágenes y sus etiquetas correspondientes a las carpetas de destino.

    Parámetros:
        image_list (list[Path]): Lista de rutas a imágenes a mover.
        img_dest (Path): Carpeta destino para las imágenes.
        label_dest (Path): Carpeta destino para las etiquetas.
        labels_source (Path): Carpeta origen de las etiquetas.
    """
    for img_path in image_list:
        base_name = img_path.stem
        label_path = labels_source / f"{base_name}.txt"

        img_dst = img_dest / img_path.name
        label_dst = label_dest / label_path.name

        if img_path.exists() and label_path.exists():
            shutil.move(str(img_path), str(img_dst))
            shutil.move(str(label_path), str(label_dst))
        else:
            print(f"Faltan archivos para {base_name}")


def clean_empty_folder(folder_path):
    """
    Elimina una carpeta si está vacía.

    Parámetros:
        folder_path (Path): Ruta de la carpeta a comprobar y eliminar.
    """
    if folder_path.exists() and not any(folder_path.iterdir()):
        folder_path.rmdir()


def split_dataset(dataset_dir, train_split=0.8, seed=42):
    """
    Divide un conjunto de datos en entrenamiento y validación de forma aleatoria pero reproducible.

    Parámetros:
        dataset_dir (str): Ruta al directorio del dataset que contiene 'train' y 'labels'.
        train_split (float): Proporción de datos para entrenamiento (valor entre 0 y 1).
        seed (int): Semilla para la aleatorización.
    """
    dataset_path = Path(dataset_dir)

    images_path = dataset_path / "train"
    labels_path = dataset_path / "labels"

    new_images_train = dataset_path / "images/train"
    new_images_val = dataset_path / "images/val"
    new_labels_train = dataset_path / "labels/train"
    new_labels_val = dataset_path / "labels/val"

    for path in [new_images_train, new_images_val, new_labels_train, new_labels_val]:
        path.mkdir(parents=True, exist_ok=True)

    all_images = list(images_path.glob('*.jpg'))
    random.seed(seed)
    random.shuffle(all_images)

    split_idx = int(len(all_images) * train_split)
    train_images = all_images[:split_idx]
    val_images = all_images[split_idx:]

    move_files(train_images, new_images_train, new_labels_train, labels_path)
    move_files(val_images, new_images_val, new_labels_val, labels_path)

    clean_empty_folder(images_path)
    clean_empty_folder(labels_path)

########################################################################################################################
#                                                                                                                      #
#                                        FLUJO PRINCIPAL DE PARTICIÓN DE DATOS                                         #
#                                                                                                                      #
########################################################################################################################

if __name__ == "__main__":
    input_folder_cv = "../data/processed_cv"
    input_folder_dl = "../data/processed_dl"
    mode = "all"
    train_split = 0.8
    seed = 24

    print("Comenzando partición de datos")
    if mode == "classic_vision":
        split_dataset(input_folder_cv, train_split, seed)
    elif mode == "deep_learning":
        split_dataset(input_folder_dl, train_split, seed)
    elif mode == "all":
        split_dataset(input_folder_cv, train_split, seed)
        split_dataset(input_folder_dl, train_split, seed)
    else:
        raise ValueError(f"Modo '{mode}' no reconocido")
    print("Partición de datos finalizada")