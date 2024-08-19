
from fastapi import APIRouter, Depends, HTTPException
from models.subscription import Subscription
from models.user import User
from dto.subscriptions import SubscriptionCreate, SubscriptionResponse
from api.helper.helper import get_db, get_current_user, calculate_subscription_end_date
from sqlalchemy.orm import Session

router = APIRouter()

    
@router.post("/subscriptions/", response_model=SubscriptionResponse)
async def create_subscription(
    subscription: SubscriptionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.subscription and current_user.subscription.is_active:
        raise HTTPException(status_code=400, detail="User already has an active subscription")

    end_date = calculate_subscription_end_date(subscription.plan_type)
    new_subscription = Subscription(
        user_id=current_user.user_id,
        plan_type=subscription.plan_type,
        end_date=end_date
    )
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return new_subscription

@router.get("/subscriptions/current", response_model=SubscriptionResponse)
async def get_current_subscription(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.subscription or not current_user.subscription.is_active:
        raise HTTPException(status_code=404, detail="No active subscription found")
    return current_user.subscription

@router.delete("/subscriptions/cancel")
async def cancel_subscription(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.subscription or not current_user.subscription.is_active:
        raise HTTPException(status_code=404, detail="No active subscription found")
    
    current_user.subscription.is_active = False
    db.commit()
    return {"message": "Subscription cancelled successfully"}

