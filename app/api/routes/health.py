from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.pinecone_service import index

router = APIRouter()


# -------------------------------
# BASIC APP HEALTH
# -------------------------------
@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-meeting-copilot"
    }


# -------------------------------
# DATABASE HEALTH
# -------------------------------
@router.get("/health/db")
def database_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "postgresql"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database unhealthy: {str(e)}"
        )


# -------------------------------
# VECTOR DB HEALTH (PINECONE)
# -------------------------------
@router.get("/health/vector")
def vector_health():
    try:
        stats = index.describe_index_stats()

        return {
            "status": "healthy",
            "vector_db": "pinecone",
            "stats": stats
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Pinecone unhealthy: {str(e)}"
        )