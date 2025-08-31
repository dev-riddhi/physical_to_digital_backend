from PIL import Image
import pytesseract

# Path to tesseract binary (only needed on Windows if not in PATH)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Open an image
img = Image.open("/home/riddhi/code/python_projects/teserractOCR/image.jpeg")

# Run OCR
text = pytesseract.image_to_string(img, lang="eng")
print("OCR Result:", text)
