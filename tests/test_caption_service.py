"""
tests/test_caption_service.py
"""

from services.caption_service import CaptionService


def main():

    service = CaptionService()

    image_path = "images/sample.jpg"

    caption = service.generate_caption(image_path)

    print("\n")

    print("=" * 60)
    print("GENERATED CAPTION")
    print("=" * 60)

    print(caption)

    print("=" * 60)


if __name__ == "__main__":
    main()