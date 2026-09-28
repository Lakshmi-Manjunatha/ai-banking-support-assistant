This module is the AI/RAG service for the AI Banking Support Assistant portfolio project.
It is built with Python + FastAPI and currently implements a
Retrieval-Augmented Generation (RAG) flow manually, without LangChain

The service accepts a natural-language banking support question such as:

`Example : Why might my transaction be declined?`

This service Instead of sending only that question to the LLM, the service:
1. Converts the question into an embedding.
2. Searches PostgreSQL/pgvector for semantically similar banking-policy
   chunks.
3. Retrieves the most relevant original text. (cosine-distance search)
4. Combines the retrieved context with the user's question.
5. Sends that prompt to Gemini.
6. Returns the generated answer through the FastAPI /ask endpoint.


FLOW 1 — happens when documents are loaded

`Document
→ Chunk
→ Embed
→ Store`

FLOW 2 — happens when user asks a question

`Question
→ Embed
→ Search
→ Retrieve chunks
→ LLM
→ Answer`

#### **Technology Stack**
- Python --- AI service implementation
- FastAPI --- REST API framework
- Uvicorn --- ASGI application server
- Pydantic --- request/response models
- Google Gen AI SDK --- Gemini LLM and embedding API access
- Gemini --- answer generation
- Gemini Embeddings --- semantic vector generation
- PostgreSQL --- persistent document/chunk storage
- pgvector --- vector storage and similarity search inside
  PostgreSQL
- SQLAlchemy --- ORM and database access
- Alembic --- database schema migrations
- python-dotenv --- local environment-variable loading


### **To run this application locally :**

`run : uvicorn app.main:app --reload`


#### Test link :

`http://127.0.0.1:8000/docs`
