from ultralytics import YOLO
from pathlib import Path

########################################################################################################################

def load_model(model_path):
    """
    Carga un modelo YOLOv8 desde un archivo .pt.

    Parámetros:
        model_path (str | Path): Ruta al archivo del modelo .pt

    Devuelve:
        YOLO: Objeto del modelo cargado
    """
    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"El archivo de modelo no existe: {model_path}")
    model = YOLO(str(model_path))
    return model
