"""
services/caption_service.py

Image Caption Generation Service
"""

import random
import re

import torch
from PIL import Image

from core.model_loader import ModelLoader


class CaptionService:
    """
    Service responsible for generating captions from images
    using Salesforce BLIP.
    """

    def __init__(self):
        loader = ModelLoader()

        self.processor = loader.get_processor()
        self.model = loader.get_model()
        self.device = loader.get_device()

    def _clean_caption(self, caption):
        """
        Clean and normalize a BLIP-generated caption.
        """

        if not caption:
            return ""

        caption = caption.strip()

        # Remove repeated consecutive words
        words = caption.split()
        cleaned_words = []

        for word in words:
            current = word.lower().strip(".,!?;:")

            if cleaned_words:
                previous = cleaned_words[-1].lower().strip(".,!?;:")

                if current == previous:
                    continue

            cleaned_words.append(word)

        caption = " ".join(cleaned_words)

        # Remove common unwanted prefixes
        prefixes = [
            "a photo of ",
            "an image of ",
            "a picture of ",
            "the image of ",
        ]

        lower_caption = caption.lower()

        for prefix in prefixes:
            if lower_caption.startswith(prefix):
                caption = caption[len(prefix):]
                break

        caption = caption.strip()

        # Remove extra spaces
        caption = re.sub(r"\s+", " ", caption)

        # Capitalize first character
        if caption:
            caption = caption[0].upper() + caption[1:]

        # Add punctuation
        if caption and caption[-1] not in ".!?":
            caption += "."

        return caption

    def _lowercase_first(self, text):
        """
        Lowercase only the first character.
        """

        if not text:
            return text

        return text[0].lower() + text[1:]

    def _generate_base_caption(self, image):
        """
        Generate the factual image caption using BLIP.
        """

        inputs = self.processor(
            images=image,
            return_tensors="pt"
        )

        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_length=30,
                num_beams=5,
                no_repeat_ngram_size=2,
                early_stopping=True
            )

        caption = self.processor.decode(
            output[0],
            skip_special_tokens=True
        )

        return self._clean_caption(caption)

    def _generate_detailed_caption(self, base_caption):
        """
        Generate a more descriptive version of the BLIP caption.

        The wording changes while staying grounded in the
        information detected by the model.
        """

        clean = base_caption.rstrip(".!?")
        text = self._lowercase_first(clean)

        templates = [
            (
                f"The image shows {text}. "
                f"The subject is clearly visible and stands out "
                f"against the surrounding scene."
            ),
            (
                f"The scene features {text}. "
                f"The main subject is clearly visible within "
                f"the surrounding environment."
            ),
            (
                f"Clearly visible in the image is {text}. "
                f"The subject is positioned prominently within "
                f"the scene."
            ),
            (
                f"This image captures {text}. "
                f"The surrounding setting provides context for "
                f"the main subject."
            ),
        ]

        return random.choice(templates)

    def _generate_creative_caption(self, base_caption):
        """
        Generate a more expressive caption while preserving
        the visual information detected by BLIP.
        """

        clean = base_caption.rstrip(".!?")
        text = self._lowercase_first(clean)

        templates = [
            (
                f"A charming moment unfolds with {text}, "
                f"bringing a lively touch to the scene."
            ),
            (
                f"The scene comes alive with {text}, "
                f"creating a memorable moment in the image."
            ),
            (
                f"A delightful moment is captured as {text}, "
                f"giving the scene its own character."
            ),
            (
                f"At the heart of this scene is {text}, "
                f"turning a simple moment into something special."
            ),
            (
                f"A beautiful moment takes shape with {text}, "
                f"giving the image a natural sense of charm."
            ),
        ]

        return random.choice(templates)

    def generate_caption(self, image_path, style="Short"):
        """
        Generate a caption for an image.

        Parameters
        ----------
        image_path : str
            Path to the uploaded image.

        style : str
            Caption style:
            - Short
            - Detailed
            - Creative

        Returns
        -------
        str
            Generated image caption.
        """

        if not image_path:
            return "Please upload an image first."

        style = style or "Short"

        try:
            with Image.open(image_path) as image:
                image = image.convert("RGB")

                # Generate factual caption
                base_caption = self._generate_base_caption(image)

                if not base_caption:
                    return "Unable to generate a caption for this image."

                # Apply selected style
                if style == "Short":
                    return base_caption

                if style == "Detailed":
                    return self._generate_detailed_caption(
                        base_caption
                    )

                if style == "Creative":
                    return self._generate_creative_caption(
                        base_caption
                    )

                # Fallback
                return base_caption

        except Exception as e:
            print(f"Caption generation error: {e}")

            return "Unable to generate a caption for this image."