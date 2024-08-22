
import jwt
from jwt import PyJWTError
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from connectors.db.postgresql import SessionLocal
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from constants.constants import SECRET_KEY, ALGORITHM
from passlib.context import CryptContext
from models.user import User
from dto.subscriptions import SubscriptionType
import hashlib, os
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Helper functions
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
  
  
# Subscription helper functions
def calculate_subscription_end_date(plan_type: SubscriptionType) -> datetime:
    now = datetime.utcnow()
    if plan_type.endswith("_monthly"):
        return now + timedelta(days=30)
    elif plan_type.endswith("_annual"):
        return now + timedelta(days=365)
    else:
        raise ValueError("Invalid plan type")
    
def hash_password(password: str) -> str:
    salt = os.urandom(32)
    # Use SHA256 for hashing
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + hashed.hex()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    salt = bytes.fromhex(hashed_password[:64])
    stored_password = hashed_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100000)
    return pwdhash.hex() == stored_password