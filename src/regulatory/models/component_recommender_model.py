from pydantic import BaseModel, Field
from typing import List

class ComponentRecommenderModel(BaseModel):
    components_list: List[str] = Field(
        description=(
            """List of recommended components for regulatory compliance, safety, and performance.
Each component is selected based on device type and use-case to ensure all relevant standards are met."""
        )
    )