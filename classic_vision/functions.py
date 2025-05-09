import random
import os
import cv2
import numpy as np

import cv2
import numpy as np
from skimage import segmentation, color

def estabilizar_luminosidad_hls(img_bgr, lum=0.25, sat=0):
    img_hls = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HLS)
    h, l, s = cv2.split(img_hls)

    # Corrección suave de la luminosidad (20% hacia 128)
    delta_l = cv2.subtract(128, l)
    l_corr = cv2.addWeighted(l, 1.0, delta_l, lum, 0)

    # Aumento sutil de saturación (15%), sin exceder 255
    s_corr = cv2.addWeighted(s, 1.0, s, sat, 0)
    s_corr = np.clip(s_corr, 0, 255).astype(np.uint8)

    # Proteger zonas blancas de cambios
    mask_whites = (l > 220) & (s < 30)
    l_corr[mask_whites] = l[mask_whites]
    s_corr[mask_whites] = s[mask_whites]

    img_hls_corr = cv2.merge([h, l_corr, s_corr])
    return cv2.cvtColor(img_hls_corr, cv2.COLOR_HLS2BGR)

def seg_and_pyr_mean_shift(img_bgr):
    # 1) Suavizado ligero
    img_smooth = cv2.pyrMeanShiftFiltering(img_bgr, sp=16, sr=10)
    # 2) Segmentación quickshift en superpíxeles pequeños
    segments = segmentation.quickshift(img_smooth, kernel_size=1, max_dist=3, ratio=0.2)
    # 3) Reconstruir imagen “promediada” por segmentos (opcional)
    segmented = color.label2rgb(segments, img_bgr, kind='avg')
    return segmented

def detect_and_paint(img_bgr):
    hsv_min = np.array([0, 0, 50], dtype=np.uint8)
    hsv_max = np.array([180, 50, 180], dtype=np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    color = (0, 255, 0)  # Verde

    # Estabilizar luminosidad
    img_bgr = estabilizar_luminosidad_hls(img_bgr)

    # Aplicar PyrMeanShift y QuickShift para segmentar
    img_bgr = seg_and_pyr_mean_shift(img_bgr)

    # Convertir imagen segmentada a HSV para detección
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, hsv_min, hsv_max)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Encontrar contornos y crear la máscara para la carretera
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    road = np.zeros_like(mask)
    if cnts:
        cv2.fillPoly(road, [max(cnts, key=cv2.contourArea)], 255)

    result = img_bgr.copy()
    result[road == 255] = color
    return result

def stack_side_by_side(img_left, img_right):
    h1, w1 = img_left.shape[:2]
    h2, w2 = img_right.shape[:2]
    if h1 != h2:
        scale = h1 / h2
        img_right = cv2.resize(img_right, (int(w2 * scale), h1), interpolation=cv2.INTER_AREA)
    return np.hstack([img_left, img_right])

def process_images(input_dir, output_dir, n_samples):
    os.makedirs(output_dir, exist_ok=True)
    jpg_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".jpg")]
    random.shuffle(jpg_files)
    sample_files = jpg_files[:min(n_samples, len(jpg_files))]

    for fname in sample_files:
        path = os.path.join(input_dir, fname)
        img = cv2.imread(path)
        after = detect_and_paint(img)
        combo = stack_side_by_side(img, after)
        out_name = os.path.splitext(fname)[0] + "_before_after.jpg"
        cv2.imwrite(os.path.join(output_dir, out_name), combo)
