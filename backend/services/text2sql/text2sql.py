import sqlite3
from premai import Prem
import json

class LLMConfig:
    api_key = "Y4tQJcHDFumZJwIQeiEDBbbet9YCEcpWkF"
    model = "gpt-3.5-turbo"
    temperature = 0.7
    project_id="5588"

class Text2SQL:
    def __init__(self):
        # self.connection = sqlite3.connect("")
        # self.cursor = self.connection.cursor()
        self.llm_config = LLMConfig()
        self.client = Prem(api_key=self.llm_config.api_key)
        

    def call_llm(self, prompt):
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt},],
            model=self.llm_config.model,
            temperature=self.llm_config.temperature,
            project_id=self.llm_config.project_id
        )
        
        return response.choices[0].message.content