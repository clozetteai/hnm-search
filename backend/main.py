import base64
import uuid
import os, io, random, time, secrets
from textwrap import dedent
from fastapi import FastAPI, UploadFile, File, Form, Depends, status, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException
from typing import List
from connectors.s3.minio import minio_client
from constants.constants import MINIO_BUCKET_NAME, ACCESS_TOKEN_EXPIRE_MINUTES
from minio.error import S3Error
from datetime import timedelta
from models.user import User, UserSettings, Message, BotResponse, PromptTemplate, Feedback, APIKey, ChatSession
from dto.user import UserCreate, ChatSessionCreate, FeedbackCreate, MessageCreate, UserSettingsUpdate, SubscriptionCreate, SubscriptionResponse
from sqlalchemy.orm import Session
from api.helper.helper import pwd_context, create_access_token, get_current_user, get_db, calculate_subscription_end_date
from models.user import Subscription

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allows all origins, you can specify specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

current_dir = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(current_dir, "assets")

# Dummy data starting here
TOTAL_PRODUCTS = 1000
ASSETS = [os.path.join(IMAGE_DIR, f"asset{i+1}.jpeg") for i in range(5)]


@app.get("/")
async def root():
    return {"message": "Not Found in this World"}


def generate_products(page: int, limit: int):
    products = []
    for i in range(limit):
        product_id = (page - 1) * limit + i + 1
        with open(ASSETS[i % len(ASSETS)], "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        products.append({
            "id": product_id,
            "title": f"Product {product_id}",
            "price": f"$ {random.uniform(10, 100):.2f}",
            "imageUrl": f"data:image/jpeg;base64,{base64_image}",
        })
    return products


@app.get("/api/search")
async def search(query: str, type: str, page: int = 1, limit: int = 10):
    time.sleep(1)  # Simulate delay
    products = generate_products(page, limit)
    total_products = TOTAL_PRODUCTS
    bot_response = dedent(f"""
        Here is what I found for "{query}"\n\nI\'ve found some great options for you. 
        Let me know if you need more details! From backend
    """
    )
    return JSONResponse(
        content={
            "products": products,
            "totalProducts": total_products,
            "botResponse": bot_response,
        }
    )
    
@app.post("/api/upload-image")
async def upload_image(image: UploadFile = File(...)):
    time.sleep(1)  # Simulate delay
    file_location = f"images/{image.filename}"
    with open(file_location, "wb") as file:
        file.write(await image.read())
    return {"success": True, "message": "Image uploaded successfully"}


@app.post("/api/search/image")
async def image_search(prompt: str = Form(...), images: List[UploadFile] = File(None)):
    time.sleep(1)  # Simulate delay

    # Process and upload images to MinIO
    uploaded_images = []
    if images:
        for image in images:
            try:
                content = await image.read()
                print("filename: ", image.filename)
                image_name = f"{uuid.uuid4()}_{image.filename}"  # Create a unique name for each image
                
                # Upload image to MinIO
                minio_client.put_object(
                    MINIO_BUCKET_NAME,
                    image_name,
                    io.BytesIO(content),  # Wrap content in BytesIO
                    length=len(content),
                    content_type=image.content_type
                )
                
                # Generate presigned URL for the uploaded image (valid for 1 hour)
                image_url = minio_client.presigned_get_object(
                    MINIO_BUCKET_NAME, 
                    image_name, 
                    expires=timedelta(hours=1) 
                )
                uploaded_images.append(image_url)

            except S3Error as e:
                print(f"Error uploading image {image.filename}: {e}")

    # Generate bot response
    bot_response = dedent(f"""
        Here is what I found for "{prompt}" with {len(uploaded_images)} image(s)\n\n
        I've found some great options based on your text and image input. 
        Let me know if you need more details! From backend
    """)

    return JSONResponse(
        content={
            "totalProducts": TOTAL_PRODUCTS,
            "botResponse": bot_response,
            "uploadedImages": uploaded_images 
        }
    )

# Record voice endpoint
@app.post("/api/record-voice")
async def record_voice(audio: UploadFile = File(...)):
    time.sleep(1)  # Simulate delay
    file_location = f"audio/{audio.filename}"
    with open(file_location, "wb") as file:
        file.write(await audio.read())
    return {"success": True, "message": "Voice recorded successfully"}


@app.post("/api/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"username": new_user.username, "email": new_user.email}

@app.post("/api/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# User settings endpoints
@app.put("/api/users/settings")
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

# Chat session endpoints
@app.post("/api/chat-sessions/", status_code=status.HTTP_201_CREATED)
async def create_chat_session(session: ChatSessionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_session = ChatSession(user_id=current_user.user_id, title=session.title)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@app.get("/api/chat-sessions/")
async def list_chat_sessions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sessions = db.query(ChatSession).filter(ChatSession.user_id == current_user.user_id).all()
    return sessions

# Message endpoints
@app.post("/chat-sessions/{session_id}/messages/", status_code=status.HTTP_201_CREATED)
async def create_message(session_id: int, message: MessageCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.session_id == session_id, ChatSession.user_id == current_user.user_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    new_message = Message(session_id=session_id, user_id=current_user.user_id, content=message.content, message_type=message.message_type)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

@app.get("/api/chat-sessions/{session_id}/messages/")
async def list_messages(session_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.query(ChatSession).filter(ChatSession.session_id == session_id, ChatSession.user_id == current_user.user_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.timestamp).all()
    return messages

# Bot response endpoints
@app.post("/api/bot-responses/", status_code=status.HTTP_201_CREATED)
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
@app.post("/api/messages/{message_id}/feedback", status_code=status.HTTP_201_CREATED)
async def create_feedback(message_id: int, feedback: FeedbackCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.message_id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    new_feedback = Feedback(user_id=current_user.user_id, message_id=message_id, rating=feedback.rating, comment=feedback.comment)
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback

# API key endpoints
@app.post("/api/api-keys/", status_code=status.HTTP_201_CREATED)
async def create_api_key(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    api_key = APIKey(user_id=current_user.user_id, api_key=secrets.token_urlsafe(32))
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return {"api_key": api_key.api_key}

@app.get("/api/api-keys/")
async def list_api_keys(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    api_keys = db.query(APIKey).filter(APIKey.user_id == current_user.user_id, APIKey.is_active == True).all()
    return api_keys

@app.delete("/api/api-keys/{key_id}")
async def delete_api_key(key_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    api_key = db.query(APIKey).filter(APIKey.key_id == key_id, APIKey.user_id == current_user.user_id).first()
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    api_key.is_active = False
    db.commit()
    return {"message": "API key deactivated"}

# Prompt template endpoints
@app.post("/api/prompt-templates/", status_code=status.HTTP_201_CREATED)
async def create_prompt_template(name: str, content: str, db: Session = Depends(get_db)):
    new_template = PromptTemplate(name=name, content=content)
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    return new_template

@app.get("/api/prompt-templates/")
async def list_prompt_templates(db: Session = Depends(get_db)):
    templates = db.query(PromptTemplate).all()
    
@app.post("/subscriptions/", response_model=SubscriptionResponse)
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

@app.get("/subscriptions/current", response_model=SubscriptionResponse)
async def get_current_subscription(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.subscription or not current_user.subscription.is_active:
        raise HTTPException(status_code=404, detail="No active subscription found")
    return current_user.subscription

@app.delete("/subscriptions/cancel")
async def cancel_subscription(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.subscription or not current_user.subscription.is_active:
        raise HTTPException(status_code=404, detail="No active subscription found")
    
    current_user.subscription.is_active = False
    db.commit()
    return {"message": "Subscription cancelled successfully"}

@app.delete("/users/me")
async def delete_user_account(background_tasks: BackgroundTasks, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Implement any necessary cleanup tasks here
    def cleanup_user_data(user_id: int):
        # Perform cleanup tasks (e.g., deleting user data, cancelling subscriptions, etc.)
        pass

    current_user.is_active = False
    db.commit()
    background_tasks.add_task(cleanup_user_data, current_user.user_id)
    return {"message": "User account deactivated. Cleanup tasks scheduled."}