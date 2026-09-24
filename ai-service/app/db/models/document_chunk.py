from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import BigInteger, String, Text, DateTime, Sequence, func, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

document_chunk_id_seq = Sequence(name="document_chunk_id_seq", start=1, increment=1)


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column("doc_chunk_id", BigInteger, document_chunk_id_seq, primary_key=True)

    source: Mapped[str] = mapped_column(String(255), nullable=False)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)

    embedding: Mapped[list[float]] = mapped_column(Vector(768), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
