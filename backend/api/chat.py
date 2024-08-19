
from fastapi import APIRouter, Depends, status, HTTPException
from models.user import User, Message, ChatSession
from dto.user import ChatSessionCreate, MessageCreate
from api.helper.helper import get_db, get_current_user
from sqlalchemy.orm import Session

router = APIRouter()


# Chat session endpoints
@router.post("/chat-sessions/", status_code=status.HTTP_201_CREATED)
async def create_chat_session(session: ChatSessionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_session = ChatSession(user_id=current_user.user_id, title=session.title)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@router.get("/chat-sessions/")
async def list_chat_sessions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sessions = db.query(ChatSession).filter(ChatSession.user_id == current_user.user_id).all()
    return sessions

# Message endpoints
@router.post("/chat-sessions/{session_id}/messages/", status_code=status.HTTP_201_CREATED)
async def create_message(session_id: int, message: MessageCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.session_id == session_id, ChatSession.user_id == current_user.user_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    new_message = Message(session_id=session_id, user_id=current_user.user_id, content=message.content, message_type=message.message_type)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

@router.get("/chat-sessions/{session_id}/messages/")
async def list_messages(session_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.session_id == session_id, ChatSession.user_id == current_user.user_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.timestamp).all()
    return messages