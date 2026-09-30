import inspect
import os

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_postgres import PGEngine, PGVectorStore

from app.lagchain_rag import embedding

load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is not configured")

embedding_dimension = os.getenv("EMBEDDING_DIMENSION")

if not embedding_dimension:
    raise ValueError("EMBEDDING_DIMENSION is not configured")

table_name = os.getenv("DOC_CHUNK_TABLE_NAME")

if not table_name:
    raise ValueError("DOC_CHUNK_TABLE_NAME is not configured")

engine = PGEngine.from_connection_string(url=database_url)

embeddings = embedding.embeddings

#engine.init_vectorstore_table(table_name=table_name, vector_size=int(embedding_dimension))

vector_store = PGVectorStore.create_sync(engine=engine,
                                         table_name=table_name,
                                         embedding_service=embeddings)


def add_documents(chunks: list[Document]):
    ids = [
        chunk.metadata["chunk_id"]
        for chunk in chunks
    ]
    print("Executing the db insert")
    vector_store.add_documents(documents=chunks, ids=ids)
