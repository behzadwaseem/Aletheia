from pydantic import BaseModel, Field
from typing import List


class PreferenceRequest(BaseModel):
    item_ids: List[int] = Field(
        ...,
        min_items=1,
        description="MovieLens movie IDs selected by the user",
    )
    k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of recommendations to return",
    )
