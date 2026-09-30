import hashlib
import uuid

from langchain_core.documents import Document


def generate_chunk_id(chunk: Document) -> str:

    document_id = chunk.metadata["document_id"]
    document_version = chunk.metadata["document_version"]
    chunk_index = chunk.metadata["chunk_index"]

    value = f"{document_id}:{document_version}:{chunk_index}"

    chunk_id = uuid.uuid5(uuid.NAMESPACE_URL, value)

    return str(chunk_id)