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
        min_new_tokens=5,
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
            inputs = self.processor(
                images=image,
                text=prompt,
                return_tensors="pt",
            )
        else:
            inputs = self.processor(
                images=image,
                return_tensors="pt",
            )

        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        generation_kwargs = {
            "max_new_tokens": max_new_tokens,
            "min_new_tokens": min_new_tokens,
            "num_beams": num_beams,
            "do_sample": do_sample,
            "repetition_penalty": 1.15,
            "no_repeat_ngram_size": 3,
            "length_penalty": 1.0,
            "early_stopping": True,
        }

        if do_sample:
            generation_kwargs.update(
                {
                    "temperature": temperature,
                    "top_p": top_p,
                }
            )

        with torch.inference_mode():
            output = self.model.generate(
                **inputs,
                **generation_kwargs,
            )

        text = self.processor.decode(
            output[0],
            skip_special_tokens=True,
        ).strip()

        return self._clean(text)

    def generate_caption(self, image, style="Short"):
        style = (style or "Short").strip().lower()

        if style == "short":
            return self._generate(
                image,
                max_new_tokens=20,
                min_new_tokens=5,
                num_beams=6,
                do_sample=False,
            )

        if style == "detailed":
            caption = self._generate(
                image,
                prompt="a detailed photo of",
                max_new_tokens=48,
                min_new_tokens=10,
                num_beams=7,
                do_sample=False,
            )

            if len(caption.split()) < 10:
                caption = self._generate(
                    image,
                    max_new_tokens=45,
                    min_new_tokens=8,
                    num_beams=7,
                    do_sample=False,
                )

            return self._refine_detailed(caption)

        if style == "creative":
            caption = self._generate(
                image,
                prompt="a natural caption for this image",
                max_new_tokens=38,
                min_new_tokens=7,
                num_beams=4,
                do_sample=True,
                temperature=0.85,
                top_p=0.92,
            )

            return self._refine_creative(caption)

        raise ValueError(
            "Caption style must be Short, Detailed, or Creative."
        )

    @staticmethod
    def _clean(text):
        if not text:
            return ""

        text = re.sub(
            r"^(a|an|the)\s+"
            r"(detailed|creative|natural)\s+"
            r"(description|caption)\s*(of|for)?\s*",
            "",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"^(this image|the image)\s+(shows|depicts)\s+",
            "",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"\b(a|an|the)\s+(photo|picture|image)\s+of\s+",
            "",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(r"\s+", " ", text).strip()

        text = re.sub(
            r"([.!?])\s*\1+",
            r"\1",
            text,
        )

        if text and text[-1] not in ".!?":
            text += "."

        return text[:1].upper() + text[1:] if text else text

    @staticmethod
    def _refine_detailed(caption):
        if not caption:
            return caption

        caption = caption.strip()

        if caption[-1] not in ".!?":
            caption += "."

        return caption

    @staticmethod
    def _refine_creative(caption):
        if not caption:
            return caption

        caption = caption.strip()

        caption = re.sub(
            r"^(a|an|the)\s+",
            "",
            caption,
            count=1,
            flags=re.IGNORECASE,
        )

        caption = re.sub(
            r"\bvery\s+very\b",
            "very",
            caption,
            flags=re.IGNORECASE,
        )

        if caption and caption[-1] not in ".!?":
            caption += "."

        return caption[:1].upper() + caption[1:]