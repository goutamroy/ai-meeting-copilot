from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.database import (
    get_db
)

from app.db.schemas import (
    ChatRequest
)

from app.db.models import (
    ChatHistory
)

from app.services.chat_service import (
    ask_question
)

from app.utils.logger import (
    logger
)

from app.utils.exceptions import (
    DatabaseException
)

router = APIRouter()


# ---------------------------------
# CHAT WITH MEETING
# ---------------------------------
@router.post("/chat")
def chat_with_meeting(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    answer = ask_question(
        question=
            request.question,
        meeting_id=
            request.meeting_id,
        db=db
    )

    return {
        "success": True,
        "meeting_id":
            request.meeting_id,
        "question":
            request.question,
        "answer":
            answer
    }


# ---------------------------------
# CHAT HISTORY
# ---------------------------------
@router.get(
    "/chat-history/{meeting_id}"
)
def get_chat_history(
    meeting_id: int,
    db: Session = Depends(get_db)
):
    try:
        chats = (
            db.query(
                ChatHistory
            )
            .filter(
                ChatHistory
                .meeting_id
                == meeting_id
            )
            .order_by(
                ChatHistory
                .created_at.desc()
            )
            .all()
        )

        return {
            "success": True,
            "count":
                len(chats),
            "data":
                chats
        }

    except Exception as e:
        logger.error(
            f"Chat history "
            f"failed: {str(e)}"
        )

        raise DatabaseException(
            "Failed to fetch "
            "chat history"
        )