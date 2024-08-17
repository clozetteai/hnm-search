import os
import time
import random
from textwrap import dedent
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
import base64
from typing import List
from connectors.s3.minio import minio_client
from constants.constants import MINIO_BUCKET_NAME
import uuid
from minio.error import S3Error
import io
from datetime import timedelta

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
print(IMAGE_DIR)

# Dummy data starting here
TOTAL_PRODUCTS = 1000
ASSETS = [os.path.join(IMAGE_DIR, f"asset{i+1}.jpeg") for i in range(5)]


@app.get("/")
async def root():
    return {"message": "Hello World"}


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


