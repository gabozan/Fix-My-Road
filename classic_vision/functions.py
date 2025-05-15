import os
import cv2
import numpy as np
from skimage import segmentation, color

def preprocess_with_segmentation(img_bgr):
    img_smooth = cv2.pyrMeanShiftFiltering(img_bgr, sp=10, sr=8)
    segments = segmentation.quickshift(img_smooth, kernel_size=3, max_dist=6, ratio=0.5)
    return color.label2rgb(segments, img_bgr, kind='avg').astype(np.uint8)

def detect_and_paint(img_bgr, hsv_min, hsv_max, kernel, color):
    hsv  = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, hsv_min, hsv_max)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    road = np.zeros_like(mask)
    if cnts:
        cv2.fillPoly(road, [max(cnts, key=cv2.contourArea)], 255)
    painted = img_bgr.copy()
    painted[road == 255] = color
    return painted, road

def detect_crack_in_road_region(original_img, road_mask):
    # Aplicar la máscara de carretera
    masked = cv2.bitwise_and(original_img, original_img, mask=road_mask)

    # Eliminar zonas blancas y amarillas (marcas viales)
    hsv = cv2.cvtColor(masked, cv2.COLOR_BGR2HSV)
    mask_white = cv2.inRange(hsv, (0, 0, 200), (180, 50, 255))
    mask_yellow = cv2.inRange(hsv, (15, 50, 50), (35, 255, 255))
    mask_ignore = cv2.bitwise_or(mask_white, mask_yellow)
    mask_valid = cv2.bitwise_not(mask_ignore)

    gray_cleaned = cv2.bitwise_and(cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY), mask_valid)
    blurred = cv2.GaussianBlur(gray_cleaned, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    cnts, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    crack_boxed = original_img.copy()

    if cnts:
        largest = max(cnts, key=cv2.contourArea)
        if cv2.contourArea(largest) > 30:  # filtro de ruido mínimo
            x, y, w, h = cv2.boundingRect(largest)
            cv2.rectangle(crack_boxed, (x, y), (x + w, y + h), (0, 0, 255), 2)

    return crack_boxed

def process_images(input_dir, output_dir, n_samples):
    os.makedirs(output_dir, exist_ok=True)

    jpg_files = sorted(f for f in os.listdir(input_dir) if f.lower().endswith(".jpg"))
    sample_files = jpg_files[:min(n_samples, len(jpg_files))]

    hsv_min = np.array([0, 0, 95], dtype=np.uint8)
    hsv_max = np.array([40, 100, 200], dtype=np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    road_color = (0, 255, 0)

    for fname in sample_files:
        path = os.path.join(input_dir, fname)
        img = cv2.imread(path)
        img_seg = preprocess_with_segmentation(img)

        painted_on_segmented, road_mask = detect_and_paint(img_seg, hsv_min, hsv_max, kernel, road_color)
        crack_annotated = detect_crack_in_road_region(img, road_mask)

        combined = np.hstack([img, painted_on_segmented, crack_annotated])
        out_name = os.path.splitext(fname)[0] + "_with_crack.jpg"
        cv2.imwrite(os.path.join(output_dir, out_name), combined)

# === Punto de entrada principal ===
if __name__ == "__main__":
    input_folder = "../data/processed_cv/images/train"
    output_folder_cv = "./results_cv"
    n_samples = 30

    process_images(input_folder, output_folder_cv, n_samples)
