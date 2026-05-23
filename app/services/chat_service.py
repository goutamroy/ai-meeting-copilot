import time
from sqlalchemy.orm import Session
from openai import OpenAI

from app.config.settings import settings
from app.db.models import (
    Meeting,
    ChatHistory
)

from app.utils.logger import logger
from app.utils.exceptions import (
    NotFoundException,
    ValidationException,
    ProcessingException
)

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)

MAX_RETRIES = 3
BACKOFF_SECONDS = 2


def ask_question(
    question: str,
    meeting_id: int,
    db: Session
) -> str:
    if not question.strip():
        raise ValidationException(
            "Question "
            "cannot be empty"
        )

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

    context = f"""
Transcript:
{meeting.transcript or ""}

Summary:
{meeting.summary or ""}

Action Items:
{meeting.action_items or ""}

Key Decisions:
{meeting.key_decisions or ""}
"""

    for attempt in range(
        1,
        MAX_RETRIES + 1
    ):
        try:
            logger.info(
                f"Chat generation "
                f"attempt {attempt}"
            )

            response = (
                client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content":
                                "Answer only "
                                "from the "
                                "provided "
                                "meeting context."
                        },
                        {
                            "role": "user",
                            "content":
                                f"Context:\n"
                                f"{context}\n\n"
                                f"Question: "
                                f"{question}"
                        }
                    ],
                    timeout=60
                )
            )

            answer = (
                response
                .choices[0]
                .message
                .content
                if response
                and response.choices
                else
                "No response generated."
            )

            chat = ChatHistory(
                meeting_id=
                    meeting_id,
                question=
                    question,
                answer=
                    answer
            )

            db.add(chat)
            db.commit()
            db.refresh(chat)

            logger.info(
                f"Chat saved "
                f"id={chat.id}"
            )

            return answer

        except Exception as e:
            db.rollback()

            logger.warning(
                f"Chat retry "
                f"{attempt} failed: "
                f"{str(e)}"
            )

            if attempt < MAX_RETRIES:
                sleep_time = (
                    BACKOFF_SECONDS
                    ** attempt
                )
                time.sleep(
                    sleep_time
                )
                continue

            logger.error(
                "Chat failed "
                "after retries"
            )

            raise ProcessingException(
                "Chat processing failed"
            )