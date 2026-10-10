import logging

from fastapi import FastAPI
from app.api.routes import router
from app.logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(router)
logger.info("FastAPI application initialized")
