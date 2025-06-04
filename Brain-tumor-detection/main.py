import os
from datasets import load_dataset
from ultralytics import YOLO
from PIL import Image
import tkinter as tk
from tkinter import messagebox
from ui import start_ui

# Hardcoded descriptions for common tumor types.
tumor_info = {
    "glioma": "Gliomas are brain tumors originating from glial cells. They vary in aggressiveness and require specialized treatment.",
    "meningioma": "Meningiomas arise from the meninges and are usually benign but can sometimes be aggressive.",
    "pituitary": "Pituitary tumors develop in the pituitary gland; treatment often involves hormonal therapy or surgical resection."
}

# Load the dataset globally
print("Loading dataset...")
ds = load_dataset("mmenendezg/brain-tumor-object-detection")

# Load the pre-trained YOLO model (ensure brain_tumor_detection.pt is in the working directory)
model_path = "brain_tumor_detection.pt"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file '{model_path}' not found. Please ensure it exists.")
print("Loading YOLO model...")
model = YOLO(model_path)

def run_detection(tumor_type: str):
    """
    Searches the dataset for an image with the specified tumor type,
    runs the YOLO model detection, and returns the path to the image and combined info.
    """
    tumor_type = tumor_type.lower().strip()
    info = tumor_info.get(tumor_type, f"No extra info available for '{tumor_type}'.")
    
    # Find a sample containing the tumor type
    sample = None
    for example in ds["train"]:
        anns = example.get("annotations", [])
        if any(ann.get("label", "").lower() == tumor_type for ann in anns):
            sample = example
            break
    if sample is None:
        return None, f"No images found with tumor type '{tumor_type}'."
    
    # Save the image to a temporary file
    image = sample["image"]
    temp_image_path = "temp_tumor.jpg"
    image.save(temp_image_path)
    
    # Run object detection on the image
    results = model.predict(source=temp_image_path, save=False)
    result_str = str(results)
    
    combined_info = info + "\n\nDetection Results:\n" + result_str
    return temp_image_path, combined_info

if __name__ == "__main__":
    start_ui(run_detection)