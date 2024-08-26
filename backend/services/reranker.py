import os
from typing import Optional

import requests
from scipy.spatial.distance import cosine
from services.search import EmbeddingSearchService
from services.tidb_connector import TiDBConfig, connect_to_tidb_engine
from sqlalchemy.orm import Session

rerank_prompt  = """
Given the set of articles (a dict) and the description, rerank the results 
based on the similarity of the description with the query.

Here is the list of articles 

{articles}

here is what the user asked for:

{query}

Now rerank it and give me a list of top 10 articles from it.
give the list of articles in return like this:

[article1, article2, article3, article4 ....]

list of articles: 
"""

def rerank_using_llm(article_ids: list[dict]):
    pass 



class Reranker:
    def __init__(
        self,
        tidb_config: Optional[TiDBConfig] = TiDBConfig(),
        reranker_result_limit: int = 5,
    ) -> None:
        self.base_url = os.getenv("SEARCH_API_BASE_URL")
        self.engine, self.db_entity = connect_to_tidb_engine(tidb_config=tidb_config)
        self.reranker_result_limit = reranker_result_limit

    def cosine_similarity(self, vec1, vec2):
        return 1 - cosine(vec1, vec2)

    def fetch_embeddings(self, article_ids):
        with Session(self.engine) as session:
            products = (
                session.query(self.db_entity)
                .filter(self.db_entity.article_id.in_(article_ids))
                .all()
            )
            return {product.article_id: product.text_embedding for product in products}

    def rerank(
        self,
        search_service: EmbeddingSearchService,
        results: list[dict],
        query: list[str],
    ):
        ranked_products = []
        query = ", ".join(query)

        embedding_response = search_service.get_text_embedding(query)

        if embedding_response:
            article_ids = [result["article_id"] for result in results]
            embeddings_dict = self.fetch_embeddings(article_ids)

            for result in results:
                article_id = result["article_id"]
                text_embeddings = embeddings_dict.get(article_id)
                similarity = self.cosine_similarity(embedding_response, text_embeddings)
                ranked_products.append((similarity, result))

            ranked_products.sort(reverse=True, key=lambda x: x[0])
            return [
                product for _, product in ranked_products[: self.reranker_result_limit]
            ]

        return results[: self.reranker_result_limit]
