import pytesseract
from PIL import Image
from paddleocr import PaddleOCR


class OcrModel:

    def tesseract_ocr(self, file_path: str):
        image = Image.open(file_path)
        return pytesseract.image_to_string(image=image, lang="eng")

    def paddle_ocr(self, image_path: str):

        if image_path is None:
            return "No image uploaded."

        try:

            ocr = PaddleOCR(use_angle_cls=True, lang="en")

            # Run OCR
            result = ocr.predict(image_path)

            # Check if result is not empty and has 'rec_texts'
            if result and isinstance(result, list) and "rec_texts" in result[0]:
                extracted_texts = result[0]["rec_texts"]
                return (
                    "\n".join(extracted_texts)
                    if extracted_texts
                    else "No text detected."
                )
            else:
                return "No text detected or unexpected result format."

        except Exception as e:
            return f"Error occurred: {str(e)}"
