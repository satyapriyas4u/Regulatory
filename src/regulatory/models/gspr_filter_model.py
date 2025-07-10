from typing import List, Union, Literal
from pydantic import BaseModel, Field


class GSPRSubsection(BaseModel):
    Subsection: Literal["10.1", "10.2", "10.3", "10.4"] = Field(
        description="The specific subsection of GSPR 10 being evaluated."
    )
    Applicability: Literal["Applicable", "Not Applicable"] = Field(
        description="Whether this specific subsection is applicable to the device/component."
    )
    Justification: str = Field(
        description="Explanation for why this subsection is applicable or not."
    )


class GSPRWithSubsections(BaseModel):
    GSPR: Literal["10"] = Field(
        description="GSPR section 10 which has nested subsections (10.1-10.4)."
    )
    Subsections: List[GSPRSubsection] = Field(
        description="List of evaluations for each subsection under GSPR section 10."
    )


class GSPRItem(BaseModel):
    GSPR: str = Field(
        description="The number of the GSPR section (excluding 10). Example: '1', '2', ..., '9', '11', ..., '23'."
    )
    Applicability: Literal["Applicable", "Not Applicable"] = Field(
        description="Whether this GSPR section is applicable to the device/component."
    )
    Justification: str = Field(
        description="Explanation for why the GSPR section is applicable or not."
    )


class GSPRStructuredResponse(BaseModel):
    gspr_results: List[Union[GSPRItem, GSPRWithSubsections]] = Field(
        description="Structured evaluation of all GSPR sections with applicability and justification."
    )