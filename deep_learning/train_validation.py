from ultralytics import YOLO
from deep_learning.config import MODEL, DATA_YAML, IMG_SIZE, DEVICE, PROJECT
from pathlib import Path
import json
from itertools import product
from datetime import datetime

########################################################################################################################

FLIP_LR_VALUES = [0.3, 0.5]
HSV_H_VALUES   = [0.01, 0.015]
HSV_S_VALUES   = [0.6,  0.7]
HSV_V_VALUES   = [0.3,  0.4]
SCALE_VALUES   = [0.3,  0.5]
BATCH_SIZES    = [8, 16]
EPOCHS_VALUES  = [30, 50]

def train_and_validate(fliplr, hsv_h, hsv_s, hsv_v, scale, batch_size, epochs, run_id):
    """
    Entrena y valida un YOLOv8 con hiperparámetros personalizados.
    """
    experiment_name = f"grid_{run_id}"
    print(f"\nEntrenando experimento: {experiment_name}")

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
        hsv_v=hsv_v,
        scale=scale
    )

    print("Entrenamiento finalizado.")

    # ────────── VALIDACIÓN ÚNICA (split val) ──────────
    metrics = model.val(split="val", save=False, plots=False)

    mAP50 = metrics.box.map50 if hasattr(metrics.box, "map50") else 0
    mAP5095 = metrics.box.map if hasattr(metrics.box, "map") else 0
    f1 = float(metrics.box.f1.mean()) if hasattr(metrics.box, "f1") else 0

    # ────────── GUARDAR MÉTRICAS ──────────
    results_path = Path(PROJECT) / experiment_name / "metrics.json"
    results_path.parent.mkdir(parents=True, exist_ok=True)
    with open(results_path, "w") as f:
        json.dump({
            "timestamp":  datetime.now().isoformat(timespec="seconds"),
            "mAP@0.5":    mAP50,
            "mAP@0.5:0.95": mAP5095,
            "f1_score":   f1,
            "fliplr":     fliplr,
            "hsv_h":      hsv_h,
            "hsv_s":      hsv_s,
            "hsv_v":      hsv_v,
            "scale":      scale,
            "batch_size": batch_size,
            "epochs":     epochs,
            "patience":   patience,
            "weights":    str(Path(PROJECT) / experiment_name / "weights" / "best.pt")
        }, f, indent=4)
    print(f"Métricas guardadas en {results_path}\n")



if __name__ == "__main__":

    grid = list(product(
        FLIP_LR_VALUES,
        HSV_H_VALUES,
        HSV_S_VALUES,
        HSV_V_VALUES,
        SCALE_VALUES,
        BATCH_SIZES,
        EPOCHS_VALUES
    ))

    for i, (fl, hh, hs, hv, sc, bs, ep) in enumerate(grid):
        run_id = (f"{i:03d}_f{fl}_hh{hh}_hs{hs}_hv{hv}"
                  f"_sc{sc}_b{bs}_e{ep}")
        train_and_validate(fliplr=fl, hsv_h=hh, hsv_s=hs, hsv_v=hv, scale=sc, batch_size=bs, epochs=ep,
                           run_id=run_id, patience=50)