from app.db.database import SessionLocal
from app.db.models.document_chunk import DocumentChunk

db = SessionLocal()


def save_embeddings(document_chunks : list[DocumentChunk] ) :
    try :
        db.add_all(document_chunks)
        db.commit()

    except Exception as ex :
        db.rollback()
        raise

    finally:
        db.close()