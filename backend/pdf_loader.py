import fitz

def extract_text(pdf_path):

    text = ""

    try:
        doc = fitz.open(pdf_path)

        for page in doc:
            text += page.get_text("text") + "\n"

        doc.close()

    except Exception as e:
        print(f"PDF Error: {e}")

    return text