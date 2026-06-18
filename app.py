from backend.pdf_loader import extract_text_from_pdf
from backend.chunker import create_chunks

pdf_path = "data/uploads/cnn_rnn_sample.pdf"

text = extract_text_from_pdf(pdf_path)

chunks = create_chunks(text)

print(f"Total Chunks: {len(chunks)}")

print(chunks[0])
