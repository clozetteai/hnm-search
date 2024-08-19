from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from models.user import User
from dto.user import UserCreate
from api.helper.helper import create_access_token, get_current_user, hash_password, verify_password, get_db
from fastapi.security import OAuth2PasswordRequestForm
from constants.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from models.user import User, UserSettings
from dto.user import UserCreate, UserSettingsUpdate

router = APIRouter()

@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"username": new_user.username, "email": new_user.email}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# User settings endpoints
@router.put("/users/settings")
async def update_user_settings(settings: UserSettingsUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_settings = db.query(UserSettings).filter(UserSettings.user_id == current_user.user_id).first()
    if not db_settings:
        db_settings = UserSettings(user_id=current_user.user_id)
        db.add(db_settings)
    for key, value in settings.dict(exclude_unset=True).items():
        setattr(db_settings, key, value)
    db.commit()
    db.refresh(db_settings)
    return db_settings


@router.delete("/users/me")
async def delete_user_account(background_tasks: BackgroundTasks, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    def cleanup_user_data(user_id: int):
        # Perform cleanup tasks (e.g., deleting user data, cancelling subscriptions, etc.)
        pass

    current_user.is_active = False
    db.commit()
    background_tasks.add_task(cleanup_user_data, current_user.user_id)
    return {"message": "User account deactivated. Cleanup tasks scheduled."}