"""
ui/layout.py

Professional Gradio interface for the AI Image Captioner.
"""

import gradio as gr

from ui.theme import create_theme


CSS = """
body {
    background: #eef4ff !important;
}

/* Main container */

.gradio-container {
    max-width: 1200px !important;
    margin: auto !important;
}

/* Header */

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #1f2937;
    margin-top: 10px;
    margin-bottom: 6px;
}

.sub-title {
    text-align: center;
    font-size: 17px;
    color: #64748b;
    margin-bottom: 25px;
}

/* Cards */

.card {
    background: white;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
}

/* Caption */

.caption-output textarea {
    font-size: 18px !important;
    line-height: 1.7 !important;
}

/* Buttons */

button {
    border-radius: 12px !important;
    font-size: 17px !important;
    font-weight: 700 !important;
}

/* Generate button */

.generate-button {
    margin-top: 12px;
}

/* Footer */

.footer {
    text-align: center;
    color: #64748b;
    padding: 20px;
    font-size: 14px;
}

/* Images */

img {
    border-radius: 15px;
}

/* Hide default Gradio footer */

footer {
    visibility: hidden;
}
"""


def create_ui(caption_service):

    theme = create_theme()

    with gr.Blocks(
        theme=theme,
        css=CSS,
        title="AI Image Captioner",
    ) as demo:

        # --------------------------------------------------
        # Header
        # --------------------------------------------------

        gr.HTML(
            """
            <div class="main-title">
                🤖 AI Image Captioner
            </div>

            <div class="sub-title">
                Generate natural language captions using
                <strong>Salesforce BLIP</strong>
            </div>
            """
        )

        # --------------------------------------------------
        # Main application
        # --------------------------------------------------

        with gr.Row():

            # ----------------------------------------------
            # Left side
            # ----------------------------------------------

            with gr.Column(scale=1):

                with gr.Group(elem_classes="card"):

                    image_input = gr.Image(
                        label="🖼️ Upload Image",
                        type="filepath",
                    )

                    generate_button = gr.Button(
                        "🚀 Generate Caption",
                        variant="primary",
                        elem_classes="generate-button",
                    )

            # ----------------------------------------------
            # Right side
            # ----------------------------------------------

            with gr.Column(scale=1):

                with gr.Group(elem_classes="card"):

                    caption_output = gr.Textbox(
                        label="✨ Generated Caption",
                        placeholder=(
                            "Your generated caption "
                            "will appear here..."
                        ),
                        lines=6,
                        elem_classes="caption-output",
                    )

        # --------------------------------------------------
        # Footer
        # --------------------------------------------------

        gr.HTML(
            """
            <div class="footer">
                Made with ❤️ using
                <strong>Python</strong> ·
                <strong>Gradio</strong> ·
                <strong>Hugging Face</strong> ·
                <strong>Salesforce BLIP</strong>
            </div>
            """
        )

        # --------------------------------------------------
        # Event
        # --------------------------------------------------

        generate_button.click(
            fn=caption_service.generate_caption,
            inputs=image_input,
            outputs=caption_output,
        )

    return demo