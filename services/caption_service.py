import base64
import io
import re
import time

from PIL import Image
from huggingface_hub import InferenceClient

from config import HF_MODEL, HF_PROVIDER, HF_TOKEN


class CaptionService:
    def __init__(self, model_loader=None):
        if not HF_TOKEN:
            raise RuntimeError("HF_TOKEN is not configured.")

        self.model_name = HF_MODEL
        self.provider = HF_PROVIDER or "novita"

        self.client = InferenceClient(
            provider=self.provider,
            api_key=HF_TOKEN,
            timeout=120,
        )

    def generate_caption(self, image, style="Short"):
        if image is None:
            raise ValueError("Please upload an image first.")

        if not isinstance(image, Image.Image):
            image = Image.open(image)

        image = image.convert("RGB")

        style = (style or "Short").strip().lower()

        if style == "short":
            prompt = (
                "Describe this image in one concise natural sentence. "
                "Identify the main subject and what it is doing. "
                "Only describe what is visibly present."
            )
            max_tokens = 50
            temperature = 0.2

        elif style == "detailed":
            prompt = (
                "Describe this image in detail. Mention the main "
                "subjects, their actions, the environment, colors, "
                "and important visible details. Do not invent facts."
            )
            max_tokens = 100
            temperature = 0.2

        elif style == "creative":
            prompt = (
                "Write a natural and engaging caption for this image. "
                "Keep it visually accurate and concise. "
                "Do not invent information."
            )
            max_tokens = 70
            temperature = 0.7

        else:
            raise ValueError(
                "Caption style must be Short, Detailed, or Creative."
            )

        image_url = self._image_to_data_url(image)

        last_error = None

        for attempt in range(3):
            try:
                response = self.client.chat_completion(
                    model=self.model_name,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt,
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": image_url,
                                    },
                                },
                            ],
                        }
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature,
                    extra_body={
                        "chat_template_kwargs": {
                            "enable_thinking": False
                        }
                    },
                )

                text = self._extract_text(response)

                if text:
                    return self._clean(text)

                raise RuntimeError(
                    "The model returned an empty response."
                )

            except Exception as exc:
                last_error = exc

                if attempt < 2:
                    time.sleep(2 * (attempt + 1))

        raise RuntimeError(
            f"Hugging Face inference failed: {last_error}"
        )

    @staticmethod
    def _extract_text(response):
        if response is None:
            return ""

        try:
            choices = response.choices
        except Exception:
            return ""

        if not choices:
            return ""

        message = choices[0].message

        if message is None:
            return ""

        content = getattr(message, "content", None)

        if isinstance(content, str) and content.strip():
            return content.strip()

        if isinstance(content, list):
            parts = []

            for item in content:
                if isinstance(item, str):
                    parts.append(item)

                elif isinstance(item, dict):
                    value = item.get("text")
                    if value:
                        parts.append(str(value))

                else:
                    value = getattr(item, "text", None)
                    if value:
                        parts.append(str(value))

            result = " ".join(parts).strip()

            if result:
                return result

        reasoning = getattr(
            message,
            "reasoning_content",
            None,
        )

        if isinstance(reasoning, str) and reasoning.strip():
            return reasoning.strip()

        return ""

    @staticmethod
    def _image_to_data_url(image):
        image = image.copy()

        image.thumbnail(
            (1024, 1024),
            Image.Resampling.LANCZOS,
        )

        buffer = io.BytesIO()

        image.save(
            buffer,
            format="JPEG",
            quality=85,
            optimize=True,
        )

        encoded = base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")

        return f"data:image/jpeg;base64,{encoded}"

    @staticmethod
    def _clean(text):
        if not text:
            return ""

        text = str(text).strip()

        text = re.sub(
            r"<think>.*?</think>",
            "",
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )

        text = re.sub(
            r"^(assistant|caption)\s*:\s*",
            "",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        ).strip()

        text = re.sub(
            r"([.!?])\s*\1+",
            r"\1",
            text,
        )

        if text and text[-1] not in ".!?":
            text += "."

        return text[:1].upper() + text[1:]