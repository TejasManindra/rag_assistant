from backend.embeddings import get_embeddings
from backend.vector_store import search

def retrieve(query):

    query_embedding = get_embeddings(
        [query]
    )[0]

    return search(
        query_embedding,
        n_results=3
    )