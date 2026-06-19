from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

def get_embeddings(texts):

    return model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    ).tolist()