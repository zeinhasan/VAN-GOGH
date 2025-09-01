from typing import TypedDict

class GraphState(TypedDict):
    """
    Represents the state of a graph, including the prompt and the base64-encoded image.
    """
    prompt: str  # The text prompt for the graph
    image_b64: str  # The image in base64 encoding