from backend.pdf_loader import extract_text_from_pdf

pdf_path = "data/uploads/cnn_rnn_sample.pdf"

text = extract_text_from_pdf(pdf_path)

print(text[:2000])