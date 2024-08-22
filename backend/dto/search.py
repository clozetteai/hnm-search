

from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class SearchPayload(BaseModel):
    customer_message: Optional[str] = None
    attached_image: Optional[str] = None  

class SearchResponse(BaseModel):
    bot_message: str
    is_catalouge_changed: bool
    catalouge: List[Dict[str, Any]]