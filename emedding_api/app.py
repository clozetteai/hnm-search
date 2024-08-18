import base64
from io import BytesIO

import torch
from clip import clip
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
from sentence_transformers import SentenceTransformer

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

text_embedding_model = None
image_embedding_model, image_preprocess = None, None


@app.on_event("startup")
async def startup_event():
    global text_embedding_model
    global image_embedding_model
    global image_preprocess

    text_embedding_model = SentenceTransformer(
        "dunzhang/stella_en_400M_v5", trust_remote_code=True
    )

    if torch.cuda.is_available():
        text_embedding_model = text_embedding_model.cuda()
        image_embedding_model, image_preprocess = clip.load("ViT-B/32", device="cuda")
    else:
        image_embedding_model, image_preprocess = clip.load("ViT-B/32", device="cpu")


@app.on_event("shutdown")
async def shutdown_event():
    global text_embedding_model
    global image_embedding_model
    global image_preprocess

    if text_embedding_model:
        del text_embedding_model

    if image_embedding_model:
        del image_embedding_model

    if image_preprocess:
        del image_preprocess
    torch.cuda.empty_cache()


def get_query_embedding(query: str):
    query_prompt_name = "s2p_query"
    query_embeddings = text_embedding_model.encode(
        [query], prompt_name=query_prompt_name
    )
    return query_embeddings.squeeze().tolist()


def get_image_embedding(image_bs64: str):
    try:
        # Decode the Base64 string into bytes
        image_data = base64.b64decode(image_bs64)

        # Load the image from the bytes
        image = Image.open(BytesIO(image_data))

        # Convert the image to RGB (ensure compatibility with models)
        image = image.convert("RGB")

        # Preprocess the image (e.g., resize, normalize)
        image_input = image_preprocess(image).unsqueeze(0)

        if torch.cuda.is_available():
            image_input = image_input.cuda()

        image_features = image_embedding_model.encode_image(image_input)
        image_embedding = image_features / image_features.norm(dim=-1, keepdim=True)

        return image_embedding.squeeze().tolist()

    except (OSError, ValueError) as e:
        raise ValueError(f"Invalid image: {e}")

    except Exception as e:
        raise ValueError(f"An unexpected error occurred: {e}")


@app.get("/api/text_embedding")
async def query_embedding(
    query: str = Query(..., description="The query string to embed")
):
    if text_embedding_model is None:
        return JSONResponse(
            content={"status": 503, "error": "Model not loaded"}, status_code=503
        )

    embedding = get_query_embedding(query)
    embedding_str = str(embedding)
    return JSONResponse(content={"status": 200, "embedding": embedding_str})


@app.post("/api/image_embedding")
async def image_embedding(request: Request):
    try:
        data = await request.json()
        image_bs64 = data.get("image_bs64", None)

        if not image_bs64:
            return JSONResponse(
                content={"status": 400, "error": "No image data provided"},
                status_code=400,
            )

        embedding = get_image_embedding(image_bs64)
        embedding_str = str(embedding)

        return JSONResponse(content={"status": 200, "embedding": embedding_str})

    except ValueError as e:
        return JSONResponse(content={"status": 400, "error": str(e)}, status_code=400)

    except Exception as e:
        return JSONResponse(
            content={"status": 500, "error": "Internal Server Error"}, status_code=500
        )
