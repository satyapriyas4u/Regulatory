import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain.schema.runnable import RunnableParallel
from langchain_groq import ChatGroq
import io
from dotenv import load_dotenv
from regulatory.prompts.component_recommender_prompt import COMPONENT_RECOMMENDER_PROMPT
from regulatory.models.component_recommender_model import ComponentRecommenderModel

# Load environment variables
load_dotenv()

prompt = PromptTemplate(
    template=COMPONENT_RECOMMENDER_PROMPT,
    input_variables=[
        "device_type",
        "components",
        "intended_purpose",
        "intended_users",
        "risk_classification"
    ]
)

llm=ChatGroq(model="deepseek-r1-distill-llama-70b")

component_recommender_llm=llm.with_structured_output(ComponentRecommenderModel)

component_recommender_chain= prompt | component_recommender_llm


device_inputs = {
    "device_type": """Total Knee Replacement System, comprising femoral component, tibial tray, tibial insert, 
patellar component, fixation elements (screws, pegs, stems), and optional augments/spacers, 
constructed from MoCs such as CoCrMo, titanium alloys, UHMWPE, and ceramics, 
with optional coatings (e.g., hydroxyapatite, titanium plasma spray).""",

    "components": """o Femoral Component (Condyles): CoCrMo, titanium alloy, or ceramic, coated or uncoated.
o Tibial Tray: Titanium alloy or CoCrMo, coated or uncoated.
o Tibial Insert: UHMWPE, fixed or mobile-bearing.
o Patellar Component (Button): UHMWPE or ceramic.
o Fixation Elements (Screws, Pegs, Stems): Titanium alloy or CoCrMo, coated or uncoated.
o Augments/Spacers: Titanium alloy, CoCrMo, or UHMWPE, for bone defects or alignment.""",

    "intended_purpose": """Restore knee joint function by replacing damaged articular surfaces, 
providing pain relief, mobility, and stability in patients with severe knee osteoarthritis 
or degenerative conditions.""",

    "intended_users": """Trained orthopedic surgeons in hospitals and surgical centers""",

    "regulatory_region": """EU"""
}


response = component_recommender_chain.invoke(device_inputs)
print(response)