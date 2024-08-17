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
    
    def execute_query(self, query, num_of_tries=1):
        errors_list = []
        result = None
        
        for attempt in range(num_of_tries):
            cursor = self.database.cursor()
            try:
                if len(errors_list) > 0:
                    PROMPT = f"""
# TASK: Correct the following SQL statement based on the following error list.
Make sure for the SQL query generated, the 'where' clause should not exactly match for a string
as it may be slightly different, do a 'fuzzy-search' or 'contains' matching 
Make sure Never do 'SELECT *' always do 'SELECT             
article_id, prod_name, product_type_name, product_group_name, department_name,
index_name, section_name, detail_desc, graphical_appearance_name, colour_group_name,
perceived_colour_value_name'

# Latest error:
{errors_list[-1]}

# Full error List:
{json.dumps(errors_list, indent=2)}

# SQL Statement: {query}
""" + """
# Required Output Format:
{
    "sql_prompt": "query"
}
"""
                    llm_output = json.loads(self.call_llm(PROMPT))
                    query = llm_output["sql_prompt"]
                cursor.execute(query)
                result = cursor.fetchall() 
                return result
            except Exception as e:
                errors_list.append(str(e))
                if attempt < num_of_tries - 1:
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                else:
                    print(f"Attempt {attempt + 1} failed: {e}. No more retries.")
        
        return result, errors_list
        