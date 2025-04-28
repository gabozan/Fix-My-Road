from functions import *

if __name__ == "__main__":
    input_folder = "../data/processed_cv/train"
    output_folder_cv = "./results_cv"
    n_samples = 10

    hsv_min = np.array([0, 0, 30], dtype=np.uint8)
    hsv_max = np.array([180, 70, 220], dtype=np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    green = (0, 255, 0)

    process_images(input_folder, output_folder_cv, n_samples, hsv_min, hsv_max, kernel, green)