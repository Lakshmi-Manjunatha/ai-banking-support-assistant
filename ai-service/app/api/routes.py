from fastapi import APIRouter
from app.model.chat import AskRequest, AskResponse
from app.service.ask_service import retrieve_answer

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "service is up"}


@router.post("/ask", response_model= AskResponse)
def ask(request: AskRequest):
    llm_response = retrieve_answer(request.question)
    return AskResponse(
        answer=llm_response
    )