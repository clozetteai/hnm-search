import os
import time
import random
from textwrap import dedent
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import base64

from routes import router as search_router

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IMAGE_DIR = "/home/anindya/workspace/opensource/company-ai/backend/assets"
ASSETS = [f for f in os.listdir(IMAGE_DIR) if f.endswith((".jpeg", ".jpg", ".png"))]


def generate_product(product_id: int, image_file: str):
    with open(os.path.join(IMAGE_DIR, image_file), "rb") as image:
        base64_image = base64.b64encode(image.read()).decode("utf-8")
    return {
        "id": product_id,
        "title": f"Product {product_id}",
        "price": f"$ {random.uniform(10, 100):.2f}",
        "imageUrl": f"data:image/jpeg;base64,{base64_image}",
    }


@app.get("/api/catalog")
async def get_catalog(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=50)):
    total_products = len(ASSETS)
    start_index = (page - 1) * limit
    end_index = min(start_index + limit, total_products)

    products = [
        generate_product(i + 1, ASSETS[
            random.choice(range(0, len(ASSETS)))
        ]) for i in range(start_index, end_index)
    ]

    return JSONResponse(
        content={
            "products": products,
            "totalProducts": total_products,
            "botResponse": "Welcome to our catalog! Here are some of our products. Feel free to browse or search for specific items.",
        }
    )


# @app.get("/api/search")
# async def search(
#     query: str = "",
#     type: str = "text",
#     page: int = Query(1, ge=1),
#     limit: int = Query(10, ge=1, le=50),
# ):
#     time.sleep(1)  # Simulate delay

#     if not query:
#         # If no query is provided, return the catalog
#         return await get_catalog(page, limit)

#     # Perform search (for demonstration, we'll just filter based on the query in the product title)
#     total_products = len(ASSETS)

#     start_index = (page - 1) * limit
#     end_index = min(start_index + limit, total_products)

#     products = [
#         generate_product(i + 1, ASSETS[
#             random.choice(range(0, len(ASSETS)))
#         ])
#         for i in range(start_index, end_index)
#     ]

#     bot_response = dedent(
#         f"""
#         Here is what I found for "{query}"\n\nI've found {total_products} options for you. 
#         Let me know if you need more details!
#     """
#     )

#     return JSONResponse(
#         content={
#             "products": products,
#             "totalProducts": total_products,
#             "botResponse": bot_response,
#         }
#     )


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


app.include_router(search_router)
