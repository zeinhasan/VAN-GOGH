import os
from dotenv import load_dotenv
from logger import logger

# Load environment variables from .env file
load_dotenv()

# --- Global Variables ---

# Retrieve GEMINI_API_KEY from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.error("--- 🚨 FATAL: GEMINI_API_KEY not found in environment variables! ---")
    raise ValueError("GEMINI_API_KEY is not set.")

# Model name for easy configuration
MODEL_NAME = "gemini-2.5-flash-image-preview"

logger.info(f"--- ✅ Config loaded. Using model: {MODEL_NAME} ---")