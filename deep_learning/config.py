# config.py

MODELS = {
    "nano": "yolov8n.pt",
    "small": "yolov8s.pt"
}

DATA_YAML = "../data/processed_dl/data.yaml"
IMG_SIZE = 512
EPOCHS = 50
BATCH_SIZE = 16
CONF_THRES = 0.25