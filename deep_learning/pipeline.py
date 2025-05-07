from pathlib import Path
import csv
from utils import load_image, save_image
from preprocessing import letterbox
from model import load_model
from predict import predict_image


########################################################################################################################

MODEL_PATH = "theRoadFixer.pt"
INPUT_DIR = Path("../data/raw/test/")
PROCESSED_DIR = Path("../data/processed_dl/test/")
OUTPUT_DIR = Path("../predictions/")
CSV_PATH = OUTPUT_DIR / "predictions_dl.csv"

########################################################################################################################

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

model = load_model(MODEL_PATH)
csv_rows = []

for image_file in INPUT_DIR.glob("*.jpg"):
    file_name = image_file.stem
    img = load_image(image_file)
    original_size = (img.shape[1], img.shape[0])
    img_resized, scale, (left, top) = letterbox(img, original_size)
    save_image((PROCESSED_DIR / f"{file_name}.jpg"), img_resized)
    results = predict_image(model, (PROCESSED_DIR / f"{file_name}.jpg"))
    boxes = results[0].boxes

    predictions = []
    for i in range(len(boxes)):
        class_id = boxes.cls[i]
        x1, y1, x2, y2 = map(float, boxes.xyxy[i].tolist())

        x1 = (x1 - left) / scale
        y1 = (y1 - top) / scale
        x2 = (x2 - left) / scale
        y2 = (y2 - top) / scale

        predictions.extend([int(class_id), int(x1), int(y1), int(x2), int(y2)])

    prediction_str = " ".join(map(str, predictions))
    csv_rows.append({
        "ImageId": file_name,
        "PredictionString": prediction_str
    })

with CSV_PATH.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["ImageId", "PredictionString"])
    writer.writeheader()
    writer.writerows(csv_rows)