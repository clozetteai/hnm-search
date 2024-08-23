import os
import traceback
from typing import Any, Dict, List, Optional

from config import LLMConfig, Settings, TiDBConfig
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.catalouge import get_article_info
from services.tidb_connector import connect_to_tidb
from services.workflow import WorkFlow

load_dotenv(find_dotenv())

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
        llm_config=LLMConfig(), tidb_config=TiDBConfig(), settings=Settings()
    )


@app.on_event("shutdown")
async def shutdown_event():
    global workflow
    if workflow:
        del workflow


from typing import Optional

from fastapi import File, Form, HTTPException, UploadFile


@app.post("/api/search", response_model=SearchResponse)
async def search(
    customer_message: Optional[str] = Form(None), file: UploadFile = File(None)
):
    try:
        if file is not None:
            if file.content_type != "image/jpeg":
                raise HTTPException(
                    status_code=400,
                    detail="Invalid file format. Only .jpg files are allowed.",
                )
            filepath = os.path.join(os.getcwd(), file.filename)
            # Save the file or process it as needed
            with open(filepath, "wb") as buffer:
                buffer.write(file.file.read())
        else:
            filepath = None

        result = workflow.run(filepath, customer_message)

        for content in result.catalouge:
            image_url = (
                f"{os.getenv('IMAGE_API_BASE_URL')}/api/image/0{content['article_id']}"
            )
            content["image_url"] = image_url

        return SearchResponse(
            bot_message=result.bot_message,
            is_catalouge_changed=result.is_catalouge_changed,
            catalouge=result.catalouge,
        )
    except Exception as e:
        tb_str = traceback.format_exc()
        print("----------")
        print(tb_str)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/catalouge")
def get_catalouge():
    catalouge = workflow.catalouge_state
    for content in catalouge:
        image_url = (
            f"{os.getenv('IMAGE_API_BASE_URL')}/api/image/0{content['article_id']}"
        )
        content["image_url"] = image_url
    return catalouge


@app.get("/api/article/{article_id}")
def get_article(article_id: int):
    article = get_article_info(
        database=connect_to_tidb(tidb_config=workflow.tidb_config),
        article_id=article_id,
    )
    article["image_url"] = f"{os.getenv('IMAGE_API_BASE_URL')}/api/image/0{article_id}"
    return article
