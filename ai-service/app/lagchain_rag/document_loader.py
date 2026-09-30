from pathlib import Path
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader
)
import os

load_dotenv()

files_path = os.getenv("BANK_POLICY_FILES_PATH")

if not files_path:
    raise ValueError("BANK_POLICY_FILES_PATH is not configured")


def load_documents() -> list[Document]:

    documents = []
    directory = Path(files_path)

    for path in directory.iterdir():

        if not path.is_file():
            continue

        extension = path.suffix.lower()

        if extension == ".txt":
            loader = TextLoader(str(path), encoding="utf-8")

        elif extension == ".pdf":
            loader = PyPDFLoader(str(path))

        elif extension == ".docx":
            loader = Docx2txtLoader(str(path))

        else:
            print(f"Skipping unsupported file: {path.name}")
            continue

        loaded_documents = loader.load()
        document_id = path.stem
        for document in loaded_documents:
            document.metadata["document_id"] = document_id
            document.metadata["document_version"] = "1"


        documents.extend(loaded_documents)

    return documents
