# File: src/regulatory/chains/component_recommender_chain.py

import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnableParallel
from regulatory.prompts.component_recommender_prompt import COMPONENT_RECOMMENDER_PROMPT
from regulatory.models.component_recommender_model import ComponentRecommenderModel
from regulatory.llm.llm_provider import get_groq_llm, get_vllm_llm


# Updated prompt with only device_type and intended_purpose
prompt = PromptTemplate(
    template=COMPONENT_RECOMMENDER_PROMPT,
    input_variables=["device_type", "intended_purpose"]
)

# Load the model
llm = get_groq_llm()

llm = ChatOpenAI(
    model="unsloth/DeepSeek-R1-Distill-Llama-70B-bnb-4bit",
    openai_api_key="EMPTY",
    openai_api_base="http://narmada.merai.cloud:8000/v1",
    max_tokens=7100,
    temperature=0,
)

# Chain
component_recommender_chain = prompt | component_recommender_llm

async def main():
    device_inputs = {
        "device_type": "Total Knee Replacement System",
        "intended_purpose": "Restore knee joint function by replacing damaged articular surfaces to relieve pain and improve mobility in patients with severe osteoarthritis."
    }

    response = await component_recommender_chain.ainvoke(device_inputs)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())


# Run the script to test the component recommender chain
# python -m regulatory.chains.component_recommender_chain or
# uv run -m regulatory.chains.component_recommender_chain