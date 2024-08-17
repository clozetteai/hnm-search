from typing import Optional, List 
from pydantic import BaseModel, Field 

class ConversationInput(BaseModel):
    message: str 


class SearchOutput(BaseModel):
    conversation_output: dict
    products: Optional[List[dict]] = None
    total_products: Optional[int] = None
    bot_response: str
