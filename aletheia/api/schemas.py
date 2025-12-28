from pydantic import BaseModel, Field
from typing import List

class PreferenceRequest(BaseModel):
    item_ids: List[int] = Field(..., min_items=1)
    k: int = 5