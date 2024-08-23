import os
from typing import Optional

import torch
from clip import clip
from config import Settings
from PIL import Image
from sentence_transformers import SentenceTransformer


class Embeddings:
    def __init__(self, settings: Optional[Settings] = Settings()) -> None:
        self.settings = settings
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.image_embedding_model, self.image_preprocess = clip.load(
            self.settings.image_embedding_name, device=self.device
        )
        self.text_embedding_model = SentenceTransformer(
            self.settings.text_embedding_name, trust_remote_code=True
        ).to(self.device)

    def get_image_embedding(self, image_path: str):
        image = Image.open(image_path).convert("RGB")
        image_input = self.image_preprocess(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            image_features = self.image_embedding_model.encode_image(image_input)
        image_embedding = image_features / torch.Tensor(image_features).norm(
            dim=-1, keepdim=True
        )
        return image_embedding.cpu().numpy().tolist()

    def get_text_embedding(self, text: str):
        text_embedding = self.text_embedding_model.encode(str(text)).tolist()
        return text_embedding
