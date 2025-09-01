from langgraph.graph import StateGraph, END
from lang.nodes.nodes import GraphState, generate_image_b64_node

def create_image_generation_graph():
    """Builds a LangGraph workflow for Base64 image generation."""
    workflow = StateGraph(GraphState)

    # Add the image generation node
    workflow.add_node("image_b64_generator", generate_image_b64_node)

    workflow.set_entry_point("image_b64_generator")
    workflow.add_edge("image_b64_generator", END)

    return workflow.compile()

app_runnable = create_image_generation_graph()