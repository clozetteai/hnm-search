import os
import base64
import requests
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.orm import Session
from services.tidb_connector import connect_to_tidb_engine
from config import TiDBConfig
from typing import Optional

load_dotenv(find_dotenv())


class EmbeddingSearchService:
    def __init__(self, tidb_config: Optional[TiDBConfig] = TiDBConfig()) -> None:
        self.base_url = os.getenv("SEARCH_API_BASE_URL")
        self.engine, self.db_entity = connect_to_tidb_engine(tidb_config=tidb_config)

    def perform_text_search(self, query: str, limit: int):
        embedding_response = requests.get(
            f"{self.base_url}/api/text_embedding", params={"query": query}
        )
        if embedding_response.status_code == 200:
            text_embedding = embedding_response.json()
            with Session(self.engine) as session:
                entities = (
                    session.query(self.db_entity)
                    .order_by(
                        self.db_entity.text_embedding.cosine_distance(text_embedding)
                    )
                    .limit(limit)
                    .all()
                )
            return {"status": 200, "results": [entity.to_json() for entity in entities]}
        else:
            return {"status": 500, "results": []}

    # def perform_image_search_from_file(self, image_file_path: str, limit: int):
    #     with open(image_file_path, "rb") as f:
    #         image_bytes = f.read()
    #     image_bs64 = base64.b64encode(image_bytes).decode("utf-8")
    #     return self.perform_image_search_from_bs64(image_bs64=image_bs64, limit=limit)

    def perform_image_search_from_bs64(self, image_bs64: str, limit: int):
        payload = {"image_bs64": image_bs64}
        response = requests.post(f"{self.base_url}/api/image_embedding", json=payload)
        if response.status_code == 200:
            data = response.json()
            image_embedding = eval(data["embedding"])
            with Session(self.engine) as session:
                entities = (
                    session.query(self.db_entity)
                    .order_by(
                        self.db_entity.image_embedding.cosine_distance(image_embedding)
                    )
                    .limit(limit)
                    .all()
                )
            return {"status": 200, "results": [entity.to_json() for entity in entities]}
        else:
            return {"status": 500, "results": []}
        
    def perform_image_search_from_file(self, filepath: str, limit: int):
        file_extension = filepath.split('.')[-1]
        if file_extension.lower() != "jpg":
            return {"error": "Invalid file format. Only .jpg files are allowed."}
        try:
            with open(filepath, 'rb') as file:
                files = {'file': (filepath, file, 'image/jpeg')}
                response = requests.post(self.base_url, files=files)
            if response.status_code == 200:
                image_embedding = response.json()
                with Session(self.engine) as session:
                    entities = (
                        session.query(self.db_entity)
                        .order_by(
                            self.db_entity.image_embedding.cosine_distance(image_embedding)
                        )
                        .limit(limit)
                        .all()
                    )
                return {"status": 200, "results": [entity.to_json() for entity in entities]}
            else:
                return {"error": response.json().get("error", "An error occurred")}
        except Exception as e:
            return {"error": str(e)}
        
