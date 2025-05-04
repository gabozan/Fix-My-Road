import random
import os
import cv2
import numpy as np

def detect_and_paint(img_bgr, hsv_min, hsv_max, kernel, color):
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, hsv_min, hsv_max)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    road = np.zeros_like(mask)
    if cnts:
        cv2.fillPoly(road, [max(cnts, key=cv2.contourArea)], 255)
    painted = img_bgr.copy()
    painted[road == 255] = color
    return painted

def stack_side_by_side(img_left, img_right):
    h1, w1 = img_left.shape[:2]
    h2, w2 = img_right.shape[:2]
    if h1 != h2:
        scale = h1 / h2
        img_right = cv2.resize(img_right, (int(w2 * scale), h1), interpolation=cv2.INTER_AREA)
    return np.hstack([img_left, img_right])

def process_images(input_dir, output_dir, n_samples, hsv_min, hsv_max, kernel, color):
    os.makedirs(output_dir, exist_ok=True)
    jpg_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".jpg")]
    random.shuffle(jpg_files)
    sample_files = jpg_files[:min(n_samples, len(jpg_files))]

    for fname in sample_files:
        path = os.path.join(input_dir, fname)
        img = cv2.imread(path)
        after = detect_and_paint(img, hsv_min, hsv_max, kernel, color)
        combo = stack_side_by_side(img, after)
        out_name = os.path.splitext(fname)[0] + "_before_after.jpg"
        cv2.imwrite(os.path.join(output_dir, out_name), combo)
