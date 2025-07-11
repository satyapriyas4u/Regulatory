# regulatory/llm/llm_provider.py

# import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

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
    return ChatOpenAI(
        model="unsloth/DeepSeek-R1-Distill-Llama-70B-bnb-4bit",
        api_key=None,  # Set your API key if needed
        base_url="http://narmada.merai.cloud:8000/v1",  # Use the full base URL
        temperature=0,
    )
