from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# -------------------------
# Chat Request Schema
# -------------------------
class ChatRequest(BaseModel):
    meeting_id: int
    question: str


# -------------------------
# Chat Response Schema
# -------------------------
class ChatResponse(BaseModel):
    success: bool
    answer: str


# -------------------------
# Meeting Base Schema
# -------------------------
class MeetingBase(BaseModel):
    audio_file_url: str
    transcript: Optional[str] = None
    summary: Optional[str] = None
    action_items: Optional[str] = None
    key_decisions: Optional[str] = None


# -------------------------
# Meeting Create Schema
# -------------------------
class MeetingCreate(MeetingBase):
    pass


# -------------------------
# Meeting Response Schema
# -------------------------
class MeetingResponse(MeetingBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------------
# Chat History Base Schema
# -------------------------
class ChatHistoryBase(BaseModel):
    meeting_id: int
    question: str
    answer: str


# -------------------------
# Chat History Response Schema
# -------------------------
class ChatHistoryResponse(ChatHistoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------------
# All Meetings Response
# -------------------------
class MeetingsListResponse(BaseModel):
    success: bool
    count: int
    data: List[MeetingResponse]


# -------------------------
# Chat History List Response
# -------------------------
class ChatHistoryListResponse(BaseModel):
    success: bool
    count: int
    data: List[ChatHistoryResponse]