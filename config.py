import os

from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN", "").strip()

HF_MODEL = os.getenv(
    "HF_MODEL",
    "zai-org/GLM-4.5V",
).strip()

HF_PROVIDER = os.getenv(
    "HF_PROVIDER",
    "novita",
).strip()

MAX_IMAGE_SIZE_MB = 10

SUPPORTED_FORMATS = {
    "jpg",
    "jpeg",
    "png",
    "webp",
    "bmp",
}