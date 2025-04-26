from ultralytics import YOLO
from deep_learning.config import MODELS, DATA_YAML, IMG_SIZE, EPOCHS, BATCH_SIZE

########################################################################################################################

def train_model(model_name):
    print(f"Entrenando modelo: {model_name}")
    model = YOLO(MODELS[model_name])
    model.train(
        data=DATA_YAML,
        imgsz=IMG_SIZE,
        epochs=EPOCHS,
        batch=BATCH_SIZE,
        name=f"train_{model_name}"
    )

if __name__ == "__main__":
    for model_name in MODELS.keys():
        train_model(model_name)
