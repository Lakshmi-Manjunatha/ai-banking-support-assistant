from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is not configured")

# Database engine - manages database connectivity and connection pooling
engine = create_engine(database_url)

# Session factory - creates SQLAlchemy Session objects
SessionLocal = sessionmaker(
    bind=engine
)

# Base class for SQLAlchemy ORM entities/models
class Base(DeclarativeBase):
    pass