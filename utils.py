"""
utils.py
"""

import csv
import json
import os
import time
from PIL import Image

caption_history = []


def save_caption(caption):
    caption_history.append(caption)


def get_history():
    return caption_history


def clear_history():
    caption_history.clear()


def export_caption(caption):

    os.makedirs("outputs", exist_ok=True)

    filepath = "outputs/caption.txt"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(caption)

    return filepath


def export_json():

    os.makedirs("outputs", exist_ok=True)

    filepath = "outputs/history.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(caption_history, f, indent=4)

    return filepath


def export_csv():

    os.makedirs("outputs", exist_ok=True)

    filepath = "outputs/history.csv"

    with open(filepath, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow(["Caption"])

        for caption in caption_history:
            writer.writerow([caption])

    return filepath


def get_image_info(image_path):

    image = Image.open(image_path)

    width, height = image.size

    return {
        "Resolution": f"{width} x {height}",
        "File Size": f"{round(os.path.getsize(image_path)/1024,2)} KB"
    }


def start_timer():
    return time.time()


def stop_timer(start):
    return round(time.time()-start,2)