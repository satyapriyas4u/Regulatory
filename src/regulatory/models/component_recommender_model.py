from pydantic import BaseModel, Field
from typing import List

class ComponentRecommenderModel(BaseModel):
    components_list: List[str] = Field(
        description="A list of recommended additional components essential for regulatory compliance, device safety, and performance based on the input device type and use-case."
    )