import os
import base64
import random
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from models import ConversationInput, SearchOutput
from services.conversation_module.conversation_module import ConversationModule

router = APIRouter()
cm = ConversationModule(5)

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

def search_from_user_conversation(query: List[str], page: int = 1, limit: int = 10):
    total_products = len(ASSETS)
    start_index = (page - 1) * limit
    end_index = min(start_index + limit, total_products)
    products = [
        generate_product(i + 1, ASSETS[random.choice(range(0, len(ASSETS)))])
        for i in range(start_index, end_index)
    ]
    bot_response = f"Here's what I found based on your preferences. I've found {total_products} options for you."
    return {
        "products": products,
        "total_products": total_products,
        "bot_response": bot_response,
    }

@router.post("/search", response_model=SearchOutput)
async def search(
    input: ConversationInput,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
):
    conversation_output = cm.converse(input.message)
    
    if not conversation_output["conversation_ended"]:
        return SearchOutput(
            conversation_output=conversation_output,
            bot_response=conversation_output["bot_response"],
            products=None,
            total_products=None
        )
    else:
        cm.reset()
        search_query = conversation_output["outputs"]["search_query"]
        products = search_from_user_conversation(search_query, page, limit)
        return SearchOutput(
            conversation_output=conversation_output,
            products=products["products"],
            total_products=products["total_products"],
            bot_response=products["bot_response"]
        )

@router.get("/catalog")
async def get_catalog(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=50)):
    total_products = len(ASSETS)
    start_index = (page - 1) * limit
    end_index = min(start_index + limit, total_products)
    products = [
        generate_product(i + 1, ASSETS[random.choice(range(0, len(ASSETS)))])
        for i in range(start_index, end_index)
    ]
    return {
        "products": products,
        "total_products": total_products,
        "bot_response": "Welcome to our catalog! Here are some of our products. Feel free to ask me if you need help finding something specific."
    }
