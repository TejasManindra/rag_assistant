from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

def create_chunks(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    return splitter.split_text(text)