import fitz
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

def extract_text(pdf_path):

    text = ""

    try:

        doc = fitz.open(pdf_path)

        for page in doc:

            page_text = page.get_text("text")

            if page_text.strip():

                text += page_text + "\n"

            else:

                pix = page.get_pixmap(
                    matrix=fitz.Matrix(3,3)
                )

                temp_img = "temp_page.png"

                pix.save(temp_img)

                img = Image.open(temp_img)

                ocr_text = pytesseract.image_to_string(
                    img
                )

                text += ocr_text + "\n"

        doc.close()

    except Exception as e:

        print(
            f"PDF Error: {e}"
        )

    return text