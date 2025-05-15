from pathlib import Path
import csv
from utils import load_image, save_image
from preprocessing import letterbox
from model import load_model
from predict import predict_image
import time

########################################################################################################################

MODEL_PATH = "theRoadFixer.pt"
INPUT_DIR = Path("../data/raw/test/")
PROCESSED_DIR = Path("../data/processed_dl/test/")
OUTPUT_DIR = Path("../predictions/")
CSV_PATH = OUTPUT_DIR / "submission_overall.csv"

########################################################################################################################

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

model = load_model(MODEL_PATH)
csv_rows = []

start_time = time.time()
num_images = 0

for image_file in INPUT_DIR.glob("*.jpg"):
    num_images += 1
    file_name = image_file.stem
    img = load_image(image_file)
    original_size = (img.shape[1], img.shape[0])
    img_resized, scale, (left, top) = letterbox(img, original_size)
    save_image((PROCESSED_DIR / f"{file_name}.jpg"), img_resized)
    results = predict_image(model, (PROCESSED_DIR / f"{file_name}.jpg"))
    boxes = results[0].boxes

    predictions = []
    scores = boxes.conf.tolist()
    classes = boxes.cls.tolist()
    coords = boxes.xyxy.tolist()

    full_preds = [(scores[i], int(classes[i]) + 1, coords[i]) for i in range(len(boxes))]
    full_preds.sort(reverse=True, key=lambda x: x[0])
    top_preds = full_preds[:5]

    for score, class_id, (x1, y1, x2, y2) in top_preds:
        x1 = int((x1 - left) / scale)
        y1 = int((y1 - top) / scale)
        x2 = int((x2 - left) / scale)
        y2 = int((y2 - top) / scale)
        predictions.extend([class_id, x1, y1, x2, y2])

    prediction_str = " ".join(map(str, predictions))
    csv_rows.append({
        "ImageId": file_name,
        "PredictionString": prediction_str
    })

end_time = time.time()
total_time = end_time - start_time
avg_time_per_image = total_time / num_images if num_images else 0

print(f"Tiempo total: {total_time:.2f} segundos")
print(f"Tiempo medio por imagen: {avg_time_per_image:.4f} segundos")

with CSV_PATH.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["ImageId", "PredictionString"])
    writer.writeheader()
    writer.writerows(csv_rows)

########################################################################################################################

csv_input_path = CSV_PATH
output_dir = OUTPUT_DIR
output_dir.mkdir(exist_ok=True)

files = {
    "India": open(output_dir / "submission_india.csv", "w", newline=''),
    "Japan": open(output_dir / "submission_japan.csv", "w", newline=''),
    "Norway": open(output_dir / "submission_norway.csv", "w", newline=''),
    "United_States": open(output_dir / "submission_us.csv", "w", newline=''),
}

writers = {country: csv.writer(f, quoting=csv.QUOTE_MINIMAL) for country, f in files.items()}

with open(csv_input_path, "r") as infile:
    reader = csv.reader(infile)
    header = next(reader)
    for writer in writers.values():
        writer.writerow(header)

    for row in reader:
        filename = row[0]
        if filename.startswith("India_"):
            writers["India"].writerow(row)
        elif filename.startswith("Japan_"):
            writers["Japan"].writerow(row)
        elif filename.startswith("Norway_"):
            writers["Norway"].writerow(row)
        elif filename.startswith("United_States_"):
            writers["United_States"].writerow(row)

for f in files.values():
    f.close()