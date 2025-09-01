import time
from datetime import datetime
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from lang.graph.graph import app_runnable
from logger import configure_logging, logger


# Initial logging configuration
configure_logging(log_level="INFO", log_to_console=True)

api = FastAPI(
    title="Image Generation API (JSON Output)",
    description="API to generate images and return them in JSON format."
)


class InputRequest(BaseModel):
    """Defines the structure of the incoming request body."""
    client_id: str
    conversation_id: str
    conversation: str  # Image prompt
    msisdn: str
    timestamp: Optional[str] = None
    job_id: Optional[str] = None


@api.post("/generate_image_json")
async def generate_image_json(request: InputRequest):
    """
    Receives a prompt, runs the image generation pipeline, and returns a JSON response containing the Base64 image data.
    """
    start_time = time.time()
    logger.info(f"--- 🚀 API Start for JSON Image Response at : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")

    process_successful = True
    final_state = {}

    try:
        # Run the graph with the user's prompt
        inputs = {"prompt": request.conversation}
        final_state = await app_runnable.ainvoke(inputs)

        if not final_state.get("image_b64"):
            raise ValueError("Failed to get Base64 image data from graph.")

    except Exception as e:
        logger.error(f"--- 🚨 API ERROR: {e} ---", exc_info=True)
        process_successful = False
        final_state["image_b64"] = None

    end_time = time.time()
    latency_milliseconds = (end_time - start_time) * 1000

    # Build the JSON response
    response_data = {
        "chat_id": request.conversation_id,
        "client_id": request.client_id,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "latency_ms": round(latency_milliseconds, 1),
        "chat": request.conversation,
        "msisdn": request.msisdn,
        "image": final_state.get("image_b64"),
        "process_is_success": process_successful,
    }

    logger.info("--- ✅ Returning JSON response with Base64 image. ---")
    return response_data


@api.get("/health")
async def health_check():
    """Endpoint to check if the API is running."""
    return {"status": "healthy"}