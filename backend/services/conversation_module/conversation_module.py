import os
from dotenv import load_dotenv, find_dotenv
import concurrent.futures
from premai import Prem
import json
from services.conversation_module.prompt_generator import PromptGenerator

load_dotenv(find_dotenv())

class LLMConfig:
    temperature = 0.7
    api_key = os.getenv("PREM_API_KEY")
    model = os.getenv("PREM_LLM_MODEL")
    project_id = os.getenv("PREM_PROJECT_ID")

class ConversationModule:
    def __init__(self, max_turns=5):
        self.llm_config = LLMConfig()
        self.client = Prem(api_key=self.llm_config.api_key)
        self.max_turns = max_turns
        self.message_list = []
        self.turn_count = 0
        self.system_prompt = """
        You are a chat bot that helps users to recommend clothes. Your job is to ask user questions and gather information about their preferences. Use short and concise text messages. Remember answers to the questions will be mapped to these columns:
        [
            {"column_name": "article_id", "datatype": "int64"},
            {"column_name": "prod_name", "datatype": "object"},
            {"column_name": "product_type_name", "datatype": "object"},
            {"column_name": "product_group_name", "datatype": "object"},
            {"column_name": "department_name", "datatype": "object"},
            {"column_name": "index_name", "datatype": "object"},
            {"column_name": "section_name", "datatype": "object"},
            {"column_name": "detail_desc", "datatype": "object"},
            {"column_name": "graphical_appearance_name", "datatype": "object"},
            {"column_name": "colour_group_name", "datatype": "object"},
            {"column_name": "perceived_colour_value_name", "datatype": "object"}
        ]
        After gathering sufficient information or reaching the maximum number of turns, indicate that you're ready to search for products.
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

    def reset(self):
        self.message_list = []
        self.turn_count = 0

    def converse(self, message: str):
        self.message_list.append({"role": "user", "content": message})
        self.turn_count += 1

        if self.turn_count >= self.max_turns:
            return self.end_conversation()

        llm_output = self.call_llm(self.message_list)
        assistant_message = llm_output["message"]["content"]
        self.message_list.append({"role": "assistant", "content": assistant_message})

        if "ready to search" in assistant_message.lower():
            return self.end_conversation()

        return {
            "message_list": self.message_list,
            "conversation_ended": False,
            "bot_response": assistant_message
        }

    def end_conversation(self):
        self.message_list.append({
            "role": "assistant",
            "content": "Great! I have enough information to search for products that match your preferences."
        })
        return {
            "message_list": self.message_list,
            "conversation_ended": True,
            "outputs": self.create_exit_outputs()
        }

    def call_llm(self, message):
        response = self.client.chat.completions.create(
            messages=message if isinstance(message, list) else [{"role": "user", "content": message}],
            system_prompt=self.system_prompt if isinstance(message, list) else "",
            model=self.llm_config.model,
            temperature=self.llm_config.temperature,
            project_id=self.llm_config.project_id
        )
        return response.choices[0].to_dict()
