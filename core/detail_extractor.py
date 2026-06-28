import os
import shutil
import fitz
from PIL import Image
import pytesseract

# ✅ FIXED: Cross-platform Tesseract detection instead of hardcoded Windows path
_tesseract = shutil.which("tesseract")
if _tesseract:
    pytesseract.pytesseract.tesseract_cmd = _tesseract
else:
    # Fallback for Windows if not on PATH
    _win_default = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(_win_default):
        pytesseract.pytesseract.tesseract_cmd = _win_default


def extract_text(file):
    ext = os.path.splitext(file)[1].lower()
    if ext == ".pdf":
        doc = fitz.open(file)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    elif ext in [".png", ".jpg", ".jpeg"]:
        img = Image.open(file)
        text = pytesseract.image_to_string(img)
        return text

    else:
        raise ValueError(f"Unsupported file type: {ext}")


