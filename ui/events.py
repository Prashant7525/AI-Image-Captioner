from datetime import datetime
from pathlib import Path

from utils import validate_image

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_caption(image, style, caption_service):
    validate_image(image)
    caption = caption_service.generate_caption(image, style)
    download_path = save_caption(caption)
    return caption, f"✓ {style} caption generated successfully.", download_path


def save_caption(caption):
    if not caption or not caption.strip():
        return None
    filename = datetime.now().strftime("caption_%Y%m%d_%H%M%S.txt")
    path = OUTPUT_DIR / filename
    path.write_text(caption.strip() + "\n", encoding="utf-8")
    return str(path)
