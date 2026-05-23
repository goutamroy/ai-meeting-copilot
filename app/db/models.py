from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.db.database import Base


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    audio_file_url = Column(
        String,
        nullable=False
    )

    transcript = Column(
        Text,
        nullable=True
    )

    summary = Column(
        Text,
        nullable=True
    )

    action_items = Column(
        Text,
        nullable=True
    )

    key_decisions = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    meeting_id = Column(
        Integer,
        ForeignKey("meetings.id")
    )

    question = Column(
        Text,
        nullable=False
    )

    answer = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )