from typing import Optional, List, Dict, Any
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from services.conversation.conversation import ConversationModule
from services.text2sql.retriever import Text2SQLCandidateGenerator
from services.search import EmbeddingSearchService
from services.catalouge import get_default_catalog
from config import LLMConfig, Settings
from services.tidb_connector import connect_to_tidb_engine, TiDBConfig
# from tidb_connector import connect_to_tidb_engine, TiDBConfig

load_dotenv(find_dotenv())

class OutputSchema(BaseModel):
    bot_message: str
    is_catalouge_changed: bool
    catalouge: List[Dict[str, Any]]

class WorkFlow:
    def __init__(
        self,
        llm_config: Optional[LLMConfig] = LLMConfig(),
        tidb_config: Optional[TiDBConfig] = TiDBConfig(),
        settings: Optional[Settings] = Settings(),
    ) -> None:
        self.llm_config, self.tidb_config, self.settings = llm_config, tidb_config, settings

        self.conversation_module = ConversationModule(
            llm_config=llm_config,
            history_length=self.settings.message_history_length,
            num_customer_queries=self.settings.num_customer_queries,
        )

        self.engine, self.HandMProductEntity = connect_to_tidb_engine(tidb_config)
        self.search = EmbeddingSearchService(tidb_config=tidb_config)

        self.text2sql = Text2SQLCandidateGenerator(
            llm_config=llm_config, tidb_config=tidb_config
        )

        self.catalouge_state = self.get_default_catalog()

        self.message_list = self.conversation_module.message_list

    def get_default_catalog(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        try:
            default_catalog = session.query(self.HandMProductEntity).limit(self.settings.start_page_catalouge_length).all()
            return [product.to_json() for product in default_catalog]
        finally:
            session.close()

    def run(self, payload: dict) -> OutputSchema:
        customer_message = payload.get("customer_message")
        attached_image = payload.get("attached_image")
        response_from_image, response_from_text = [], []
        final_output_response = "Here is what I found ..."
        is_catalouge_changed = False

        if customer_message:
            refined_message = self.conversation_module.converse(message=customer_message)
            bot_message = refined_message["outputs"]["bot_output"]
            text_search_queries = refined_message["outputs"]["search_query"]

            final_output_response = f"{bot_message['data_found_output']} and {bot_message['data_not_found_output']}"
            self.message_list = refined_message["message_list"]

            if text_search_queries:
                from_text_embedding_search = self.search.perform_text_search(
                    query=", ".join(text_search_queries),
                    limit=self.settings.text_search_limit,
                )
                response_from_text = from_text_embedding_search["results"]
                sql_response = []
                for query in text_search_queries:
                    sql_query = self.text2sql.convert(query)
                    result, error_list = self.text2sql.execute_query(sql_query["sql_prompt"])
                    if error_list is None:
                        sql_response.extend(result)

                print(f"Done text2sql, got {len(sql_response)} results")

                response_from_text = response_from_text + sql_response
                if self.catalouge_state != response_from_text:
                    is_catalouge_changed = True

        if attached_image:
            response_from_image = self.search.perform_image_search_from_bs64(
                image_bs64=attached_image, limit=self.settings.image_search_limit
            )["results"]

            is_catalouge_changed = True

        article_set_before_reranking = response_from_image + response_from_text
        unique_articles_dict = {
            article["article_id"]: article for article in article_set_before_reranking
        }

        unique_articles_list = list(unique_articles_dict.values())

        if self.catalouge_state != unique_articles_list:
            is_catalouge_changed = True
            self.catalouge_state = unique_articles_list

        return OutputSchema(
            bot_message=final_output_response,
            is_catalouge_changed=is_catalouge_changed,
            catalouge=self.catalouge_state,
        )