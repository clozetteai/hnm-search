# Author: Anidyadeep Sanigrahi https://github.com/Anindyadeep

import json
import mysql.connector
from textwrap import dedent
from premai import Prem
from typing import Optional
from services.text2sql.prompts import Text2SQLPrompts
from config import LLMConfig, TiDBConfig

from dotenv import load_dotenv, find_dotenv
from config import TABLE_COLUMNS, Settings

load_dotenv(find_dotenv())


class Text2SQLCandidateGenerator:
    def __init__(
        self,
        llm_config: Optional[LLMConfig] = LLMConfig(),
        tidb_config: Optional[TiDBConfig] = TiDBConfig(),
        settings: Optional[Settings] = Settings(),
    ) -> None:
        self.llm_config = llm_config
        self.client = Prem(api_key=self.llm_config.api_key)

        self.database = mysql.connector.connect(
            **{
                "host": tidb_config.host,
                "port": tidb_config.port,
                "user": tidb_config.user,
                "password": tidb_config.password,
                "database": tidb_config.db_name,
                "autocommit": tidb_config.autocommit,
                "use_pure": tidb_config.use_pure,
            }
        )
        self.prompt = Text2SQLPrompts(
            table_name=tidb_config.table_name, database=self.database
        )
        self.settings = settings

    def call_llm(self, prompt):
        response = self.client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt},
            ],
            model=self.llm_config.model,
            temperature=self.llm_config.temperature,
            project_id=self.llm_config.project_id,
        )
        return response.choices[0].message.content

    def convert(self, query):
        llm_prompt = self.prompt(query)
        generated_output = self.call_llm(llm_prompt)
        return json.loads(generated_output)

    def execute_query(self, query):
        errors_list = []
        result = None

        for attempt in range(self.settings.text2sql_num_tries):
            cursor = self.database.cursor()
            try:
                if len(errors_list) > 0:
                    PROMPT = dedent(
                        f"""
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
                    """
                        + """
                    # Required Output Format:
                    {
                        "sql_prompt": "query"
                    }
                    """
                    )
                    llm_output = json.loads(self.call_llm(PROMPT))
                    query = llm_output["sql_prompt"]
                cursor.execute(query)
                results = cursor.fetchall()
                results = [dict(zip(TABLE_COLUMNS, result)) for result in results]
                return results, None
            except Exception as e:
                print("Retrying ...")
                errors_list.append(str(e))
                if attempt < self.settings.text2sql_num_tries - 1:
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                else:
                    print(f"Attempt {attempt + 1} failed: {e}. No more retries.")

        return result, errors_list
