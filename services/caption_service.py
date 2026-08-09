import re
from PIL import Image
import torch


class CaptionService:
    def __init__(self, model_loader):
        self.processor = model_loader.get_processor()
        self.model = model_loader.get_model()
        self.device = model_loader.get_device()

    def _generate(
        self,
        image,
        prompt=None,
        max_new_tokens=40,
        num_beams=5,
        do_sample=False,
        temperature=1.0,
        top_p=0.9,
    ):
        if image is None:
            raise ValueError("Please upload an image first.")
        if not isinstance(image, Image.Image):
            image = Image.open(image)
        image = image.convert("RGB")

        if prompt:
            inputs = self.processor(images=image, text=prompt, return_tensors="pt")
        else:
            inputs = self.processor(images=image, return_tensors="pt")

        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        generation_kwargs = {
            "max_new_tokens": max_new_tokens,
            "num_beams": num_beams,
            "do_sample": do_sample,
            "repetition_penalty": 1.12,
            "no_repeat_ngram_size": 3,
        }
        if do_sample:
            generation_kwargs.update({"temperature": temperature, "top_p": top_p})

        with torch.inference_mode():
            output = self.model.generate(**inputs, **generation_kwargs)

        text = self.processor.decode(output[0], skip_special_tokens=True).strip()
        return self._clean(text)

    def generate_caption(self, image, style="Short"):
        style = (style or "Short").strip().lower()

        if style == "short":
            return self._generate(
                image,
                max_new_tokens=18,
                num_beams=5,
            )

        if style == "detailed":
            caption = self._generate(
                image,
                prompt="a detailed description of",
                max_new_tokens=45,
                num_beams=6,
            )
            if len(caption.split()) < 8:
                caption = self._generate(
                    image,
                    max_new_tokens=40,
                    num_beams=6,
                )
            return caption

        if style == "creative":
            return self._generate(
                image,
                prompt="a creative description of",
                max_new_tokens=35,
                num_beams=1,
                do_sample=True,
                temperature=0.95,
                top_p=0.9,
            )

        raise ValueError("Caption style must be Short, Detailed, or Creative.")

    @staticmethod
    def _clean(text):
        text = re.sub(
            r"^(a|an|the)\s+(creative|detailed)\s+description of\s+",
            "",
            text,
            flags=re.IGNORECASE,
        )
        text = re.sub(
            r"^(a|an|the)\s+description of\s+",
            "",
            text,
            flags=re.IGNORECASE,
        )
        text = re.sub(r"\s+", " ", text).strip()
        if text and text[-1] not in ".!?":
            text += "."
        return text[:1].upper() + text[1:] if text else text
