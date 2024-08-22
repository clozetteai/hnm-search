
from fastapi import APIRouter, Depends, status, HTTPException
from models.user import User, APIKey
from api.helper.helper import get_current_user, get_db
from sqlalchemy.orm import Session
import secrets

router = APIRouter()


# API key endpoints
@router.post("/api-keys/", status_code=status.HTTP_201_CREATED)
async def create_api_key(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    api_key = APIKey(user_id=current_user.user_id, api_key=secrets.token_urlsafe(32))
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return {"api_key": api_key.api_key}

@router.get("/api-keys/")
async def list_api_keys(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    api_keys = db.query(APIKey).filter(APIKey.user_id == current_user.user_id, APIKey.is_active == True).all()
    return api_keys

@router.delete("/api-keys/{key_id}")
async def delete_api_key(key_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    api_key = db.query(APIKey).filter(APIKey.key_id == key_id, APIKey.user_id == current_user.user_id).first()
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    api_key.is_active = False
    db.commit()
    return {"message": "API key deactivated"}