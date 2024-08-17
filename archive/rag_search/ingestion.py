from tqdm import tqdm
from typing import Union 
from fastembed.sparse.bm25 import BM25
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from fastembed.late_interaction import LateInteractionTextEmbedding


class HandMDataIngestionService:
    def __init__(self, config: dict) -> None:
        self.config = config
        self.collection_name = config["collection_name"]
        self.collection_uri = config["collection_uri"]
        self.qdrant_client = QdrantClient(self.collection_uri)
        
        # Initialize the collection
        # This part is wrong, we need to check the way config is defned.

        if self.qdrant_client.collection_exists(self.collection_name):
            self.qdrant_client.use_collection(self.collection_name)
        else:
            self.qdrant_client.create_collection(
                self.collection_name,
                vectors_config={
                    self.config["dense_embedding"]["alias"]: models.VectorParams(
                        size=self.config["dense_embedding"]["size"],
                        distance=models.Distance.COSINE,
                    ),
                    self.config["late_interaction"]["alias"]: models.VectorParams(
                        size=self.config["late_interaction"]["size"],
                        distance=models.Distance.COSINE,
                        multivector_config=models.MultiVectorConfig(
                            comparator=models.MultiVectorComparator.MAX_SIM,
                        ),
                    ),
                },
                sparse_vectors_config={
                    self.config["sparse_embedding"]["alias"]: models.SparseVectorParams(
                        modifier=models.Modifier.IDF,
                    ),
                }
            )
        
        # Initialize different embedding models
        self.embedding_model = SentenceTransformer(
            self.config["dense_embedding"]["model_name"]
        )
    
    def update_point(self, id: int):
        raise NotImplementedError
    
    def delete_point(self, id: int):
        raise NotImplementedError
    
    def upload_points_from_csv(self, csv_path: str):
        raise NotImplementedError
    
    def upload_points(self, data: Union[list[dict], dict]):
        raise NotImplementedError
