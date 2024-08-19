
import enum
from datetime import datetime
from pydantic import BaseModel


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