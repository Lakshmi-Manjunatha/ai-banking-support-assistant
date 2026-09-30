from langchain_core.documents import Document

from app.lagchain_rag.store_vector import vector_store


def retrieve_documents(question : str) -> list[Document]:
    return vector_store.similarity_search(query=question, k= 3)