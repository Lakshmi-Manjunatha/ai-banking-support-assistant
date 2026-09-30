import os
from collections import defaultdict

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

chunk_size = os.getenv("CHUNK_SIZE")

if not chunk_size:
    raise ValueError("chunk_size is not configured")

chunk_overlap = os.getenv("CHUNK_OVERLAP")

if not chunk_overlap:
    raise ValueError("chunk_overlap is not configured")


def chunk_documents(documents: list[Document]) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = int(chunk_size),
                                                   chunk_overlap = int(chunk_overlap))

    chunks = text_splitter.split_documents(documents)

    chunk_counters = defaultdict(int)

    for chunk in chunks:
        document_id = chunk.metadata["document_id"]

        chunk.metadata["chunk_index"] = chunk_counters[document_id]

        chunk_counters[document_id] += 1
    return chunks
