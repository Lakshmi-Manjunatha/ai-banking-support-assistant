import logging
import os

from dotenv import load_dotenv
from langchain_core.documents import Document

from app.lagchain_rag.store_vector import vector_store

logger = logging.getLogger(__name__)

load_dotenv()

def get_config(default_value: int, env_key: str) -> int:
    value = os.getenv(env_key)

    if not value:
        logger.warning(
            "%s configuration value is missing. Default value is set: %s",
            env_key,
            default_value,
        )
        return default_value

    return int(value)


def get_config_float(env_key: str) -> float:
    value = os.getenv(env_key)

    if not value:
        logger.error("%s configuration value is missing", env_key)
        raise ValueError(f"{env_key} is set to null or empty")

    return float(value)


MAX_DISTANCE = get_config_float("RETRIEVER_DOCUMENT_MAX_DISTANCE")
FETCH_LIMIT = get_config(20, "RETRIEVER_DOCUMENT_FETCH_LIMIT")
NUMBER_OF_DOC_RETURN = get_config(3, "NUMBER_OF_DOC_RETURN")


def retrieve_documents(question: str) -> list[Document]:
    logger.info(
        "Retrieving documents: question_length=%s, fetch_limit=%s, max_distance=%s, return_limit=%s",
        len(question),
        FETCH_LIMIT,
        MAX_DISTANCE,
        NUMBER_OF_DOC_RETURN,
    )

    try:
        documents_with_scores = vector_store.similarity_search_with_score(
            query=question,
            k=FETCH_LIMIT,
        )
    except Exception:
        logger.exception("Document retrieval failed")
        raise

    scores = [distance for _document, distance in documents_with_scores]
    if scores:
        logger.info(
            "Retrieved candidate documents: count=%s, best_distance=%s, worst_distance=%s",
            len(documents_with_scores),
            min(scores),
            max(scores),
        )
    else:
        logger.info("Retrieved candidate documents: count=0")

    relevant_documents = [
        document
        for document, distance in documents_with_scores
        if distance <= MAX_DISTANCE
    ]

    selected_documents = relevant_documents[:NUMBER_OF_DOC_RETURN]

    logger.info(
        "Selected relevant documents: relevant_count=%s, returned_count=%s",
        len(relevant_documents),
        len(selected_documents),
    )

    return selected_documents
