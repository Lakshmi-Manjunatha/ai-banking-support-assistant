from fastapi import APIRouter
from app.model.chat import AskRequest, AskResponse
from app.service.llm_service import  ask_llm

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "service is up"}


@router.post("/ask", response_model= AskResponse)
def ask(request: AskRequest):
    llm_response = ask_llm(request.question)
    return AskResponse(
        answer=llm_response
    )