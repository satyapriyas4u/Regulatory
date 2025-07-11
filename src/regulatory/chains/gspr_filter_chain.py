import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate
from regulatory.prompts.gspr_filter_prompt import GSPR_FILTER_PROMPT
from regulatory.models.gspr_filter_model import  GSPRStructuredResponse
# from langchain_groq import ChatGroq

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

# llm=ChatGroq(model="deepseek-r1-distill-llama-70b")

# Initialize LLM
llm = ChatOpenAI(
    model="unsloth/DeepSeek-R1-Distill-Llama-70B-bnb-4bit",
    openai_api_key="EMPTY",                       # any non‑empty string is fine
    openai_api_base="http://narmada.merai.cloud:8000/v1",
    max_tokens=3200,
    temperature=0,
)

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