from pathlib import Path
import csv
from model import load_model
from predict import predict_image

########################################################################################################################

MODEL_PATH = "theRoadFixer.pt"
IMAGES_DIR = Path("../data/processed_dl/test/")
OUTPUT_DIR = Path("../predictions/")
CSV_PATH = OUTPUT_DIR / "predictions_dl.csv"

########################################################################################################################

model = load_model(MODEL_PATH)
csv_rows = []

for image_file in IMAGES_DIR.glob("*.jpg"):
    file_name = image_file.stem
    results = predict_image(model, image_file)
    boxes = results[0].boxes

    predictions = []
    for i in range(len(boxes)):
        class_id = boxes.cls[i]
        x1, y1, x2, y2 = boxes.xyxy[i].tolist()
        predictions.extend([int(class_id), int(x1), int(y1), int(x2), int(y2)])

    prediction_str = " ".join(map(str, predictions))
    csv_rows.append({
        "ImageId": file_name,
        "PredictionString": prediction_str
    })

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
with CSV_PATH.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["ImageId", "PredictionString"])
    writer.writeheader()
    writer.writerows(csv_rows)