"""
ui/events.py

Gradio event handlers for the AI Image Captioner.
"""

from services.caption_service import CaptionService

from utils import (
    save_caption,
    get_history,
    clear_history,
    export_caption,
    export_csv,
    export_json,
    get_image_info,
    start_timer,
    stop_timer,
)


# Load the model once when the application starts
caption_service = CaptionService()


def generate_caption(image, style):
    """
    Generate a caption for the uploaded image.
    """

    if image is None:
        return "", "", "", None

    start = start_timer()

    # Generate caption using selected style
    caption = caption_service.generate_caption(
        image,
        style
    )

    elapsed = stop_timer(start)

    # Save caption to history
    save_caption(caption)

    # Build caption history
    history = "\n\n".join(
        f"{i + 1}. {cap}"
        for i, cap in enumerate(get_history())
    )

    # Image information
    info = get_image_info(image)

    # Statistics
    stats = f"""
🖼 Resolution : {info['Resolution']}

📁 File Size : {info['File Size']}

⚡ Processing Time : {elapsed} sec

📝 Characters : {len(caption)}

🔤 Words : {len(caption.split())}

💻 Device : {caption_service.device}

🤖 Model : Salesforce BLIP

🎨 Style : {style}
"""

    # Export current caption
    file = export_caption(caption)

    return caption, history, stats, file


def clear_all():
    """
    Clear current caption and history.
    """

    clear_history()

    return "", "", "", None


def download_json():
    """
    Export caption history as JSON.
    """

    return export_json()


def download_csv():
    """
    Export caption history as CSV.
    """

    return export_csv()