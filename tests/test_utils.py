from PIL import Image
import pytest
from utils import validate_image, format_image_info


def test_validate_image_accepts_pil_image():
    image = Image.new("RGB", (100, 100))
    validate_image(image)


def test_validate_image_rejects_missing_image():
    with pytest.raises(ValueError):
        validate_image(None)


def test_format_image_info():
    image = Image.new("RGB", (1280, 720))
    assert "1,280 × 720 px" in format_image_info(image)
