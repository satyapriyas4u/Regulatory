from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from regulatory.graph.node import (
    user_input_node,
    component_recommender_node,
    gspr_filter_node,
    gspr_generator_node,
    f_g_node
)
from regulatory.graph.state import GlobalState, GSPRState, ComponentSection

import json
# -----------------------------------------------------------
    # Initial empty state
state = GlobalState(
        user_input={
            "device_type": "",
            "intended_use": "",
            "intended_users": [],
            "components": [],
            "region_classification": ""
        },
        recommender={
            "recommended_components": [],
            "given_components": []
        },
        applicable_gspr={
            "applicable_gspr": {}
        },
        gspr=GSPRState(
            gspr_content=ComponentSection(
                components={}
            )
        )
    )
workflow = StateGraph(GlobalState)
# Add nodes
workflow.add_node("user_input_node", user_input_node)
workflow.add_node("component_recommender_node", component_recommender_node)
workflow.add_node("main_node", f_g_node)
# Add edges to connect nodes
workflow.add_edge(START, "user_input_node")
workflow.add_edge("user_input_node", "component_recommender_node")
workflow.add_edge( "component_recommender_node","main_node")

workflow.add_edge("main_node", END)

# Compile
chain = workflow.compile()
display(Image(chain.get_graph().draw_mermaid_png()))

state = chain.invoke(state)