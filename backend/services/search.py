import os
from typing import Optional

import torch
from clip import clip
from config import Settings, TiDBConfig
from dotenv import find_dotenv, load_dotenv
from PIL import Image
from sentence_transformers import SentenceTransformer
from services.tidb_connector import connect_to_tidb_engine
from sqlalchemy.orm import Session

load_dotenv(find_dotenv())


class EmbeddingSearchService:
    def __init__(
        self,
        tidb_config: Optional[TiDBConfig] = TiDBConfig(),
        settings: Optional[Settings] = Settings(),
    ) -> None:
        self.base_url = os.getenv("SEARCH_API_BASE_URL")
        self.engine, self.db_entity = connect_to_tidb_engine(tidb_config=tidb_config)

        # All the embeddings related things goes her
        self.settings = settings
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.image_embedding_model, self.image_preprocess = clip.load(
            self.settings.image_embedding_name, device=self.device
        )
        self.text_embedding_model = SentenceTransformer(
            self.settings.text_embedding_name, trust_remote_code=True
        ).to(self.device)

    def get_image_embedding(self, image_path: str):
        try:
            image = Image.open(image_path).convert("RGB")
            image_input = self.image_preprocess(image).unsqueeze(0).to(self.device)
            with torch.no_grad():
                image_features = self.image_embedding_model.encode_image(image_input)
            image_embedding = image_features / torch.Tensor(image_features).norm(
                dim=-1, keepdim=True
            )
            image_embedding = image_embedding.squeeze(0).tolist()
        except Exception as e:
            print(e)

            image_embedding = None

        return image_embedding

    def get_text_embedding(self, text: str):
        try:
            text_embedding = (
                self.text_embedding_model.encode([text]).squeeze(0).tolist()
            )

        except Exception as e:
            print(e)
            text_embedding = None

        return text_embedding

    def perform_text_search(self, query: str, limit: int):
        embedding_response = self.get_text_embedding(query)
        if isinstance(embedding_response, list):
            print("------------------------------")
            print(len(embedding_response))
            with Session(self.engine) as session:
                entities = (
                    session.query(self.db_entity)
                    .order_by(
                        self.db_entity.text_embedding.cosine_distance(
                            embedding_response
                        )
                    )
                    .limit(limit)
                    .all()
                )

            print("ALL OKAY WITH TEXT EMBEDDING SEARCH")
            return {"status": 200, "results": [entity.to_json() for entity in entities]}
        else:
            return {"status": 500, "results": []}

    def perform_image_search_from_file(self, filepath: str, limit: int):
        response = self.get_image_embedding(image_path=filepath)

        if response is None:
            return {"status": 500, "results": []}

        try:
            with Session(self.engine) as session:
                entities = (
                    session.query(self.db_entity)
                    .order_by(self.db_entity.image_embedding.cosine_distance(response))
                    .limit(limit)
                    .all()
                )
            return {"status": 200, "results": [entity.to_json() for entity in entities]}
        except Exception as e:
            print("PROBLEM WITH IMAGE EMBEDDING SEARCH")
            return {"status": 500, "error": str(e), "results": []}
