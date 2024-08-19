import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ASSET_PATH = Path(os.getcwd()) / "assets"
ALL_ASSETS = [
    f for f in os.listdir(ASSET_PATH) if f.endswith((".jpeg", ".jpg", ".png"))
]

TABLE_COLUMNS = [
    "article_id",
    # name of the product section
    "prod_name",
    "product_type_name",
    "product_group_name",
    # Department
    "department_name",
    "index_name",
    "section_name",
    # Detail Desc
    "detail_desc",
    # Color section
    "graphical_appearance_name",
    "colour_group_name",
    "perceived_colour_value_name",
]


class TiDBConfig:
    host = os.getenv("TIDB_HOST")
    port = os.getenv("TIDB_PORT")
    user = os.getenv("TIDB_USERNAME")
    password = os.getenv("TIDB_PASSWORD")
    db_name = os.getenv("TIDB_DATABASE")
    table_name = os.getenv("TIDB_TABLENAME")
    autocommit = True
    use_pure = True
    image_embedding_dim = 512
    text_embedding_dim = 1024

    def to_json(self):
        config_dict = {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "database": self.db_name,
            "autocommit": self.autocommit,
            "use_pure": self.use_pure,
            "text_embedding_dim": self.text_embedding_dim,
            "image_embedding_dim": self.image_embedding_dim,
        }
        return config_dict


class LLMConfig:
    temperature = 0.7
    api_key = os.getenv("PREMAI_API_KEY")
    model = os.getenv("PREM_LLM_MODEL")
    project_id = os.getenv("PREM_PROJECT_ID")

    def to_json(self):
        return {
            "temperature": self.temperature,
            "api_key": self.api_key,
            "model": self.model,
            "project_id": self.project_id,
        }


class Settings:
    message_history_length: int = 3
    num_customer_queries: int = 3
    start_page_catalouge_length: int = 100
    image_search_limit: int = 50
    text_search_limit: int = 50
    text2sql_num_tries: int = 3
