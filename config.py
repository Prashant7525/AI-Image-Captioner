"""
config.py

Configuration for the basic AI Image Captioner.
"""

MODEL_NAME = "Salesforce/blip-image-captioning-base"

MAX_LENGTH = 50
MIN_LENGTH = 5
NUM_BEAMS = 5

DEVICE = "cuda"