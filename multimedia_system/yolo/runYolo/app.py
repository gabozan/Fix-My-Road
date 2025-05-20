import os
import tempfile
from flask import Flask, request, jsonify
from PIL import Image, ImageDraw
from google.cloud import storage
from google.cloud.sql.connector import Connector, IPTypes
import traceback
from ultralytics import YOLO

app = Flask(__name__)
gcs = storage.Client()

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "theRoadFixer.pt")
model = YOLO(MODEL_PATH)

BUCKET_NAME = os.environ.get('BUCKET_NAME', 'fixmyroad-videos')
DAMAGE_TYPES = [None, "longitudinal", "transversal", "cocodrilo", "bache"]
DAMAGE_POINTS = {
    "longitudinal": 10,
    "transversal": 10,
    "cocodrilo": 15,
    "bache": 25
}

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

@app.route('/process', methods=['POST'])
def process_video():
    try:
        data = request.get_json()
        src_name = data['name']
        is_anonymous = 'userId' not in data
        user_id = data.get('userId', 'anonymous')
        video_id = os.path.splitext(os.path.basename(src_name))[0]

        detections = []
        num_frames = 10

        for i in range(num_frames):
            # DETECCION DE DAÑO
            damage = random.choices(DAMAGE_TYPES, weights=[0.6, 0.2, 0.15, 0.05])[0]
            if damage:
                img = Image.new('RGB', (640, 480), color=(30, 30, 30))
                draw = ImageDraw.Draw(img)
                draw.text((50, 50), f"{damage.upper()} (frame {i})", fill=(255, 200, 0))
                tmp = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
                img.save(tmp, format='JPEG')
                tmp.close()

                dest = f"detections/{user_id}/{video_id}/{i}_{damage}.jpg"
                blob = gcs.bucket(BUCKET_NAME).blob(dest)
                blob.upload_from_filename(tmp.name, content_type='image/jpeg')
                detections.append({'frame': i, 'damage': damage, 'path': dest})
                os.remove(tmp.name)

        total_points = 0
        user_db_id = None

        conn = get_db_connection()
        cur = conn.cursor()

        if not is_anonymous:
            cur.execute('SELECT id_user, score FROM "user" WHERE name = %s', (user_id,))
            user = cur.fetchone()
            if user:
                user_db_id, current_score = user
            else:
                cur.execute('''
                    INSERT INTO "user" (name, email, password, score)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id_user
                ''', (user_id, f"{user_id}@fake.com", "default_pass", 0))
                user_db_id = cur.fetchone()[0]
                current_score = 0
        else:
            user_db_id = None
            current_score = 0

        for det in detections:
            points = DAMAGE_POINTS.get(det["damage"], 0)
            total_points += points
            cur.execute('''
                INSERT INTO reports (id_user, damage_type, image_url, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s)
            ''', (
                user_db_id, 
                det["damage"],
                det["path"],
                round(random.uniform(-90, 90), 6),
                round(random.uniform(-180, 180), 6)
            ))

        if not is_anonymous:
            cur.execute('UPDATE "user" SET score = %s WHERE id_user = %s',
                        (current_score + total_points, user_db_id))
            
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            'userId': user_id,
            'videoId': video_id,
            'detections': detections,
            'pointsEarned': total_points if not is_anonymous else 0
        }), 200

    except Exception as e:
        print("[ERROR]", traceback.format_exc())
        return jsonify({'error': str(e)}), 500
