from fastapi import APIRouter
from pydantic import BaseModel

from app.services.summary_service import generate_summary
from app.utils.exceptions import ValidationException

router = APIRouter()


class SummaryRequest(BaseModel):
    transcript: str


@router.post("/summary")
def summarize(
    request: SummaryRequest
):
    if not request.transcript.strip():
        raise ValidationException(
            "Transcript cannot be empty"
        )

    result = generate_summary(
        request.transcript
    )

    return {
        "success": True,
        "summary": result
    }