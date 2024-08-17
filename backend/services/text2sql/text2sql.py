from dotenv import load_dotenv, find_dotenv
from premai import Prem
from .prompts import Prompts
import mysql.connector
import os
import json

load_dotenv(find_dotenv())


class LLMConfig:
    temperature = 0.7
    api_key = os.getenv("PREM_API_KEY")
    model = os.getenv("PREM_LLM_MODEL")
    project_id = os.getenv("PREM_PROJECT_ID")
    
class TiDBConfig:
    host = os.getenv('TIDB_HOST')
    port = os.getenv('TIDB_PORT')
    user = os.getenv('TIDB_USERNAME')
    password = os.getenv('TIDB_PASSWORD')
    db_name = os.getenv('TIDB_DATABASE')
    table_name = os.getenv("TIDB_TABLENAME")
    autocommit = True
    use_pure = True
    
    def to_json(self):
        config_dict = {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "database": self.db_name,
            "autocommit": self.autocommit,
            "use_pure": self.use_pure
        }
        return config_dict


class Text2SQL:
    def __init__(self):
        self.llm_config = LLMConfig()
        self.client = Prem(api_key=self.llm_config.api_key)
        
        self.db_config = TiDBConfig()
        self.database = mysql.connector.connect(
            **self.db_config.to_json()
        )
        self.prompt = Prompts(
            table_name=self.db_config.table_name,
            database=self.database
        )

    def call_llm(self, prompt):
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt},],
            model=self.llm_config.model,
            temperature=self.llm_config.temperature,
            project_id=self.llm_config.project_id
        )
        
        return response.choices[0].message.content
    
    def convert(self, query):
        llm_prompt = self.prompt(query)
        generated_output = self.call_llm(llm_prompt)
        return json.loads(generated_output)
    
    def execute_query(self):
        ...