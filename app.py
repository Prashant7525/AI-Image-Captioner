"""
app.py

Entry point for the AI Image Captioner.
"""

from services.caption_service import CaptionService
from ui.layout import create_ui


def main():

    print("=" * 60)
    print("AI IMAGE CAPTIONER")
    print("=" * 60)

    caption_service = CaptionService()

    app = create_ui(caption_service)

    app.launch()


if __name__ == "__main__":
    main()