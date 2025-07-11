from typing import List
from regulatory.models.gspr_generator_model import GSPRGENERATORMODEL
from regulatory.prompts.gspr_generator_prompt import GSPR_GENERATOR_PROMPT
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
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
llm = ChatGroq(model="deepseek-r1-distill-llama-70b")

# llm=ChatGroq(model="deepseek-r1-distill-llama-70b")

llm = ChatOpenAI(
    model="unsloth/DeepSeek-R1-Distill-Llama-70B-bnb-4bit",
    openai_api_key="EMPTY",
    openai_api_base="http://narmada.merai.cloud:8000/v1",
    max_tokens=3200,
    temperature=0,
)

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