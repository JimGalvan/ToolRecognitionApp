from fastai.vision.all import *
import numpy as np
from PIL import Image
import cv2
from pathlib import Path

def predict_and_extract(image_path, model_path='model.pkl', output_dir='predictions'):
    """
    Loads a FastAI segmentation model and predicts tool regions in an image.
    Saves overlay and extracted tools.
    """
    # === Load model ===
    learn = load_learner(model_path)

    # === Predict segmentation mask ===
    img = PILImage.create(image_path)
    pred_mask, _, _ = learn.predict(img)

    # ================================================================
    # --- Load COCO categories ---
    with open('tool_dataset/train/_annotations.coco.json') as f:
        coco_data = json.load(f)

    # Map: category_id → category_name
    id2cat = {cat['id']: cat['name'] for cat in coco_data['categories']}

    # --- Get predicted class IDs from mask ----
    mask_array = np.array(pred_mask)

    # Get unique class IDs
    unique_ids = np.unique(mask_array)

    # If you want to ignore background (optional, if you have one)
    # unique_ids = [i for i in unique_ids if i != 0]

    # --- Map IDs to names ---
    class_names = [id2cat.get(int(i), f"unknown_{i}") for i in unique_ids]

    print("Detected object types:", class_names)

    mask = np.array(pred_mask)
    unique, counts = np.unique(mask, return_counts=True)
    for u, c in zip(unique, counts):
        print(f"Class {u} → {c} pixels")

    print()

if __name__ == "__main__":
    # Example usage
    test_image = "tool_dataset/train/IMG_3217_jpeg.rf.93646f282555d3a9bc8ef796318c3a6f.jpg"
    predict_and_extract(test_image, model_path="model_local.pkl")

