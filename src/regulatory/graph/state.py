# from typing import Annotated
from typing_extensions import TypedDict
from pydantic import BaseModel
from typing import List, Optional, Dict, Literal


#----------------------------------------------UserInputState-----------------------------------------------------
class UserInputState(TypedDict):
    device_type:str
    device_type: str
    intended_use: str
    intended_users: Optional[List[str]]
    components: List[str]
    region_classification:dict[str, str]

#----------------------------------------------RecommenderState-----------------------------------------------------
class RecommenderState(TypedDict):
    recommended_components:List[str]
    given_components:Optional[List[str]]

#---------------------------------------------ApplicableGSPRState---------------------------------------------------
class ApplicableGSPRState(TypedDict):
    applicable_gspr:Dict[str,Optional[List[str]]]

#------------------------------------------------GSPRState--------------------------------------------------------

class GSPRItem(BaseModel):
    design_input: str
    applicability: Literal["Applicable", "Not Applicable"]
    justification: str
    requirements: str
    standards: List[str]

class GSPRSection(BaseModel):
    # Key: GSPR ID like "GSPR1", "GSPR2"
    sections: Dict[str, GSPRItem]


class ComponentSection(BaseModel):
    # Key: Component name like "Femoral", "Tibial Tray"
    components: Dict[str, GSPRSection]


class GSPRState(BaseModel):
    gspr_content: ComponentSection

#--------------------------------------------------------------------------------------------------