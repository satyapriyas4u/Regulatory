from typing import List
from regulatory.models.gspr_generator_model import GSPRGENERATORMODEL
from regulatory.prompts.gspr_generator_prompt import GSPR_GENERATOR_PROMPT
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()

prompt=PromptTemplate(
    template=GSPR_GENERATOR_PROMPT,
    input_variables=[
        "device_type",
        "intended_purpose",
        "intended_use",
        "region_classifications",
        "component",
        "gspr"]
   )

# llm=ChatGroq(model="deepseek-r1-distill-llama-70b")

llm = ChatOpenAI(
    model="unsloth/DeepSeek-R1-Distill-Llama-70B-bnb-4bit",
    openai_api_key="EMPTY",
    openai_api_base="http://narmada.merai.cloud:8000/v1",
    max_tokens=7100,
    temperature=0,
)

gspr_generator_llm = llm.with_structured_output(GSPRGENERATORMODEL)

gspr_generator_chain = prompt | gspr_generator_llm















'''

import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate
from langchain.schema.runnable import RunnableParallel
from langchain_groq import ChatGroq
import io
from dotenv import load_dotenv
from prompts.gspr_filter_prompt import GSPR_FILTER_PROMPT
from models.gspr_filter_model import  GSPRStructuredResponse
from langchain_community.llms import VLLMOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.output_parsers import OutputFixingParser
# Load environment variables
load_dotenv()

parser = PydanticOutputParser(pydantic_object=GSPRStructuredResponse)

prompt = PromptTemplate(
    template=GSPR_FILTER_PROMPT,
    input_variables=[
        "device_type",
        "components",
        "intended_purpose",
        "intended_users",
        "risk_classification",
        "component_name",
    ],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)
# deepseek-r1-distill-llama-70b
# llm=ChatGroq(model="deepseek-r1-distill-llama-70b")
llm = ChatOpenAI(
    model="unsloth/DeepSeek-R1-Distill-Llama-70B-bnb-4bit",
    openai_api_key="EMPTY",                       # any non‑empty string is fine
    openai_api_base="http://narmada.merai.cloud:8000/v1",
    max_tokens=7100,
    temperature=0,
)
# gspr_filter_llm=llm.with_structured_output(GSPRStructuredResponse)
fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)

gspr_filter_chain= prompt | llm | fixing_parser




'''

'''

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

print(response)

print(f"{'GSPR':<6} {'Applicability':<15} Justification")
print("-" * 100)

for item in response.gspr_results:
    if item.GSPR == '10':
        for sub in item.Subsections:
            subsection = f"10.{sub.Subsection.split('.')[-1]}"
            print(f"{subsection:<6} {sub.Applicability:<15} {sub.Justification}")
    else:
        print(f"{item.GSPR:<6} {item.Applicability:<15} {item.Justification}")


'''
