# regulatory/llm/llm_provider.py

# import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables only once
load_dotenv()

def get_llm():
    return ChatGroq(
        model="deepseek-r1-distill-llama-70b",
        temperature=0.5  # Optional: control randomness
    )
