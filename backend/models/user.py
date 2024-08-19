
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, JSON, Enum
from datetime import datetime
from connectors.db.postgresql import Base
from sqlalchemy.orm import relationship
# from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, Enum
# from datetime import datetime



class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    subscription = relationship("Subscription", back_populates="user", uselist=False)

class UserSettings(Base):
    __tablename__ = "user_settings"

    setting_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    theme = Column(String, default="light")
    language = Column(String, default="en")
    notification_preferences = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    session_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    title = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.session_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    message_type = Column(String)

class BotResponse(Base):
    __tablename__ = "bot_responses"

    response_id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.message_id"))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    model_version = Column(String)
    tokens_used = Column(Integer)

class PromptTemplate(Base):
    __tablename__ = "prompt_templates"

    template_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserPromptHistory(Base):
    __tablename__ = "user_prompt_history"

    history_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    prompt_text = Column(Text)
    used_at = Column(DateTime, default=datetime.utcnow)

class Feedback(Base):
    __tablename__ = "feedback"

    feedback_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    message_id = Column(Integer, ForeignKey("messages.message_id"))
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class APIKey(Base):
    __tablename__ = "api_keys"

    key_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    api_key = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    


