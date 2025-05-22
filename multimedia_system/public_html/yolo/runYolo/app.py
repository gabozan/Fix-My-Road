import os
import tempfile
from flask import Flask, request, jsonify
from google.cloud import storage
from google.cloud.sql.connector import Connector, IPTypes
import traceback
from ultralytics import YOLO
from pathlib import Path
import cv2
import numpy as np
import json
import shutil

damages = {
    0: "longitudinal",
    1: "transversal",
    2: "cocodrilo",
    3: "bache"
}

points = {
    0: 10,
    1: 10,
    2: 30,
    3: 50
}

app = Flask(__name__)

gcs = storage.Client()
connector = Connector(ip_type=IPTypes.PUBLIC)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "theRoadFixer.pt")
model = YOLO(MODEL_PATH)

def get_db_connection():
    inst_conn_name = os.environ["INSTANCE_CONNECTION_NAME"]
    db_user = os.environ.get("DB_USER", "postgres")
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ.get("DB_NAME", "postgres")
    return connector.connect(
        inst_conn_name,
        "pg8000",
        user=db_user,
        password=db_pass,
        db=db_name
    )

def download_to_temp(bucket, path, suffix):
    tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    bucket.blob(path).download_to_filename(tmp.name)
    tmp.close()
    return tmp.name

def load_image(path):
    return cv2.imread(str(path))

def save_image(path, img):
    cv2.imwrite(str(path), img)

def letterbox(img,new_size=(512, 512),color=(114, 114, 114)):
    img = img.astype(np.uint8) if img.dtype != np.uint8 else img
    orig_h, orig_w = img.shape[:2]
    new_w, new_h = new_size
    scale = min(new_w / orig_w, new_h / orig_h)
    resize_w, resize_h = int(orig_w * scale), int(orig_h * scale)
    img_resized = cv2.resize(img, (resize_w, resize_h), interpolation=cv2.INTER_LINEAR)
    pad_w = new_w - resize_w
    pad_h = new_h - resize_h
    top = pad_h // 2
    bottom = pad_h - top
    left = pad_w // 2
    right = pad_w - left
    img_padded = cv2.copyMakeBorder(img_resized, top, bottom, left, right,borderType=cv2.BORDER_CONSTANT, value=color)
    return img_padded, scale, (left, top)

@app.route('/process', methods=['POST'])
def process_video():
    try:
        data = request.get_json()
        bucket = gcs.bucket(data['bucket'])
        base_name = data['baseName'] #21_timestamp
        user_id = data['userId'] #21
        video_id = base_name.split('_')[1] #timestamp

        video_file, positions_file = (
            download_to_temp(bucket, f"videos/{base_name}_video.webm", ".webm"),
            download_to_temp(bucket, f"positions/{base_name}_positions.json", ".json")
        )

        input_dir = Path(tempfile.mkdtemp())
        processed_dir = input_dir / "processed"
        processed_dir.mkdir(parents=True, exist_ok=True)

        cap = cv2.VideoCapture(video_file)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * 0.5)

        with open(positions_file, 'r') as f:
            positions = json.load(f)

        frame_idx = 0
        saved_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or saved_idx >= len(positions):
                break
            if frame_idx % frame_interval == 0:
                frame_path = input_dir / f"frame_{saved_idx}.jpg"
                cv2.imwrite(str(frame_path), frame)
                saved_idx += 1
            frame_idx += 1
        cap.release()

        total_points = 0
        detections = []

        sorted_files = sorted(input_dir.glob("*.jpg"), key=lambda f: int(f.stem.split('_')[1]))
        for i, image_file in enumerate(sorted_files):
            if i >= len(positions):
                break
            file_name = image_file.stem
            lat = positions[i]["lat"]
            lon = positions[i]["lon"]

            img = load_image(image_file)
            original_size = (img.shape[1], img.shape[0])
            img_resized, scale, _ = letterbox(img, original_size)
            processed_path = processed_dir / f"{file_name}.jpg"
            save_image(processed_path, img_resized)
            results = model(str(processed_path))
            boxes = results[0].boxes

            if len(boxes) > 0:
                classes = [int(c) for c in boxes.cls.tolist()]
                for cls in classes:
                    total_points += points[cls]
                worst_class = max(classes)

                dest = f"detections/{user_id}/{video_id}/{file_name}.jpg"
                bucket.blob(dest).upload_from_filename(str(processed_path), content_type='image/jpeg')
                public_url = f"https://storage.googleapis.com/{bucket.name}/{dest}"

                detections.append({
                    "damage": damages[worst_class],
                    "path": public_url,
                    "lat": lat,
                    "lon": lon
                })
        # CONECTAR CON LAS BD
        conn = get_db_connection()
        cur = conn.cursor()
        # AÑADIR DAÑOS DETECTADOS
        for det in detections:
            cur.execute('''
                INSERT INTO reports (id_user, damage_type, image_url, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s)
            ''', (
                user_id,
                det["damage"],
                det["path"],
                det["lat"],
                det["lon"]
            ))
        # ACTUALIZAR TABLAS SI USUARIO EXISTE
        if user_id != "none":
            cur.execute('SELECT score FROM "user" WHERE id_user = %s', (user_id,))
            result = cur.fetchone()
            current_score = result[0] if result else 0
            new_score = current_score + total_points
            cur.execute('UPDATE "user" SET score = %s WHERE id_user = %s', (new_score, user_id))
        # CERRAR LAS CONEXIONES
        conn.commit()
        cur.close()
        conn.close()
        # ELIMINAR EL VIDEO Y LAS POSICIONES
        os.remove(video_file)
        os.remove(positions_file)
        shutil.rmtree(input_dir)
        return '',204
    except Exception as e:
        print("[ERROR]", traceback.format_exc())
        return jsonify({'error': str(e)}), 500