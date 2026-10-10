import logging

from fastapi import APIRouter
from app.model.chat import AskRequest, AskResponse
from app.service.ask_service import retrieve_answer

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
def health():
    logger.info("Health check requested")
    return {"status": "service is up"}


@router.post("/ask", response_model= AskResponse)
def ask(request: AskRequest):
    logger.info("Ask request received: question_length=%s", len(request.question))
    llm_response = retrieve_answer(request.question)
    logger.info("Ask request completed")
    return AskResponse(
        answer=llm_response
    )
