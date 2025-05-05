from config import DEVICE, OUTPUT_PATH, CONFIDENCE

########################################################################################################################

def predict_image(model, image_file):
    results = model.predict(
        source=image_file,
        save=True,
        save_txt=False,
        save_conf=False,
        device=DEVICE,
        project=OUTPUT_PATH,
        name=".",
        exist_ok=True,
        conf=CONFIDENCE
    )
    return results