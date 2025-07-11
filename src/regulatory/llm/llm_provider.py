# regulatory/llm/llm_provider.py

# import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.llms.vllm import VLLMOpenAI

# Load environment variables only once
load_dotenv()

def get_groq_llm():
    """    Returns a ChatGroq instance configured for the DeepSeek model.
    """
    return ChatGroq(
        model="deepseek-r1-distill-llama-70b",
        temperature=0.5  # Optional: control randomness
    )

def get_vllm_llm():
    """
    Returns a ChatOpenAI instance configured for the DeepSeek model.
    """
    # If you want to use Groq instead, you can return get_groq_llm() here.
    return VLLMOpenAI(
        model="unsloth/DeepSeek-R1-Distill-Llama-70B-bnb-4bit",
        temperature=0.5,
        max_tokens=4096,
        api_key="dummy",
        base_url="http://narmada.merai.cloud:8000/v1",
)