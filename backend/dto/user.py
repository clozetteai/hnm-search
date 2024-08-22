
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserSettingsUpdate(BaseModel):
    theme: Optional[str]
    language: Optional[str]
    notification_preferences: Optional[dict]

class ChatSessionCreate(BaseModel):
    title: str

class MessageCreate(BaseModel):
    content: str
    message_type: str

class FeedbackCreate(BaseModel):
    rating: int
    comment: Optional[str]


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_new_password: str