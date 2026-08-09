"""
tests/test_model_loader.py

Tests the ModelLoader singleton.
"""

from core.model_loader import ModelLoader


def main():

    loader = ModelLoader()

    print("\n")

    print("=" * 60)

    print("MODEL LOADER TEST")

    print("=" * 60)

    print()

    print("Processor :", type(loader.get_processor()).__name__)

    print("Model     :", type(loader.get_model()).__name__)

    print("Device    :", loader.get_device())

    print()

    print("=" * 60)


if __name__ == "__main__":
    main()