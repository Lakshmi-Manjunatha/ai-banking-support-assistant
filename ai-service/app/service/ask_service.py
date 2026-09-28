from app.db.models.document_chunk import DocumentChunk
from app.rag.embedding_service import embedding_content
from app.db.repository.document_chunk_repository import retrieve_similar_chunks
from app.service.llm_service import ask_llm


def retrieve_context(document_chunks: list[DocumentChunk]) -> str :
    context = "\n\n".join(
        chunk.content for chunk in document_chunks
    )
    return context


def generate_prompt(question, document_chunks) -> str:

    context = retrieve_context(document_chunks)

    prompt = f""" You are a banking support assistant. Answer using only the provided context.
    If the context does not contain the answer, say you do not have enough information.
    Context:
    {context}
    Question:
    {question}"""

    return prompt



def retrieve_answer(question: str) -> str:
    question_embeddings = embedding_content(question)
    document_chunks = retrieve_similar_chunks(question_embeddings)
    prompt = generate_prompt(question, document_chunks)
    response = ask_llm(prompt)
    print(response)
    return response
