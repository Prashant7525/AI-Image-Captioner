from utils import save_caption, validate_image


def generate_caption(image, style, caption_service):
    validate_image(image)

    text = caption_service.generate_caption(
        image=image,
        style=style,
    )

    download_path = save_caption(text)

    message = (
        f"✅ **{style} caption generated successfully.**"
    )

    return text, message, download_path