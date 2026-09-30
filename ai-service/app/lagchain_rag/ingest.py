from langchain_core.documents import Document

from app.lagchain_rag.chunker import chunk_documents
from app.lagchain_rag.document_id import generate_chunk_id
from app.lagchain_rag.document_loader import load_documents
from app.lagchain_rag.store_vector import add_documents


def ingest_documents() -> list[Document]:
    documents = load_documents()
    chunks = chunk_documents(documents)
    for chunk in chunks :
        chunk.metadata["chunk_id"] = generate_chunk_id(chunk)

    add_documents(chunks)
    return chunks
