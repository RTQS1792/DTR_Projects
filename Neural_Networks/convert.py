"""
Author       : Hanqing Qi
Date         : 2023-08-09 17:52:59
LastEditors  : Hanqing Qi
LastEditTime : 2023-08-09 17:53:00
FilePath     : /balloons-in-highbay-fixed-settings-export/convert.py
Description  : 
"""

import json
from pathlib import Path
import shutil

# Configuration
FOLDER = "training/"
INPUT_FILE = FOLDER + "info.labels"
OUTPUT_DIR = Path("generated/")
WIDTH = 320.0
HEIGHT = 240.0

# Check if output directory exists or create it
if not OUTPUT_DIR.exists():
    OUTPUT_DIR.mkdir(parents=True)

# Load the JSON data from a file
try:
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: {INPUT_FILE} not found.")
    exit()

# Iterate through the 'files' list in the data
COUNTER = 0
for file in data.get("files", []):
    yolo_format_data = []
    path = Path(FOLDER + file["path"])

    if not path.exists():
        print(f"Warning: {path} does not exist. Skipping...")
        continue

    bounding_boxes = file.get("boundingBoxes", [])

    # Print the information
    print(f"Path: {path}")
    for box in bounding_boxes:
        original_label = box["label"]
        class_id = 0 if original_label == "g" else 1

        # Convert absolute bounding box dimensions to YOLO format
        x_center = (box["x"] + box["width"] / 2) / WIDTH
        y_center = (box["y"] + box["height"] / 2) / HEIGHT
        width = box["width"] / WIDTH
        height = box["height"] / HEIGHT

        yolo_format_data.append(f"{class_id} {x_center} {y_center} {width} {height}")

    newname = OUTPUT_DIR / f"{COUNTER}.jpg"  # New name for the file
    try:
        shutil.copy(path, newname)
    except PermissionError:
        print(f"Error: Permission denied to write to {newname}.")
        exit()

    # Save the YOLO format data to a text file if there are any bounding boxes
    if yolo_format_data:
        with open(OUTPUT_DIR / f"{COUNTER}.txt", "w") as f:
            f.write("\n".join(yolo_format_data))

    COUNTER += 1