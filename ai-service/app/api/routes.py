import logging

from fastapi import APIRouter, Depends
from app.model.chat import AskRequest, AskResponse
from app.security.auth import require_rag_ask
from app.service.ask_service import retrieve_answer

router = APIRouter(prefix="/api/v1")
logger = logging.getLogger(__name__)


@router.get("/health")
def health():
    logger.info("Health check requested")
    return {"status": "service is up"}


@router.post("/ask", response_model= AskResponse)
def ask(request: AskRequest, dependencies = Depends(require_rag_ask)):
    logger.info("Ask request received: question_length=%s", len(request.question))
    response = retrieve_answer(request.question)
    logger.info("Ask request completed")
    return AskResponse(
        answer=response
    )
