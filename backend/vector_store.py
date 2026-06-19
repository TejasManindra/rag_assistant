import chromadb

client = chromadb.PersistentClient(
    path="data/chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)

def clear_collection():

    global collection

    try:
        client.delete_collection("documents")
    except:
        pass

    collection = client.get_or_create_collection(
        name="documents"
    )

def store_chunks(chunks, embeddings):

    ids = [
        f"chunk_{i}"
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

def search(query_embedding, n_results=5):

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

def clear_collection():

    global collection

    try:
        client.delete_collection(
            "documents"
        )
    except:
        pass

    collection = client.get_or_create_collection(
        name="documents"
    )