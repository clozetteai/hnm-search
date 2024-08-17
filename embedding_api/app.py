from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
import torch

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable for the model
text_embedding_model = None

@app.on_event("startup")
async def startup_event():
    global text_embedding_model
    # Load the model on startup
    text_embedding_model = SentenceTransformer(
        "dunzhang/stella_en_400M_v5",
        trust_remote_code=True
    )
    if torch.cuda.is_available():
        text_embedding_model = text_embedding_model.cuda()

@app.on_event("shutdown")
async def shutdown_event():
    global text_embedding_model
    # Unload the model on shutdown
    if text_embedding_model:
        del text_embedding_model
        torch.cuda.empty_cache()

def get_query_embedding(query: str):
    query_prompt_name = "s2p_query"
    query_embeddings = text_embedding_model.encode(
        [query],
        prompt_name=query_prompt_name
    )
    return query_embeddings.squeeze().tolist()

@app.get("/api/embedding")
async def query_embedding(
    query: str = Query(..., description="The query string to embed")
):
    if text_embedding_model is None:
        return JSONResponse(
            content={
                "status": 503,
                "error": "Model not loaded"
            },
            status_code=503
        )
    
    embedding = get_query_embedding(query)
    embedding_str = str(embedding)
    return JSONResponse(
        content={
            "status": 200,
            "embedding": embedding_str
        }
    )
