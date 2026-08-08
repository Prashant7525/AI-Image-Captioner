"""
core/model_loader.py

Responsible for loading the BLIP processor and model.
"""

import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

from config import MODEL_NAME


class ModelLoader:
    """
    Loads and provides access to the BLIP model.
    """

    def __init__(self):
        print("=" * 60)
        print("Initializing BLIP Model...")
        print("=" * 60)

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        print(f"Using Device: {self.device}")
        print("Loading Processor...")

        self.processor = BlipProcessor.from_pretrained(MODEL_NAME)

        print("Processor Loaded Successfully.")
        print("Loading BLIP Model...")

        self.model = BlipForConditionalGeneration.from_pretrained(
            MODEL_NAME
        )

        self.model.to(self.device)
        self.model.eval()

        print("BLIP Model Loaded Successfully.")
        print("=" * 60)

    def get_processor(self):
        return self.processor

    def get_model(self):
        return self.model

    def get_device(self):
        return self.device