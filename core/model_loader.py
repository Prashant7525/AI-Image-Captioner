import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from config import MODEL_NAME

class ModelLoader:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = BlipProcessor.from_pretrained(MODEL_NAME)
        self.model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME)
        self.model.to(self.device)
        self.model.eval()

    def get_processor(self):
        return self.processor

    def get_model(self):
        return self.model

    def get_device(self):
        return self.device
