import pytest
from services.caption_service import CaptionService

class DummyService(CaptionService):
    def __init__(self): pass
    def _generate(self, *args, **kwargs): return "a cat sitting on grass"

def test_styles_are_supported():
    service = DummyService()
    assert "cat" in service.generate_caption(None, "Short").lower()
    assert "cat" in service.generate_caption(None, "Detailed").lower()
    assert "cat" in service.generate_caption(None, "Creative").lower()

def test_invalid_style():
    service = DummyService()
    with pytest.raises(ValueError): service.generate_caption(None, "Unknown")
