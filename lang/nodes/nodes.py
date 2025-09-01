import base64
import os
import google.genai as genai
from google.genai import types
from config import MODEL_NAME, GEMINI_API_KEY
from logger import logger
from lang.state.state import GraphState


def generate_image_b64_node(state: GraphState):
    """
    Generate an image using the google-genai library with streaming and response modalities.
    Returns a dictionary with the image encoded in Base64.
    """
    user_prompt = state.get("prompt")
    logger.info(f"--- 🖼️ Generating image for prompt: '{user_prompt}' using streaming method ---")

    try:

        client = genai.Client(api_key=GEMINI_API_KEY)
        generate_content_config = types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        )
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=user_prompt),
                ],
            ),
        ]
        stream = client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=contents,
            config=generate_content_config,
        )
        image_bytes = None
        for chunk in stream:
            # Check if the chunk contains image data
            if (
                chunk.candidates and
                chunk.candidates[0].content and
                chunk.candidates[0].content.parts and
                chunk.candidates[0].content.parts[0].inline_data and
                chunk.candidates[0].content.parts[0].inline_data.data
            ):
                inline_data = chunk.candidates[0].content.parts[0].inline_data
                image_bytes = inline_data.data
                logger.info(f"--- ✅ Image data found in stream (MIME type: {inline_data.mime_type}) ---")
                break

        if not image_bytes:
            raise ValueError("Model stream finished without returning image data. The prompt was likely refused. Please use a descriptive English prompt.")

        img_b64 = base64.b64encode(image_bytes).decode("utf-8")
        logger.info("--- ✅ Image successfully extracted from stream and converted to Base64 ---")
        return {"image_b64": img_b64}

    except Exception as e:
        logger.error(f"--- 🚨 ERROR during streaming image generation: {e} ---", exc_info=True)
        raise