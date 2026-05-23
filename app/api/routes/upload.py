from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Meeting

from app.services.meeting_pipeline import (
    process_meeting
)

from app.utils.logger import logger
from app.utils.validators import (
    validate_audio_file
)

from app.utils.exceptions import (
    ProcessingException,
    DatabaseException,
    NotFoundException
)

router = APIRouter()


# ---------------------------------
# UPLOAD AUDIO
# ---------------------------------
@router.post("/upload")
async def upload_audio(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        logger.info(
            "Starting meeting upload pipeline"
        )

        # Validate
        await validate_audio_file(
            file
        )

        # Process AI pipeline
        result = await process_meeting(
            file
        )

        meeting = Meeting(
            audio_file_url=result.get(
                "blob_url"
            ),
            transcript=result.get(
                "transcript"
            ),
            summary=result.get(
                "summary"
            ),
            action_items=result.get(
                "action_items"
            ),
            key_decisions=result.get(
                "key_decisions"
            )
        )

        db.add(meeting)
        db.commit()
        db.refresh(meeting)

        logger.info(
            f"Meeting saved "
            f"successfully: "
            f"id={meeting.id}"
        )

        return {
            "success": True,
            "meeting_id":
                meeting.id,
            "message":
                "Meeting uploaded "
                "successfully",
            "transcript":
                result.get(
                    "transcript"
                ),
            "summary":
                result.get(
                    "summary"
                ),
            "action_items":
                result.get(
                    "action_items"
                ),
            "key_decisions":
                result.get(
                    "key_decisions"
                )
        }

    except Exception as e:
        db.rollback()

        logger.error(
            f"Upload failed: "
            f"{str(e)}"
        )

        raise ProcessingException(
            "Audio upload failed"
        )


# ---------------------------------
# GET ALL MEETINGS
# ---------------------------------
@router.get("/meetings")
def get_all_meetings(
    db: Session = Depends(get_db)
):
    try:
        meetings = (
            db.query(Meeting)
            .order_by(
                Meeting.created_at.desc()
            )
            .all()
        )

        return {
            "success": True,
            "count":
                len(meetings),
            "data":
                meetings
        }

    except Exception as e:
        logger.error(
            f"Fetch meetings "
            f"failed: {str(e)}"
        )

        raise DatabaseException(
            "Failed to fetch meetings"
        )


# ---------------------------------
# GET MEETING BY ID
# ---------------------------------
@router.get(
    "/meetings/{meeting_id}"
)
def get_meeting_by_id(
    meeting_id: int,
    db: Session = Depends(get_db)
):
    try:
        meeting = (
            db.query(Meeting)
            .filter(
                Meeting.id
                == meeting_id
            )
            .first()
        )

        if not meeting:
            raise NotFoundException(
                "Meeting not found"
            )

        return {
            "success": True,
            "data": meeting
        }

    except (
        NotFoundException
    ):
        raise

    except Exception as e:
        logger.error(
            f"Meeting fetch "
            f"failed: {str(e)}"
        )

        raise DatabaseException(
            "Failed to fetch meeting"
        )