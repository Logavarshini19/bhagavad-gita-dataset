from pdf2image import convert_from_path
import pytesseract

# 1️⃣ Set this to your Tesseract install path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 2️⃣ Convert first page of the Tamil Gita PDF to image
images = convert_from_path("srimat_bhagavatgita_tamil.pdf", dpi=300, first_page=1, last_page=1)

# 3️⃣ Apply OCR in Tamil
text = pytesseract.image_to_string(images[0], lang='tam')

# 4️⃣ Print extracted Tamil text
print("📄 Tamil OCR Output:\n")
print(text)
