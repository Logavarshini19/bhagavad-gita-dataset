import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import pytesseract
from pdf2image import convert_from_path
from tqdm import tqdm
import json
import os

# 🛠️ Configure paths
pdf_path = "srimat_bhagavatgita_tamil.pdf"  # your Tamil scanned PDF
output_json = "tamil_verses.json"

# If poppler is NOT in system path, give full path here 👇
poppler_path = r"C:\Users\Varshini\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin"

# 🖼️ Convert PDF to images
print("📄 Converting PDF pages to images...")
images = convert_from_path(pdf_path, dpi=300, poppler_path=poppler_path)

# 🧠 Extract text with OCR
tamil_data = []
for i, img in enumerate(tqdm(images, desc="🕉️ Extracting Tamil OCR")):
    text = pytesseract.image_to_string(img, lang='tam+eng')
    tamil_data.append({
        "page": i + 1,
        "text": text.strip()
    })

# 💾 Save to JSON
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(tamil_data, f, ensure_ascii=False, indent=4)

print(f"✅ Extracted Tamil OCR from {len(images)} pages and saved to '{output_json}'")
