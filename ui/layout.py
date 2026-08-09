import os
import gradio as gr

from ui.events import generate_caption
from utils import format_image_info


def create_ui(caption_service, device):
    css = ""

    if os.path.exists("styles/custom.css"):
        with open("styles/custom.css", encoding="utf-8") as file:
            css = file.read()

    model_name = os.getenv(
        "HF_MODEL",
        "zai-org/GLM-4.5V",
    )

    with gr.Blocks(
        title="AI Image Captioner",
        css=css,
        theme=gr.themes.Soft(),
    ) as demo:

        gr.HTML(
            """
            <header class="hero">
                <h1>🤖 AI Image Captioner</h1>
                <p>
                    Transform images into natural-language descriptions
                    using <strong>Hugging Face Vision AI</strong>
                </p>
                <span class="status-badge">● AI Ready</span>
            </header>
            """
        )

        with gr.Row(elem_classes="info-row"):

            # =========================
            # IMAGE INPUT
            # =========================

            with gr.Column(
                scale=1,
                elem_classes="card",
            ):
                gr.Markdown("### 🖼️ Image Input")

                image = gr.Image(
                    type="pil",
                    sources=["upload", "clipboard"],
                    label="Upload Image",
                    elem_id="image_input",
                )

                image_info = gr.Markdown(
                    "Upload an image to begin.",
                    elem_id="image_info",
                )

                style = gr.Dropdown(
                    choices=[
                        "Short",
                        "Detailed",
                        "Creative",
                    ],
                    value="Short",
                    label="🎨 Caption Style",
                    elem_id="style_select",
                )

                with gr.Row():

                    generate = gr.Button(
                        "🚀 Generate Caption",
                        variant="primary",
                        elem_id="generate_btn",
                    )

                    clear = gr.Button(
                        "🗑 Clear",
                        elem_id="clear_btn",
                    )

                regenerate = gr.Button(
                    "↻ Generate Again",
                    visible=False,
                    elem_id="regenerate_btn",
                )

            # =========================
            # GENERATED CAPTION
            # =========================

            with gr.Column(
                scale=1,
                elem_classes="card",
            ):
                gr.Markdown("### ✨ Generated Caption")

                caption = gr.Textbox(
                    value="",
                    lines=8,
                    show_label=False,
                    placeholder="Your generated caption will appear here...",
                    elem_id="caption_output",
                )

                with gr.Row():

                    copy = gr.Button(
                        "📋 Copy",
                        elem_id="copy_btn",
                    )

                    download = gr.DownloadButton(
                        "⬇ Download",
                        visible=False,
                        elem_id="download_btn",
                    )

                status = gr.Markdown(
                    "",
                    elem_id="status",
                )

        # =========================
        # INFORMATION SECTION
        # =========================

        with gr.Row(elem_classes="info-row"):

            # HOW IT WORKS

            with gr.Column(
                elem_classes="info-card",
            ):
                gr.Markdown(
                    """
                    ### ⚡ How It Works

                    **1. Upload** → **2. Choose style** →
                    **3. Vision AI analyzes** → **4. Generate caption**

                    **Short** produces a concise description.

                    **Detailed** provides richer visual context.

                    **Creative** produces more engaging wording.
                    """
                )

            # MODEL INFORMATION

            with gr.Column(
                elem_classes="info-card",
            ):
                gr.Markdown(
                    f"""
                    ### ⚙️ Model Information

                    **Model:** `{model_name}`

                    **Runtime:** `Hugging Face Inference API`

                    **Framework:** `Hugging Face · Gradio`

                    **Inference:** `Remote API`
                    """
                )

        # =========================
        # FOOTER
        # =========================

        gr.HTML(
            """
            <footer class="app-footer">
                <div>
                    © 2026 Prashant Kumar · AI Image Captioner ·
                    Powered by Hugging Face Vision AI
                </div>
            </footer>
            """
        )

        # =========================
        # IMAGE INFORMATION
        # =========================

        image.change(
            lambda img: (
                format_image_info(img)
                if img
                else "Upload an image to begin."
            ),
            inputs=image,
            outputs=image_info,
        )

        # =========================
        # GENERATE FUNCTION
        # =========================

        def run(image_value, style_value):
            try:
                text, message, download_path = generate_caption(
                    image_value,
                    style_value,
                    caption_service,
                )

                return (
                    text,
                    message,
                    gr.Button(
                        value="↻ Generate Again",
                        visible=True,
                        interactive=True,
                    ),
                    gr.Button(
                        value="🚀 Generate Caption",
                        visible=True,
                        interactive=True,
                    ),
                    gr.DownloadButton(
                        value=download_path,
                        visible=True,
                    ),
                )

            except Exception as exc:

                return (
                    "",
                    f"⚠️ {exc}",
                    gr.Button(
                        visible=False,
                    ),
                    gr.Button(
                        value="🚀 Generate Caption",
                        visible=True,
                        interactive=True,
                    ),
                    gr.DownloadButton(
                        visible=False,
                    ),
                )

        # =========================
        # LOADING STATE
        # =========================

        def loading_state():

            return (
                gr.Button(
                    value="⏳ Generating...",
                    interactive=False,
                    visible=True,
                ),
                gr.Button(
                    value="⏳ Generating...",
                    interactive=False,
                    visible=True,
                ),
            )

        # =========================
        # GENERATE BUTTON
        # =========================

        generate.click(
            loading_state,
            outputs=[
                generate,
                regenerate,
            ],
        ).then(
            run,
            inputs=[
                image,
                style,
            ],
            outputs=[
                caption,
                status,
                regenerate,
                generate,
                download,
            ],
        )

        # =========================
        # REGENERATE BUTTON
        # =========================

        regenerate.click(
            loading_state,
            outputs=[
                generate,
                regenerate,
            ],
        ).then(
            run,
            inputs=[
                image,
                style,
            ],
            outputs=[
                caption,
                status,
                regenerate,
                generate,
                download,
            ],
        )

        # =========================
        # CLEAR BUTTON
        # =========================

        clear.click(
            lambda: (
                None,
                "Upload an image to begin.",
                "",
                "",
                gr.Button(
                    visible=False,
                ),
                gr.DownloadButton(
                    visible=False,
                ),
                gr.Button(
                    value="🚀 Generate Caption",
                    interactive=True,
                ),
            ),
            outputs=[
                image,
                image_info,
                caption,
                status,
                regenerate,
                download,
                generate,
            ],
        )

        # =========================
        # COPY BUTTON
        # =========================

        copy.click(
            None,
            js="""
            () => {
                const box =
                    document.querySelector(
                        '#caption_output textarea'
                    );

                const button =
                    document.querySelector(
                        '#copy_btn button'
                    );

                if (!box || !box.value.trim()) {
                    return;
                }

                navigator.clipboard.writeText(
                    box.value
                );

                if (button) {
                    const oldText =
                        button.innerText;

                    button.innerText =
                        '✓ Copied';

                    setTimeout(
                        () => {
                            button.innerText =
                                oldText;
                        },
                        1400
                    );
                }
            }
            """,
        )

    return demo