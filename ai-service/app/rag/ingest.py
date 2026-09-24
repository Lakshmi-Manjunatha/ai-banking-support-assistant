import os
from dotenv import load_dotenv

from app.db.database import SessionLocal
from app.db.models.document_chunk import DocumentChunk
from app.db.repository.document_chunk_repository import save_embeddings
from app.rag import chunker, embedding_service

load_dotenv()

file_path = os.getenv("BANK_POLICY_FILE_PATH")


def load_documents(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text


if not file_path:
    raise ValueError(f"Given file path is not findable : {file_path}")

document_text = load_documents(file_path)

chunk_size = os.getenv("CHUNK_SIZE")

if not chunk_size:
    raise ValueError("chunk_size is not configured")

chunk_overlap = os.getenv("CHUNK_OVERLAP")

if not chunk_overlap:
    raise ValueError("chunk_overlap is not configured")

chunks = chunker.load_chunks(document_text, int(chunk_size), int(chunk_overlap))


document_chunks = []

for index, chunk in enumerate(chunks):
    embedding = embedding_service.embedding_content(chunk)
    document_chunk = DocumentChunk(source=file_path, chunk_index=index, content=chunk, embedding=embedding)
    document_chunks.append(document_chunk)

save_embeddings(document_chunks)


