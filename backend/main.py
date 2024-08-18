from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from services.workflow import WorkFlow
from config import LLMConfig, TiDBConfig, Settings
from config import ASSET_PATH
from utils import image_to_base64

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchPayload(BaseModel):
    customer_message: Optional[str] = None
    attached_image: Optional[str] = None  

class SearchResponse(BaseModel):
    bot_message: str
    is_catalouge_changed: bool
    catalouge: List[Dict[str, Any]]  

global workflow

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
