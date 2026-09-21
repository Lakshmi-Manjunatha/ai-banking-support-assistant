from fastapi import APIRouter
from app.model.chat import AskRequest, AskResponse

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "service is up"}


@router.post("/ask", response_model= AskResponse)
def ask(request: AskRequest):
    return AskResponse(
        answer=f"You asked: {request.question}"
    )