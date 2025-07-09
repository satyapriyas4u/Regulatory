import json
import re
from typing import List
from models.gspr_generator_model import GSPRGENERATORMODEL
from prompts.gspr_generator_prompt import GSPR_GENERATOR_PROMPT
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
# Load environment variables (e.g. GROQ_API_KEY)
load_dotenv()

# Initialize Groq LLM
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
llm = ChatGroq(model_name="deepseek-r1-distill-lzlama-70b")

gspr_generator_llm = llm.with_structured_output(GSPRGENERATORMODEL)

gspr_generator_chain = prompt | gspr_generator_llm


device_inputs={
    "device_type": "Wearable ECG Monitor",
    "intended_purpose": "Continuous heart rhythm monitoring",
    "intended_use": "Used on the wrist during physical activity",
    "region_classifications": "EU",
    "component": "Sensor",
    "gspr": "1"
}

response = gspr_generator_chain.invoke(device_inputs)

print(response)















