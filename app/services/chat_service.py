import time
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from openai import OpenAI

from app.config.settings import settings
from app.db.models import (
    Meeting,
    ChatHistory
)

from app.services.pinecone_service import (
    search_embedding
)

from app.utils.logger import logger
from app.utils.exceptions import (
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
    meeting_id,
    db: Session
) -> str:

    if not question.strip():
        raise ValidationException(
            "Question cannot be empty"
        )

    context = None
    db_available = True

    # --------------------------------
    # Try PostgreSQL first
    # --------------------------------
    try:
        meeting = (
            db.query(Meeting)
            .filter(
                Meeting.id == meeting_id
            )
            .first()
        )

        if meeting:
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

            logger.info(
                "Meeting context "
                "loaded from DB"
            )

    except SQLAlchemyError as e:
        db.rollback()
        db_available = False

        logger.warning(
            "Database unavailable. "
            f"Trying Pinecone fallback: {str(e)}"
        )

    # --------------------------------
    # Pinecone fallback
    # --------------------------------
    if not context:
        try:
            logger.info(
                "Generating question "
                "embedding"
            )

            embedding_response = (
                client.embeddings.create(
                    model="text-embedding-3-small",
                    input=question
                )
            )

            query_embedding = (
                embedding_response
                .data[0]
                .embedding
            )

            matches = search_embedding(
                query_embedding
            )

            if matches:
                transcript = (
                    matches[0]
                    .metadata
                    .get(
                        "transcript",
                        ""
                    )
                )

                context = f"""
Transcript:
{transcript}
"""

                logger.info(
                    "Meeting context "
                    "loaded from Pinecone"
                )

        except Exception as e:
            logger.warning(
                "Pinecone fallback "
                f"failed: {str(e)}"
            )

    # --------------------------------
    # Final guard
    # --------------------------------
    if not context:
        raise ProcessingException(
            "Unable to retrieve "
            "meeting context"
        )

    # --------------------------------
    # Ask OpenAI
    # --------------------------------
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
                                "Answer only from "
                                "the provided "
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

            # --------------------------------
            # Best-effort DB save
            # --------------------------------
            if db_available:
                try:
                    chat = ChatHistory(
                        meeting_id=meeting_id,
                        question=question,
                        answer=answer
                    )

                    db.add(chat)
                    db.commit()
                    db.refresh(chat)

                    logger.info(
                        f"Chat saved "
                        f"id={chat.id}"
                    )

                except SQLAlchemyError as e:
                    db.rollback()

                    logger.warning(
                        "Skipping DB "
                        "chat save: "
                        f"{str(e)}"
                    )

            return answer

        except Exception as e:
            try:
                db.rollback()
            except Exception:
                pass

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