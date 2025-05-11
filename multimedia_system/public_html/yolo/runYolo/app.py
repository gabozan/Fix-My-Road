import os
import random
import tempfile
from flask import Flask, request, jsonify
from PIL import Image, ImageDraw
from google.cloud import storage
from google.cloud.sql.connector import Connector, IPTypes
import traceback

app = Flask(__name__)
gcs = storage.Client()
connector = Connector(ip_type=IPTypes.PUBLIC)

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

@app.route('/process', methods=['POST'])
def process_video():
    try:
        data = request.get_json()
        bucket = gcs.bucket(data['bucket'])
        base_name = data['baseName'] #21_timestamp
        user_id = data['userId'] #21
        video_id = base_name.split('_')[1] #timestamp

        # Es ruta video_file, positions_file, estan descargados en una carpeta temporal. 
        # Tienes que abrirlos y leerlos.
        video_file, positions_file = (
            download_to_temp(bucket, f"videos/{base_name}_video.webm", ".webm"),
            download_to_temp(bucket, f"positions/{base_name}_positions.json", ".json")
        )

        # Se generan imagenes falsas, que representan aquellas que contienen grietas del video. 
        detections = []
        for i in range(10):
            damage = random.choice(["longitudinal", "grieta", "erosion"])
            img = Image.new('RGB', (640, 480), color=(30, 30, 30))
            draw = ImageDraw.Draw(img)
            draw.text((50, 50), f"{damage.upper()} (frame {i})", fill=(255, 200, 0))

            tmp_img = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
            img.save(tmp_img, format='JPEG')
            tmp_img.close()

            # Subir imagen con los bounding box de las grietas a google cloud storage. 
            # La variable i puede contener cualquier número.
            dest = f"detections/{user_id}/{video_id}/{i}.jpg"
            bucket.blob(dest).upload_from_filename(tmp_img.name, content_type='image/jpeg')
            os.remove(tmp_img.name)

           
        conn = get_db_connection()
        cur = conn.cursor()

        # Insertamos un daño aleatorio en la base de datos. Simplemente era para ver si se insertaba bien.
        # Aquí insertas todas las detecciones que hayas hecho.
        det = random.choice(detections)
        cur.execute('''
            INSERT INTO reports (id_user, damage_type, image_url, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s)
        ''', (
            user_id,
            det["damage"],
            det["path"],
            20,
            30
        ))

        # Bro lo siguiente es importante, que sino nos quedamos sin plata.
        conn.commit()
        cur.close()
        conn.close()

        # No se retorna nada
        return '',204

    except Exception as e:
        print("[ERROR]", traceback.format_exc())
        return jsonify({'error': str(e)}), 500
