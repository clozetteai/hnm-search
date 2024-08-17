import os
from .prompt_generator import PromptGenerator
from dotenv import load_dotenv, find_dotenv
import concurrent.futures
from premai import Prem
import json

load_dotenv(find_dotenv())


class LLMConfig:
    temperature = 0.7
    api_key = os.getenv("PREM_API_KEY")
    model = os.getenv("PREM_LLM_MODEL")
    project_id = os.getenv("PREM_PROJECT_ID")

class ConversationModule:
    def __init__(self, message_length) -> None:
        self.llm_config = LLMConfig()
        self.client = Prem(api_key=self.llm_config.api_key)
        self.message_length = message_length
        self.message_list = []
        self.system_prompt = """
You are a chat bot that helps users to recommend clothes. You job is to ask user questions only and not recommend anything, 
related to their query. Use short and concise text messages. Remember answers to the questions will be mapped to these columns
So try to ask question from this only
[
    {
        "column_name": "article_id",
        "datatype": "int64"
    },
    {
        "column_name": "product_code",
        "datatype": "float64"
    },
    {
        "column_name": "prod_name",
        "datatype": "object"
    },
    {
        "column_name": "product_type_no",
        "datatype": "float64"
    },
    {
        "column_name": "product_type_name",
        "datatype": "object"
    },
    {
        "column_name": "product_group_name",
        "datatype": "object"
    },
    {
        "column_name": "graphical_appearance_no",
        "datatype": "float64"
    },
    {
        "column_name": "graphical_appearance_name",
        "datatype": "object"
    },
    {
        "column_name": "colour_group_code",
        "datatype": "float64"
    },
    {
        "column_name": "colour_group_name",
        "datatype": "object"
    },
    {
        "column_name": "perceived_colour_value_id",
        "datatype": "float64"
    },
    {
        "column_name": "perceived_colour_value_name",
        "datatype": "object"
    },
    {
        "column_name": "perceived_colour_master_id",
        "datatype": "float64"
    },
    {
        "column_name": "perceived_colour_master_name",
        "datatype": "object"
    },
    {
        "column_name": "department_no",
        "datatype": "float64"
    },
    {
        "column_name": "department_name",
        "datatype": "object"
    },
    {
        "column_name": "index_code",
        "datatype": "object"
    },
    {
        "column_name": "index_name",
        "datatype": "object"
    },
    {
        "column_name": "index_group_no",
        "datatype": "float64"
    },
    {
        "column_name": "index_group_name",
        "datatype": "object"
    },
    {
        "column_name": "section_no",
        "datatype": "float64"
    },
    {
        "column_name": "section_name",
        "datatype": "object"
    },
    {
        "column_name": "garment_group_no",
        "datatype": "float64"
    },
    {
        "column_name": "garment_group_name",
        "datatype": "object"
    },
    {
        "column_name": "detail_desc",
        "datatype": "object"
    }
]
"""
        
    def create_exit_outputs(self):
        pg = PromptGenerator(self.message_list)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_bot_output = executor.submit(self.call_llm, pg.output_prompt())
            future_search_query = executor.submit(self.call_llm, pg.search_prompt())

            return {
                "bot_output": json.loads(future_bot_output.result()["message"]["content"]),
                "search_query": json.loads(future_search_query.result()["message"]["content"])
            }
    
    def converse(self, message: str):
        self.message_list.append({
            "role": "user",
            "content": message
        })
        
        if (len(self.message_list) == (self.message_length * 2) - 1):
            self.message_list.append({
                "role": "assistant",
                "content": "Lemme search, we might have something!"
            })
            
            return {
                "message_list": self.message_list,
                "conversation_ended": True,
                "outputs": self.create_exit_outputs()
            }
            
        llm_output = self.call_llm(self.message_list)
        self.message_list.append({
            "role": llm_output["message"]["role"],
            "content": llm_output["message"]["content"]
        })
        return {
            "message_list": self.message_list,
            "conversation_ended": False
        }
        
        
    def call_llm(self, message):
        response = self.client.chat.completions.create(
            messages=message if type(message) == list else [{"role": "user", "content": message}],
            system_prompt=self.system_prompt if type(message) == list else "",
            model=self.llm_config.model,
            temperature=self.llm_config.temperature,
            project_id=self.llm_config.project_id
        )
        
        return response.choices[0].to_dict()