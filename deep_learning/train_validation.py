from ultralytics import YOLO
from deep_learning.config import (
    MODEL, DATA_YAML, IMG_SIZE, DEVICE, PROJECT
)
from pathlib import Path
import json
from itertools import product

# Hiperparámetros a explorar en el grid search
#FLIP_LR_VALUES = [0.3, 0.5]
#HSV_H_VALUES = [0.01, 0.015]
#HSV_S_VALUES = [0.6, 0.7]
#HSV_V_VALUES = [0.3, 0.4]
#BATCH_SIZES = [16, 32]
#EPOCHS_VALUES = [30, 50]

FLIP_LR_VALUES = [0.3]
HSV_H_VALUES = [0.01]
HSV_S_VALUES = [0.6]
HSV_V_VALUES = [0.3]
BATCH_SIZES = [16]
EPOCHS_VALUES = [1]

########################################################################################################################

def train_and_validate(fliplr, hsv_h, hsv_s, hsv_v, batch_size, epochs, run_id):
    """
    Entrena y valida un modelo YOLOv8 con hiperparámetros personalizados.

    Parámetros:
        fliplr, hsv_h, hsv_s, hsv_v (float): Hiperparámetros de data augmentation
        batch_size (int): Tamaño de batch
        epochs (int): Número de épocas
        run_id (str): Identificador del experimento
    """
    model_name = Path(MODEL).stem
    experiment_name = f"grid_{run_id}"
    print(f"Entrenando experimento: {experiment_name}")

    model = YOLO(MODEL)

    model.train(
        data=DATA_YAML,
        imgsz=IMG_SIZE,
        epochs=epochs,
        batch=batch_size,
        device=DEVICE,
        name=experiment_name,
        project=PROJECT,
        verbose=True,
        fliplr=fliplr,
        hsv_h=hsv_h,
        hsv_s=hsv_s,
        hsv_v=hsv_v
    )

    print("\nEntrenamiento finalizado.")
    save_path = Path(PROJECT) / experiment_name / "weights"
    print(f"Pesos guardados en {save_path}\n")

    print("Validando modelo entrenado...")
    metrics = model.val()

    mAP50 = metrics.box.map50 if hasattr(metrics.box, "map50") else 0
    mAP5095 = metrics.box.map if hasattr(metrics.box, "map") else 0
    f1_score = float(metrics.box.f1.mean()) if hasattr(metrics.box, "f1") else 0

    results_path = Path(PROJECT) / experiment_name / "metrics.json"
    with open(results_path, "w") as f:
        json.dump({
            "mAP@0.5": mAP50,
            "mAP@0.5:0.95": mAP5095,
            "f1_score": f1_score,
            "fliplr": fliplr,
            "hsv_h": hsv_h,
            "hsv_s": hsv_s,
            "hsv_v": hsv_v,
            "batch_size": batch_size,
            "epochs": epochs
        }, f, indent=4)
    print(f"Métricas guardadas en {results_path}\n")

########################################################################################################################
#                                                                                                                      #
#                                   FLUJO DE GRID SEARCH DE HIPERPARÁMETROS                                            #
#                                                                                                                      #
########################################################################################################################

if __name__ == "__main__":
    grid = list(product(
        FLIP_LR_VALUES,
        HSV_H_VALUES,
        HSV_S_VALUES,
        HSV_V_VALUES,
        BATCH_SIZES,
        EPOCHS_VALUES
    ))

    train_and_validate(fliplr=0.3, hsv_h=0.01, hsv_s=0.6, hsv_v=0.3, batch_size=16, epochs=1, run_id="prueba")