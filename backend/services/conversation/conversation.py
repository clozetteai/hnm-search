import concurrent.futures
import json
from typing import Optional

from config import LLMConfig
from dotenv import find_dotenv, load_dotenv
from premai import Prem
from services.conversation.prompts import *

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
        self.search_queries = []
        self.system_prompt = CONVERSATION_SYSTEM_PROMPT
        self.num_customer_queries = num_customer_queries

    def _generate_converse_output(self, chat_intent: bool):
        pg = PromptGenerator(self.message_list, num_queries=self.num_customer_queries)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_bot_output = executor.submit(self.call_llm, pg.output_prompt())
            chat_intent = True if chat_intent == "true" else False

            if not chat_intent:
                future_search_query = executor.submit(self.call_llm, pg.search_prompt())
                self.search_queries = eval(
                    future_search_query.result()["message"]["content"]
                )
            print(self.search_queries if not chat_intent else [])
            return {
                "bot_output": eval(future_bot_output.result()["message"]["content"]),
                "search_query": self.search_queries if not chat_intent else [],
            }

    def intent_classifier(self, query):
        output = self.call_llm(get_intent_prompt(query))
        intent = output["message"]["content"]
        return intent

    def reset(self):
        self.message_list = []

    def converse(self, message: str):
        self.message_list.append({"role": "user", "content": message})
        chat_intent = eval(self.intent_classifier(message))

        print(type(chat_intent), chat_intent)

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
            "outputs": self._generate_converse_output(chat_intent["chat"]),
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
