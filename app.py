import os

from core.model_loader import ModelLoader
from services.caption_service import CaptionService
from ui.layout import create_ui
from logger import get_logger


logger = get_logger(__name__)


def main():
    logger.info("Starting AI Image Captioner")

    loader = ModelLoader()
    service = CaptionService(loader)

    demo = create_ui(
        service,
        loader.get_device()
    )

    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )


if __name__ == "__main__":
    main()