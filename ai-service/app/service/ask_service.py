from langchain_core.documents import Document

from app.db.models.document_chunk import DocumentChunk
from app.lagchain_rag.retriever import retrieve_documents
from app.rag.embedding_service import embedding_content
from app.db.repository.document_chunk_repository import retrieve_similar_chunks
from app.service.llm_service import ask_llm


def retrieve_context(document_chunks: list[DocumentChunk], documents : list[Document]) -> str :

    context = ""

    if  document_chunks :
        context = "\n\n".join(
        chunk.content for chunk in document_chunks)

    if documents :
        context = "\n\n".join(
            document.page_content for document in documents)

    return context


def generate_prompt(question : str, document_chunks : list[DocumentChunk],
                    documents : list[Document]) -> str:

    context = retrieve_context(document_chunks, documents)

    prompt = f""" You are a banking support assistant. Answer using only the provided context.
    If the context does not contain the answer, say you do not have enough information.
    Context:
    {context}
    Question:
    {question}"""

    return prompt



def retrieve_answer(question: str) -> str:
    return retrieve_with_langchain(question)


def retrieve_without_langchain(question: str)-> str:
    question_embeddings = embedding_content(question)
    document_chunks = retrieve_similar_chunks(question_embeddings)
    prompt = generate_prompt(question, document_chunks, None)
    response = ask_llm(prompt)
    return response


def retrieve_with_langchain(question: str) -> str:
    documents = retrieve_documents(question)
    prompt = generate_prompt(question,None ,documents)
    response = ask_llm(prompt)
    return response



