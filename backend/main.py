import uuid
import os, io, time
from textwrap import dedent
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from constants.constants import MINIO_BUCKET_NAME
from typing import List
from connectors.s3.minio import minio_client
from minio.error import S3Error
from datetime import timedelta
import logging 

from dto.search import SearchPayload, SearchResponse
from services.workflow import WorkFlow
from config import LLMConfig, TiDBConfig, Settings
from config import ASSET_PATH
from utils import image_to_base64
from api import (
    user_router,
    chat_router,
    bot_router,
    api_key_router,
    prompt_template_router,
    subscription_router
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

global workflow
logging.basicConfig(
    level=logging.DEBUG, 
    # filename='logs/app.log', 
    # filemode='a', 
    format='%(levelname)s:     %(message)s'
)


# CONFIG TO BE REMOVE ###
current_dir = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(current_dir, "assets")
TOTAL_PRODUCTS = 1000
ASSETS = [os.path.join(IMAGE_DIR, f"asset{i+1}.jpeg") for i in range(5)]

############ ----- #######


@app.on_event("startup")
async def startup_event():
    global workflow
    workflow = WorkFlow(
        llm_config=LLMConfig(),
        tidb_config=TiDBConfig(),
        settings=Settings()
    )

@app.on_event("shutdown")
async def shutdown_event():
    global workflow
    if workflow:
        del workflow
        
@app.get("/")
async def root():
    return {"message": "Not Found in this World"}


@app.post("/api/search", response_model=SearchResponse)
async def search(payload: SearchPayload):
    try:
        result = workflow.run(payload.dict())

        # Add images to each item in the catalogue result
        for item in result.catalouge:
            image_path = ASSET_PATH / f"0{item['article_id']}.jpg"
            if image_path.exists():
                image_base64 = image_to_base64(image_path)
            else:
                image_base64 = None
            item["image"] = image_base64

        return SearchResponse(
            bot_message=result.bot_message,
            is_catalouge_changed=result.is_catalouge_changed,
            catalouge=result.catalouge
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/catalouge")
def get_catalouge():
    catalouge = workflow.catalouge_state
    for result in catalouge:
        image_path = ASSET_PATH / f"0{result['article_id']}.jpg"
        if image_path.exists():
            image_base64 = image_to_base64(image_path)
        else:
            image_base64 = None
        result["image"] = image_base64
    return catalouge  


@app.post("/api/search-by-image")
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

#TODO Need temporary voice storage convert speach -> text 
@app.post("/api/record-voice")
async def record_voice(audio: UploadFile = File(...)):
    time.sleep(1)  # Simulate delay
    file_location = f"audio/{audio.filename}"
    with open(file_location, "wb") as file:
        file.write(await audio.read())
    return {"success": True, "message": "Voice recorded successfully"}


app.include_router(user_router, prefix="/api", tags=["users"])
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(bot_router, prefix="/api", tags=["bot"])
app.include_router(api_key_router, prefix="/api", tags=["api keys"])
app.include_router(prompt_template_router, prefix="/api", tags=["prompt templates"])
app.include_router(subscription_router, prefix="/api", tags=["subscriptions"])

