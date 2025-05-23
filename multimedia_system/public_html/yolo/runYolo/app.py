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
import sys

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
print(f"[INFO] Comprobando modelo en {MODEL_PATH}, existe? {os.path.exists(MODEL_PATH)}", file=sys.stderr, flush=True)

try:
    model = YOLO(MODEL_PATH)
    print("[INFO] Modelo cargado correctamente.", file=sys.stderr, flush=True)
except Exception:
    print("[ERROR] Excepción cargando el modelo:", file=sys.stderr, flush=True)
    print(traceback.format_exc(), file=sys.stderr, flush=True)
    model = None  # Por si acaso para que no pete más adelante

def get_db_connection():
    try:
        inst_conn_name = os.environ["INSTANCE_CONNECTION_NAME"]
        db_user = os.environ.get("DB_USER", "postgres")
        db_pass = os.environ["DB_PASS"]
        db_name = os.environ.get("DB_NAME", "postgres")
        print(f"[INFO] Conectando a BD: instancia={inst_conn_name}, usuario={db_user}, base={db_name}", file=sys.stderr, flush=True)
        return connector.connect(
            inst_conn_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name
        )
    except Exception:
        print("[ERROR] Excepción conectando a la BD:", file=sys.stderr, flush=True)
        print(traceback.format_exc(), file=sys.stderr, flush=True)
        raise

def download_to_temp(bucket, path, suffix):
    try:
        tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        print(f"[INFO] Descargando {path} a temporal {tmp.name}", file=sys.stderr, flush=True)
        bucket.blob(path).download_to_filename(tmp.name)
        tmp.close()
        return tmp.name
    except Exception:
        print(f"[ERROR] Excepción descargando archivo {path}:", file=sys.stderr, flush=True)
        print(traceback.format_exc(), file=sys.stderr, flush=True)
        raise

def load_image(path):
    img = cv2.imread(str(path))
    if img is None:
        print(f"[WARNING] No se pudo cargar la imagen en {path}", file=sys.stderr, flush=True)
    else:
        print(f"[INFO] Imagen cargada correctamente desde {path}", file=sys.stderr, flush=True)
    return img

def save_image(path, img):
    try:
        cv2.imwrite(str(path), img)
        print(f"[INFO] Imagen guardada en {path}", file=sys.stderr, flush=True)
    except Exception:
        print(f"[ERROR] Excepción guardando imagen en {path}:", file=sys.stderr, flush=True)
        print(traceback.format_exc(), file=sys.stderr, flush=True)
        raise

def letterbox(img, new_size=(512, 512), color=(114, 114, 114)):
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
    img_padded = cv2.copyMakeBorder(img_resized, top, bottom, left, right, borderType=cv2.BORDER_CONSTANT, value=color)
    print(f"[INFO] Imagen redimensionada y enmarcada: original=({orig_w},{orig_h}), nuevo=({new_w},{new_h}), escala={scale:.3f}", file=sys.stderr, flush=True)
    return img_padded, scale, (left, top)

@app.route('/process', methods=['POST'])
def process_video():
    try:
        data = request.get_json()
        print(f"[INFO] Request recibido: {data}", file=sys.stderr, flush=True)

        bucket_name = data.get('bucket')
        base_name = data.get('baseName')
        user_id = data.get('userId')

        if not bucket_name or not base_name or not user_id:
            error_msg = "Faltan datos necesarios en la petición: bucket, baseName o userId"
            print(f"[ERROR] {error_msg}", file=sys.stderr, flush=True)
            return jsonify({'error': error_msg}), 400

        bucket = gcs.bucket(bucket_name)
        video_id = base_name.split('_')[1] if '_' in base_name else "unknown"
        print(f"[INFO] bucket={bucket_name}, base_name={base_name}, user_id={user_id}, video_id={video_id}", file=sys.stderr, flush=True)

        video_file = download_to_temp(bucket, f"videos/{base_name}_video.webm", ".webm")
        positions_file = download_to_temp(bucket, f"positions/{base_name}_positions.json", ".json")

        input_dir = Path(tempfile.mkdtemp())
        processed_dir = input_dir / "processed"
        processed_dir.mkdir(parents=True, exist_ok=True)

        cap = cv2.VideoCapture(video_file)
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            print(f"[WARNING] FPS del vídeo es 0, usando 1 por defecto", file=sys.stderr, flush=True)
            fps = 1
        frame_interval = int(fps * 0.5)

        with open(positions_file, 'r') as f:
            positions = json.load(f)
        print(f"[INFO] Posiciones cargadas: {len(positions)} puntos", file=sys.stderr, flush=True)

        frame_idx = 0
        saved_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or saved_idx >= len(positions):
                break
            if frame_idx % frame_interval == 0:
                frame_path = input_dir / f"frame_{saved_idx}.jpg"
                save_image(frame_path, frame)
                saved_idx += 1
            frame_idx += 1
        cap.release()
        print(f"[INFO] Frames extraídos: {saved_idx}", file=sys.stderr, flush=True)

        total_points = 0
        detections = []

        sorted_files = sorted(input_dir.glob("*.jpg"), key=lambda f: int(f.stem.split('_')[1]))
        for i, image_file in enumerate(sorted_files):
            if i >= len(positions):
                print(f"[WARNING] Más imágenes que posiciones, ignorando el resto", file=sys.stderr, flush=True)
                break
            file_name = image_file.stem
            lat = positions[i].get("latitude")
            lon = positions[i].get("longitude")

            img = load_image(image_file)
            if img is None:
                print(f"[ERROR] Imagen {image_file} no cargada, saltando...", file=sys.stderr, flush=True)
                continue
            original_size = (img.shape[1], img.shape[0])
            img_resized, scale, _ = letterbox(img, original_size)
            processed_path = processed_dir / f"{file_name}.jpg"
            save_image(processed_path, img_resized)

            if model is None:
                error_msg = "Modelo no cargado, no se puede procesar imagen"
                print(f"[ERROR] {error_msg}", file=sys.stderr, flush=True)
                return jsonify({'error': error_msg}), 500

            results = model(str(processed_path))
            boxes = results[0].boxes

            if len(boxes) > 0:
                classes = [int(c) for c in boxes.cls.tolist()]
                for cls in classes:
                    total_points += points.get(cls, 0)
                worst_class = max(classes)

                dest = f"detections/{user_id}/{video_id}/{file_name}.jpg"
                bucket.blob(dest).upload_from_filename(str(processed_path), content_type='image/jpeg')
                public_url = f"https://storage.googleapis.com/{bucket.name}/{dest}"

                detections.append({
                    "damage": damages.get(worst_class, "unknown"),
                    "path": public_url,
                    "lat": lat,
                    "lon": lon
                })
                print(f"[INFO] Detección: {detections[-1]}", file=sys.stderr, flush=True)

        # Conexión a BD
        conn = get_db_connection()
        cur = conn.cursor()

        # Insertar detecciones
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

        # Actualizar puntuación usuario
        if user_id != "none":
            cur.execute('SELECT score FROM "user" WHERE id_user = %s', (user_id,))
            result = cur.fetchone()
            current_score = result[0] if result else 0
            new_score = current_score + total_points
            cur.execute('UPDATE "user" SET score = %s WHERE id_user = %s', (new_score, user_id))
            print(f"[INFO] Usuario {user_id} score actualizado: {current_score} -> {new_score}", file=sys.stderr, flush=True)

        conn.commit()
        cur.close()
        conn.close()
        print("[INFO] Base de datos actualizada y conexiones cerradas.", file=sys.stderr, flush=True)

        # Limpieza
        try:
            os.remove(video_file)
            os.remove(positions_file)
            shutil.rmtree(input_dir)
            print("[INFO] Archivos temporales eliminados correctamente.", file=sys.stderr, flush=True)
        except Exception:
            print("[WARNING] Error eliminando archivos temporales:", file=sys.stderr, flush=True)
            print(traceback.format_exc(), file=sys.stderr, flush=True)

        return '', 204

    except Exception:
        print("[ERROR] Excepción general en /process:", file=sys.stderr, flush=True)
        print(traceback.format_exc(), file=sys.stderr, flush=True)
        return jsonify({'error': 'Error interno del servidor'}), 500
