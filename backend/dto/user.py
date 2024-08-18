import enum
from datetime import datetime
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



# Subscription Plan
class SubscriptionType(str, enum.Enum):
    STARTER_MONTHLY = "starter_monthly"
    PRO_MONTHLY = "pro_monthly"
    ENTERPRISE_MONTHLY = "enterprise_monthly"
    STARTER_ANNUAL = "starter_annual"
    PRO_ANNUAL = "pro_annual"
    ENTERPRISE_ANNUAL = "enterprise_annual"

class SubscriptionCreate(BaseModel):
    plan_type: SubscriptionType

class SubscriptionResponse(BaseModel):
    subscription_id: int
    plan_type: SubscriptionType
    start_date: datetime
    end_date: datetime
    is_active: bool