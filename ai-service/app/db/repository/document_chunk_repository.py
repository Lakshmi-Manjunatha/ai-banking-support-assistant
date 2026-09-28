from sqlalchemy import select

from app.db.database import SessionLocal
from app.db.models.document_chunk import DocumentChunk


def save_embeddings(document_chunks : list[DocumentChunk] ) :
    db = SessionLocal()
    try :
        db.add_all(document_chunks)
        db.commit()

    except Exception as ex :
        db.rollback()
        raise

    finally:
        db.close()

def retrieve_similar_chunks(question_embedding : list[float]) -> list[DocumentChunk] :

    db = SessionLocal()
    try:
        statement = (
            select (DocumentChunk)
            .order_by(DocumentChunk.embedding.cosine_distance(question_embedding))
            .limit(3)
        )
        result = db.execute(statement)
        return result.scalars().all()
    finally:
        db.close()

