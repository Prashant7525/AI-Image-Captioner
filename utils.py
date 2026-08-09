from pathlib import Path

from PIL import Image

from config import MAX_IMAGE_SIZE_MB, SUPPORTED_FORMATS


def format_image_info(image):
    if image is None:
        return "Upload an image to begin."

    try:
        image_format = image.format or "Unknown"
        width, height = image.size
        mode = image.mode

        return (
            f"**{width} × {height} px** · "
            f"**{mode}** · "
            f"**{image_format}**"
        )
    except Exception:
        return "Image information unavailable."


def validate_image(image):
    if image is None:
        raise ValueError("Please upload an image first.")

    if not isinstance(image, Image.Image):
        raise ValueError("Invalid image.")

    if image.format:
        image_format = image.format.upper()

        if image_format not in SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported image format: {image_format}"
            )

    return True


def save_caption(text):
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "caption.txt"
    output_file.write_text(
        text or "",
        encoding="utf-8",
    )

    return str(output_file)