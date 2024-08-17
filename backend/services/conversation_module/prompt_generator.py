import json


class PromptGenerator:
    def __init__(self, message_list, num_queries = 5) -> None:
        self.message_list = [f"{message['role']}: {message['content']}" for message in message_list]
        self.num_queries = num_queries
        
    def search_prompt(self):
        return f"""
# TASK: Given a conversation about a user looking for a product. Give a list of textual search queries. Make sure 
each search query should have all the things the user asked for and you may add extra variations based on user requirements

# NUMBER OF QUERIES TO BE GENERATED: {self.num_queries}

# CONVERSATION: 
{json.dumps(self.message_list, indent=2)}

# OUTPUT FORMAT:
[
    "text search query",
    ...
]
"""

    def output_prompt(self):
        PROMPT = f"""
# TASK: You are a bot that helps users to search for cloths and recommend them. The conversation between you and
user has ended, and list is at CONVERSATION. Now generate a good formal and yet fun text output for the user as
the search is completed. Also create one for when search couldn't find any data. Keep the text short and concise.

# CONVERSATION: 
{json.dumps(self.message_list, indent=2)}
"""" + """"
# OUTPUT FORMAT:
{
    "data_found_output": "output",
    "data_not_found_output": "output
}
""" 
        return PROMPT
