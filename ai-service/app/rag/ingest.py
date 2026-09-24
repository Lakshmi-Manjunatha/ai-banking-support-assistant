import os
from dotenv import load_dotenv

from app.rag import chunker, embedding_service

load_dotenv()

file_path = os.getenv("BANK_POLICY_FILE_PATH")

def load_documents(file_path : str) -> str:
    with open(file_path, "r",encoding="utf-8") as file:
        text = file.read()

    return text


if not file_path :
    raise ValueError(f"Given file path is not findable : {file_path}")

document_text = load_documents(file_path)


chunk_size = os.getenv("CHUNK_SIZE")

if not chunk_size :
    raise ValueError("chunk_size is not configured")

chunk_overlap = os.getenv("CHUNK_OVERLAP")

if not chunk_overlap :
    raise ValueError("chunk_overlap is not configured")


chunks = chunker.load_chunks(document_text, int(chunk_size), int(chunk_overlap))

for index, chunk in enumerate(chunks):
    embedding = embedding_service.embedding_content(chunk)
    print("Chunk:", index)
    print("Chunk text:", chunk)
    print("Embedding dimension:", len(embedding))
    print("First 5 values:", embedding[:5])
    print("-----------------------------")


