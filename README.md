---
title: AI Image Captioner
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: gradio
app_file: app.py
python_version: 3.12
pinned: false
---

# 🤖 AI Image Captioner

A professional image captioning application powered by **Salesforce BLIP**.

## ✨ Features

- Short, Detailed, and Creative caption styles
- Image upload and clipboard support
- Image preview and dimensions
- Copy generated captions to clipboard
- Download captions as `.txt`
- Generate Again for alternate wording
- CPU/GPU support
- Friendly validation and error messages
- Logging and automated tests
- Responsive professional UI

## 🧠 How It Works

```text
Upload Image
     ↓
Choose Caption Style
     ↓
Image Preprocessing
     ↓
Salesforce BLIP
     ↓
Caption Generation
     ↓
Copy / Download / Regenerate
```

### Caption styles

- **Short** — concise image description.
- **Detailed** — longer description with richer wording.
- **Creative** — sampling-based generation for more varied wording.

## 🛠 Tech Stack

- Python
- PyTorch
- Hugging Face Transformers
- Salesforce BLIP
- Gradio
- Pillow
- Pytest

## 📁 Project Structure

```text
AI-Image-Captioner/
├── app.py
├── config.py
├── logger.py
├── utils.py
├── requirements.txt
├── LICENSE
├── core/
│   └── model_loader.py
├── services/
│   └── caption_service.py
├── ui/
│   ├── layout.py
│   └── events.py
├── styles/
│   └── custom.css
├── tests/
│   ├── test_caption_service.py
│   └── test_model_loader.py
├── images/
└── outputs/
```

## 🚀 Run Locally

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Then open the Gradio URL shown in the terminal.

## 🧪 Run Tests

```powershell
pytest -q
```

## ☁️ Deployment

The application is ready for deployment to a Gradio-compatible hosting platform such as Hugging Face Spaces.

## 👨‍💻 Author

**Prashant Kumar**

## 📄 License

MIT License — see `LICENSE`.
