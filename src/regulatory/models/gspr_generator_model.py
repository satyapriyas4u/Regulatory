# src/regulatory/models/gspr_generator_model.py

from pydantic import BaseModel, Field

class GSPRGENERATORMODEL(BaseModel):
    component: str = Field(..., description="Name of the specific device component the GSPR applies to.")
    gspr: int = Field(..., description="GSPR section number (1–23) that this input corresponds to.")
    design_input: str = Field(..., description="Specific design input or requirement related to this component and GSPR.")
    applicability: str = Field(..., description='Indicates if this GSPR is "Applicable" or "Not Applicable" to the component.')
    justification: str = Field(..., description="Rationale for applicability status, explaining why it's applicable or not.")
    requirement: str = Field(..., description="Detailed requirement derived from the GSPR applicable to the component.")
    standard: str = Field(..., description="Applicable harmonized or recognized standard that supports compliance.")
