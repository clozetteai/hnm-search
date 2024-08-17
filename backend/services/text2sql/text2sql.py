from dotenv import load_dotenv, find_dotenv
from premai import Prem
from .prompts import Prompts
from .utils import load_sqlite_db
import os
import json

load_dotenv(find_dotenv())


class LLMConfig:
    temperature = 0.7
    api_key = os.getenv("PREM_API_KEY")
    model = os.getenv("PREM_LLM_MODEL")
    project_id = os.getenv("PREM_PROJECT_ID")

class Text2SQL:
    def __init__(self, table_name, sqlite_path):
        self.llm_config = LLMConfig()
        self.client = Prem(api_key=self.llm_config.api_key)
        self.database = load_sqlite_db(sqlite_path)
        self.prompt = Prompts(
            table_name=table_name,
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
    
    def __call__(self, query):
        llm_prompt = self.prompt(query)
        generated_output = self.call_llm(llm_prompt)
        return json.loads(generated_output)