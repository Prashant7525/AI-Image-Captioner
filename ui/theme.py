"""
ui/theme.py

Professional visual theme for the AI Image Captioner.
"""

import gradio as gr


def create_theme():
    """
    Create the application theme.
    """

    return gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        font=[
            gr.themes.GoogleFont("Inter"),
            "Arial",
            "sans-serif",
        ],
        font_mono=[
            "Consolas",
            "monospace",
        ],
    ).set(
        body_background_fill="#eef4ff",
        body_background_fill_dark="#111827",

        block_background_fill="#ffffff",
        block_background_fill_dark="#1f2937",

        block_border_width="0px",
        block_shadow="0 8px 25px rgba(0, 0, 0, 0.08)",
        block_radius="18px",

        button_primary_background_fill="#2563eb",
        button_primary_background_fill_hover="#1d4ed8",
        button_primary_text_color="#ffffff",

        input_background_fill="#ffffff",
        input_background_fill_dark="#111827",

        input_border_width="1px",
        input_border_color="#dbe4f0",

        checkbox_background_color="#2563eb",
    )