import os
import time
import random
import uvicorn
from textwrap import dedent
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

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

IMAGE_DIR = "/home/anindya/workspace/opensource/company-ai/backend/assets"

# Dummy data starting here
TOTAL_PRODUCTS = 1000
ASSETS = [os.path.join(IMAGE_DIR, f"asset{i+1}.jpeg") for i in range(5)]


import base64

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


# Upload image endpoint
@app.post("/api/upload-image")
async def upload_image(image: UploadFile = File(...)):
    time.sleep(1)  # Simulate delay
    file_location = f"images/{image.filename}"
    with open(file_location, "wb") as file:
        file.write(await image.read())
    return {"success": True, "message": "Image uploaded successfully"}


# Record voice endpoint
@app.post("/api/record-voice")
async def record_voice(audio: UploadFile = File(...)):
    time.sleep(1)  # Simulate delay
    file_location = f"audio/{audio.filename}"
    with open(file_location, "wb") as file:
        file.write(await audio.read())
    return {"success": True, "message": "Voice recorded successfully"}


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
