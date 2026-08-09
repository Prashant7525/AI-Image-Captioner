from pathlib import Path
from PIL import Image
from config import MAX_IMAGE_SIZE_MB, SUPPORTED_FORMATS

def validate_image(image):
    if image is None:
        raise ValueError("Please upload an image first.")
    if not isinstance(image, Image.Image):
        raise ValueError("The uploaded file could not be read as an image.")
    if image.format and image.format.lower() not in SUPPORTED_FORMATS:
        raise ValueError("Unsupported image format. Use JPG, JPEG, PNG, or WEBP.")
    width, height = image.size
    if width <= 0 or height <= 0:
        raise ValueError("The image has invalid dimensions.")
    if width * height > 40_000_000:
        raise ValueError("Image is too large. Please use an image below 40 megapixels.")

def format_image_info(image):
    if image is None:
        return ""
    return f"{image.width:,} × {image.height:,} px · {image.mode}"
