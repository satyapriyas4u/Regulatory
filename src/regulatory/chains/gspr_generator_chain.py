import json
import re
from typing import List
from ..models.gspr_generator_model import GSPRGENERATORMODEL
from ..prompts.gspr_generator_prompt import GSPR_GENERATOR_PROMPT
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

# Load environment variables (e.g. GROQ_API_KEY)
load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(model_name="deepseek-r1-distill-llama-70b")


def extract_json_string(text: str) -> str:
    """Extract the first valid JSON object from a possibly noisy LLM response."""
    # Remove <think> sections
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    # Try to extract content from ```json blocks
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    if match:
        return match.group(1)

    # Fallback: try to find the first standalone JSON object
    match = re.search(r"(\{.*?\})", text, flags=re.DOTALL)
    if match:
        return match.group(1)

    return ""


def generate_applicable_gspr_entries(device_metadata: dict, recommended_components: dict) -> List[GSPRGENERATORMODEL]:
    results = []

    for component, details in recommended_components.items():
        for gspr_num in details.get("gsprs", []):
            # Format the prompt
            prompt = GSPR_GENERATOR_PROMPT.format(
                device_type=device_metadata["device_type"],
                intended_purpose=device_metadata["intended_purpose"],
                intended_use=device_metadata["intended_use"],
                risk_classifications=device_metadata["risk_classifications"],
                component=component,
                gspr=gspr_num
            )
            print(f"\n[INFO] Generating GSPR entry for Component: {component}, GSPR: {gspr_num}")
            print(f"[PROMPT]:\n{prompt}")


            try:
                messages = [
                    SystemMessage(content="You are a regulatory compliance assistant."),
                    HumanMessage(content=prompt)
                ]
                response = llm.invoke(messages)
                llm_response = response.content.strip()

                print(f"[LLM RESPONSE]:\n{llm_response}")

                # Clean and parse JSON from response
                clean_json = extract_json_string(llm_response)

                if not clean_json:
                    raise ValueError("No valid JSON content found in LLM response")

                content = json.loads(clean_json)

                gspr_entry = GSPRGENERATORMODEL(
                    component=component,
                    gspr=gspr_num,
                    design_input=content["design_input"],
                    applicability="Applicable",
                    justification=content["justification"],
                    requirement=content["requirement"],
                    standard=content["standard"]
                )
                results.append(gspr_entry)
                print(f"[SUCCESS] Added GSPR entry for {component} - GSPR {gspr_num}")

            except Exception as e:
                print(f"[ERROR] Component: {component}, GSPR: {gspr_num}, Reason: {e}")
                continue

    return results


if __name__ == "__main__":
    # Sample test input
    device_metadata = {
        "device_type": "Wearable ECG Monitor",
        "intended_purpose": "Continuous heart rhythm monitoring",
        "intended_use": "Used on the wrist during physical activity",
        "risk_classifications": {
            "EU": "Class IIa",
            "US": "Class II",
            "IND": "Class B"
        }
    }

    recommended_components = {
        "Sensor": {
            "gsprs": [1, 5],
            
        },

        "Display": {
            "gsprs": [3],
            
        }
    }

    results = generate_applicable_gspr_entries(device_metadata, recommended_components)

    # Print each result in JSON format
    if results:
        print("\n\n Final Generated GSPR Entries:")
        for entry in results:
            print(entry.model_dump_json(indent=2))

    else:
        print("\n No valid GSPR entries were generated.")
