import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate
from langchain.schema.runnable import RunnableParallel
from langchain_groq import ChatGroq
import io
from dotenv import load_dotenv
from prompts.gspr_filter_prompt import GSPR_FILTER_PROMPT
from models.gspr_filter_model import  GSPRStructuredResponse

# Load environment variables
load_dotenv()



prompt = PromptTemplate(
    template=GSPR_FILTER_PROMPT,
    input_variables=[
        "device_type",
        "components",
        "intended_purpose",
        "intended_users",
        "risk_classification",
        "component_name",
    ]
)

llm=ChatGroq(model="deepseek-r1-distill-llama-70b")

gspr_filter_llm=llm.with_structured_output(GSPRStructuredResponse)

gspr_filter_chain= prompt | gspr_filter_llm


device_inputs = {
    "device_type": """Total Knee Replacement System""",

    "components": """Femoral Component""",

    "intended_purpose": """Restore knee joint function by replacing damaged articular surfaces, 
providing pain relief, mobility, and stability in patients with severe knee osteoarthritis 
or degenerative conditions.""",

    "intended_users": """Trained orthopedic surgeons in hospitals and surgical centers""",

    "regulatory_region": """EU""",
    "component_name": """Femoral Component"""
}


response = gspr_filter_chain.invoke(device_inputs)



print(f"{'GSPR':<6} {'Applicability':<15} Justification")
print("-" * 100)

for item in response.gspr_results:
    if item.GSPR == '10':
        for sub in item.Subsections:
            subsection = f"10.{sub.Subsection.split('.')[-1]}"
            print(f"{subsection:<6} {sub.Applicability:<15} {sub.Justification}")
    else:
        print(f"{item.GSPR:<6} {item.Applicability:<15} {item.Justification}")