"""
ui/layout.py

Basic Gradio interface for the AI Image Captioner.
"""

import gradio as gr


def create_ui(caption_service):

    with gr.Blocks() as demo:

        gr.Markdown(
            """
            # 🤖 AI Image Captioner

            Upload an image and generate a natural language caption
            using **Salesforce BLIP**.
            """
        )

        with gr.Row():

            with gr.Column():

                image_input = gr.Image(
                    label="Upload Image",
                    type="filepath"
                )

                generate_button = gr.Button(
                    "🚀 Generate Caption"
                )

            with gr.Column():

                caption_output = gr.Textbox(
                    label="Generated Caption",
                    placeholder="Your generated caption will appear here...",
                    lines=5
                )

        generate_button.click(
            fn=caption_service.generate_caption,
            inputs=image_input,
            outputs=caption_output
        )

    return demo