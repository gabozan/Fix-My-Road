from ultralytics import YOLO
from deep_learning.config import MODEL, DATA_YAML, IMG_SIZE, DEVICE, PROJECT
from pathlib import Path
import json
import random

########################################################################################################################

FLIP_LR_VALUES = [0.3, 0.5]
HSV_H_VALUES   = [0.01, 0.015]
HSV_S_VALUES   = [0.6,  0.7]
HSV_V_VALUES   = [0.3,  0.4]
SCALE_VALUES   = [0.3,  0.5]
BATCH_SIZES    = [8, 16]
EPOCHS_VALUES  = [30, 50]

########################################################################################################################

def train_and_validate(fliplr, hsv_h, hsv_s, hsv_v, scale, batch_size, epochs, run_id):
    """
    Entrena y valida un YOLOv8 con hiperparámetros personalizados.
    """
    experiment_name = f"grid_{run_id}"
    print(f"\nEntrenando experimento: {experiment_name}")

    model = YOLO(MODEL, seed=24)

    model.train(
        seed=24,
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
        scale=scale,
        cache = True,
        workers = 8,
        half = True
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
            "weights":    str(Path(PROJECT) / experiment_name / "weights" / "best.pt")
        }, f, indent=4)
    print(f"Métricas guardadas en {results_path}\n")



if __name__ == "__main__":
    n_trials = 12
    random.seed(24)
    for i in range(n_trials):
        fl = random.choice(FLIP_LR_VALUES)
        hh = random.choice(HSV_H_VALUES)
        hs = random.choice(HSV_S_VALUES)
        hv = random.choice(HSV_V_VALUES)
        sc = random.choice(SCALE_VALUES)
        bs = random.choice(BATCH_SIZES)
        ep = random.choice(EPOCHS_VALUES)
        run_id = f"{i:03d}_f{fl}_hh{hh}_hs{hs}_hv{hv}_sc{sc}_b{bs}_e{ep}"
        train_and_validate(fliplr=fl, hsv_h=hh, hsv_s=hs, hsv_v=hv, scale=sc, batch_size=bs, epochs=ep, run_id=run_id)