from functions import *

if __name__ == "__main__":
    input_folder = "../data/processed_cv/images/train"
    output_folder_cv = "./results_cv"
    n_samples = 10

    process_images(input_folder, output_folder_cv, n_samples)
