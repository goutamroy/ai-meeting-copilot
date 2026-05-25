import json

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import get_db
from app.db.models import Meeting

from app.services.meeting_pipeline import process_meeting
from app.utils.logger import logger
from app.utils.validators import validate_audio_file

from app.utils.exceptions import (
    ProcessingException,
    DatabaseException,
    NotFoundException
)

router = APIRouter()


# -----------------------------
# SAFE HELPERS
# -----------------------------
def safe_json_parse(value):
    if value is None:
        return []

    if isinstance(value, (list, dict)):
        return value

    if not isinstance(value, str):
        return value

    try:
        return json.loads(value)

    except Exception:
        try:
            # handles Python-style lists like ['a','b']
            import ast
            return ast.literal_eval(value)
        except Exception:
            return [str(value)]


def safe_json_dump(value):
    if value is None:
        return None

    if isinstance(value, (list, dict)):
        return json.dumps(value)

    return str(value)


def serialize_meeting(meeting: Meeting):
    return {
        "id": meeting.id,
        "audio_file_url": meeting.audio_file_url,
        "transcript": meeting.transcript,
        "summary": meeting.summary,
        "action_items": safe_json_parse(meeting.action_items),
        "key_decisions": safe_json_parse(meeting.key_decisions),
        "created_at": (
            meeting.created_at.isoformat()
            if meeting.created_at
            else None
        )
    }


# -----------------------------
# UPLOAD AUDIO
# -----------------------------
@router.post("/upload")
async def upload_audio(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        logger.info("Starting meeting upload pipeline")

        await validate_audio_file(file)
        result = await process_meeting(file)

        db_saved = False
        meeting_id = result.get("meeting_id")

        try:
            meeting = Meeting(
                audio_file_url=result.get("blob_url"),
                transcript=result.get("transcript"),
                summary=result.get("summary"),
                action_items=safe_json_dump(
                    result.get("action_items")
                ),
                key_decisions=safe_json_dump(
                    result.get("key_decisions")
                )
            )

            db.add(meeting)
            db.commit()
            db.refresh(meeting)

            db_saved = True
            meeting_id = meeting.id

        except SQLAlchemyError as db_error:
            db.rollback()
            logger.exception(
                f"DB Save Error: {str(db_error)}"
            )

        return {
            "success": True,
            "meeting_id": meeting_id,
            "db_persisted": db_saved,
            "message": "Meeting uploaded successfully",
            "transcript": result.get("transcript"),
            "summary": result.get("summary"),
            "action_items": result.get("action_items"),
            "key_decisions": result.get("key_decisions")
        }

    except Exception as e:
        try:
            db.rollback()
        except Exception:
            pass

        logger.exception(
            f"Upload failed: {str(e)}"
        )
        raise ProcessingException(
            "Audio upload failed"
        )


# -----------------------------
# GET ALL MEETINGS
# -----------------------------
@router.get("/meetings")
def get_all_meetings(
    db: Session = Depends(get_db)
):
    try:
        meetings = (
            db.query(Meeting)
            .order_by(Meeting.id.desc())
            .all()
        )

        return {
            "success": True,
            "count": len(meetings),
            "data": [
                serialize_meeting(m)
                for m in meetings
            ]
        }

    except Exception as e:
        logger.exception(
            f"/meetings failed: {str(e)}"
        )
        raise DatabaseException(
            "Failed to fetch meetings"
        )


# -----------------------------
# GET BY ID
# -----------------------------
@router.get("/meetings/{meeting_id}")
def get_meeting_by_id(
    meeting_id: int,
    db: Session = Depends(get_db)
):
    try:
        meeting = (
            db.query(Meeting)
            .filter(
                Meeting.id == meeting_id
            )
            .first()
        )

        if not meeting:
            raise NotFoundException(
                "Meeting not found"
            )

        return {
            "success": True,
            "data": serialize_meeting(meeting)
        }

    except NotFoundException:
        raise

    except Exception as e:
        logger.exception(
            f"/meetings/{meeting_id} failed: {str(e)}"
        )
        raise DatabaseException(
            "Failed to fetch meeting"
        )