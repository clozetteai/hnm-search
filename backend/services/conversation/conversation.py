# Author: Anidyadeep Sanigrahi https://github.com/Anindyadeep

from typing import Optional
from dotenv import load_dotenv, find_dotenv
import concurrent.futures
from premai import Prem
import json
from services.conversation.prompts import PromptGenerator, CONVERSATION_SYSTEM_PROMPT
from config import LLMConfig

load_dotenv(find_dotenv())


class ConversationModule:
    def __init__(
        self,
        llm_config: Optional[LLMConfig] = LLMConfig,
        history_length: Optional[int] = 5,
        num_customer_queries: Optional[int] = 3,
    ) -> None:
        self.llm_config = llm_config
        self.history_length = history_length * 2
        self.client = Prem(api_key=self.llm_config.api_key)
        self.message_list = []
        self.system_prompt = CONVERSATION_SYSTEM_PROMPT
        self.num_customer_queries = num_customer_queries

    def _generate_converse_output(self):
        pg = PromptGenerator(self.message_list, num_queries=self.num_customer_queries)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_bot_output = executor.submit(self.call_llm, pg.output_prompt())
            future_search_query = executor.submit(self.call_llm, pg.search_prompt())

            return {
                "bot_output": json.loads(
                    future_bot_output.result()["message"]["content"]
                ),
                "search_query": json.loads(
                    future_search_query.result()["message"]["content"]
                ),
            }

    def reset(self):
        self.message_list = []

    def converse(self, message: str):
        self.message_list.append({"role": "user", "content": message})

        llm_output = self.call_llm(self.message_list)
        self.message_list.append(
            {
                "role": llm_output["message"]["role"],
                "content": llm_output["message"]["content"],
            }
        )
        return {
            "message_list": self.message_list,
            "conversation_ended": False,
            "outputs": self._generate_converse_output(),
        }

    def call_llm(self, messages):
        response = self.client.chat.completions.create(
            messages=(
                messages[: self.history_length]
                if type(messages) == list
                else [{"role": "user", "content": messages}]
            ),
            system_prompt=self.system_prompt if type(messages) == list else "",
            model=self.llm_config.model,
            temperature=self.llm_config.temperature,
            project_id=self.llm_config.project_id,
        )

        return response.choices[0].to_dict()
