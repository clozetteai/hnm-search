
from fastapi import APIRouter, Depends, status, HTTPException
from models.user import User, Message, BotResponse, Feedback
from dto.user import FeedbackCreate
from api.helper.helper import get_db, get_current_user
from sqlalchemy.orm import Session

router = APIRouter()

# Bot response endpoints
@router.post("/bot-responses/", status_code=status.HTTP_201_CREATED)
async def create_bot_response(message_id: int, content: str, model_version: str, tokens_used: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.message_id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    new_response = BotResponse(message_id=message_id, content=content, model_version=model_version, tokens_used=tokens_used)
    db.add(new_response)
    db.commit()
    db.refresh(new_response)
    return new_response

# Feedback endpoints
@router.post("/messages/{message_id}/feedback", status_code=status.HTTP_201_CREATED)
async def create_feedback(message_id: int, feedback: FeedbackCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.message_id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    new_feedback = Feedback(user_id=current_user.user_id, message_id=message_id, rating=feedback.rating, comment=feedback.comment)
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback
