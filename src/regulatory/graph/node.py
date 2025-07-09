from typing import Any
from langchain_core.runnables import RunnableLambda
from state import GlobalState
import json

# Import your chains and models
from chains.component_recommender_chain import component_recommender_chain
from models.component_recommender_model import ComponentRecommenderModel
from models.gspr_filter_model import GSPRStructuredResponse, GSPRWithSubsections, GSPRItem

# Also import your gspr_filter_chain
from chains.gspr_filter_chain import gspr_filter_chain
# --------------------------------------------------------------------------------
# 📦 Node 1: Load user input from prompt.txt
def user_input_node(state: GlobalState) -> GlobalState:
    """
    Reads device input JSON from 'prompt.txt' and populates GlobalState['user_input'].
    Also initializes 'given_components'.
    """
    with open("prompt.txt", "r") as f:
        data = json.load(f)
    
    state["user_input"] = {
        "device_type": data.get("device_type", ""),
        "intended_use": data.get("intended_use", ""),
        "intended_users": data.get("intended_users", []),
        "components": data.get("components", []),
        "region_classification": data.get("region_classification", "")
    }

    # Save original components
    state["recommender"]["given_components"] = data.get("components", [])

    print("✅ Loaded user input:")
    print(json.dumps(state["user_input"], indent=2))
    return state


# --------------------------------------------------------------------------------
# 🔍 Node 2: Recommend additional components
def component_recommender_node(state: GlobalState) -> GlobalState:
    user_input = state["user_input"]

    chain_input = {
        "device_type": user_input["device_type"],
        "components": "\n".join(user_input["components"]),
        "intended_purpose": user_input["intended_use"],
        "intended_users": ", ".join(user_input.get("intended_users") or []),
        "risk_classification": user_input["region_classification"]
    }

    print("📦 Input to component recommender chain:")
    print(json.dumps(chain_input, indent=2))

    # Run the LLM chain
    response = component_recommender_chain.invoke(chain_input)
    print("📝 Raw LLM response:", response)

    # Validate & parse response
    if not isinstance(response, dict):
        raise TypeError("Response from component_recommender_chain must be a dict.")
    if "components_list" not in response:
        raise KeyError("Response missing 'components_list'.")

    model = ComponentRecommenderModel(**response)
    print("✅ Recommended Components:", model.components_list)

    # Store back to state
    state["recommender"]["recommended_components"] = model.components_list
    state["user_input"]["components"].extend(model.components_list)

    return state


# 
# 🏗️ Node 3: Filter applicable GSPR
from typing import cast
from typing import cast
from graph.state import ApplicableGSPRState



def gspr_filter_node(state: GlobalState, component_name: str) -> GlobalState:
    """
    Node to filter applicable GSPRs for a single component.
    Runs the gspr_filter_chain LLM, parses the structured response,
    flattens it into applicable GSPR ids, and updates the global state.
    """
    user_input = state["user_input"]

    # Prepare input for the LLM chain
    chain_input = {
        "device_type": user_input["device_type"],
        "components": "\n".join(user_input["components"]),
        "intended_purpose": user_input["intended_use"],
        "intended_users": ", ".join(user_input.get("intended_users") or []),
        "risk_classification": user_input["region_classification"],
        "component_name": component_name
    }

    print(f"\n🔍 Running GSPR filter for component: {component_name}")
    response = gspr_filter_chain.invoke(chain_input)
    print("📝 Raw LLM response:", response)

    # Validate and parse with Pydantic model
    if not isinstance(response, dict):
        raise ValueError(f"Expected dict response from gspr_filter_chain, got {type(response)}")
    structured = GSPRStructuredResponse(**response)
    print("✅ Parsed structured response for:", component_name)

    # Build list of only applicable GSPRs
    gspr_list = []
    for item in structured.gspr_results:
        if isinstance(item, GSPRWithSubsections):
            for sub in item.Subsections:
                if sub.Applicability == "Applicable":
                    gspr_list.append(sub.Subsection)
        elif isinstance(item, GSPRItem):
            if item.Applicability == "Applicable":
                gspr_list.append(item.GSPR)
        else:
            raise TypeError(f"Unexpected item type in gspr_results: {type(item)}")

    # Now make sure we follow the ApplicableGSPRState format exactly
    applicable_state = cast(ApplicableGSPRState, state["applicable_gspr"])

    # Ensure nested dict
    if "applicable_gspr" not in applicable_state:
        applicable_state["applicable_gspr"] = {}

    if component_name not in applicable_state["applicable_gspr"]:
        applicable_state["applicable_gspr"][component_name] = []

    applicable_state["applicable_gspr"][component_name].extend(gspr_list)

    # Put back into global state
    state["applicable_gspr"] = applicable_state

    print(f"🚀 Applicable GSPRs for '{component_name}': {gspr_list}")
    return state


## Node 4 : generate GSPR report
from chains.gspr_generator_chain import gspr_generator_chain
from models.gspr_generator_model import GSPRGENERATORMODEL



from typing import cast

from models.gspr_generator_model import GSPRGENERATORMODEL

def gspr_generator_node(state: GlobalState, component_name: str) -> GlobalState:
    user_input = state["user_input"]
    applicable_gsprs = state["applicable_gspr"]["applicable_gspr"].get(component_name) or []

    gspr_state = cast(dict, state["gspr"])
    gspr_content = cast(dict, gspr_state["gspr_content"])
    components = cast(dict, gspr_content["components"])

    if component_name not in components:
        components[component_name] = {"sections": {}}
    component_dict = components[component_name]

    for gspr in applicable_gsprs:
        main_gspr_number = gspr.split(".")[0]

        chain_input = {
            "device_type": user_input["device_type"],
            "intended_purpose": user_input["intended_use"],
            "intended_use": user_input["intended_use"],
            "region_classifications": user_input["region_classification"],
            "component": component_name,
            "gspr": main_gspr_number
        }

        print(f"\n🛠️ Generating GSPR {gspr} for component: {component_name}")
        response = gspr_generator_chain.invoke(chain_input)
        print("✅ Raw LLM JSON response:", response)

        # Defensive unpack to ensure it’s a proper dict
        if not isinstance(response, dict):
            raise TypeError("LLM response is not a dictionary")

        # Make sure all keys are present
        required_keys = ["component", "gspr", "design_input", "applicability", "justification", "requirement", "standard"]
        missing_keys = [k for k in required_keys if k not in response]
        if missing_keys:
            raise ValueError(f"LLM response missing keys: {missing_keys}")

        # Finally parse into Pydantic model (will raise error if types wrong)
        item = GSPRGENERATORMODEL(**response)

        gspr_item = {
            "design_input": item.design_input,
            "applicability": item.applicability,
            "justification": item.justification,
            "requirements": item.requirement,
            "standards": [item.standard]
        }
        section_key = f"GSPR{gspr}"
        component_dict["sections"][section_key] = gspr_item

    print(f"\n📦 Completed GSPR generation for '{component_name}'.")
    return state
