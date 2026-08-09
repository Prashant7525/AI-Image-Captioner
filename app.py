import os

from dotenv import load_dotenv

from core.model_loader import ModelLoader
from services.caption_service import CaptionService
from ui.layout import create_ui
from logger import get_logger


load_dotenv()

logger = get_logger(__name__)


def main():
    logger.info("Starting AI Image Captioner")

    model_name = os.getenv(
        "HF_MODEL",
        "zai-org/GLM-4.5V",
    )

    logger.info(
        "Using Hugging Face model: %s",
        model_name,
    )

    loader = ModelLoader()
    service = CaptionService(loader)

    demo = create_ui(
        service,
        loader.get_device(),
    )

    port = int(
        os.getenv(
            "PORT",
            "7860",
        )
    )

    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False,
    )


if __name__ == "__main__":
    main()