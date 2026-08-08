"""
services/caption_service.py

Image Caption Generation Service
"""

from PIL import Image

from config import MAX_LENGTH, MIN_LENGTH, NUM_BEAMS
from core.model_loader import ModelLoader


class CaptionService:
    """
    Service responsible for generating captions from images.
    """

    def __init__(self):
        loader = ModelLoader()

        self.processor = loader.get_processor()
        self.model = loader.get_model()
        self.device = loader.get_device()

    def generate_caption(self, image_path):
        """
        Generate a caption for an image.
        """

        if not image_path:
            return "Please upload an image first."

        with Image.open(image_path) as image:
            image = image.convert("RGB")

            inputs = self.processor(
                images=image,
                return_tensors="pt"
            )

        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        output = self.model.generate(
            **inputs,
            max_length=MAX_LENGTH,
            min_length=MIN_LENGTH,
            num_beams=NUM_BEAMS
        )

        caption = self.processor.decode(
            output[0],
            skip_special_tokens=True
        )

        return caption.strip()