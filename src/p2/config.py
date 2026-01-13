# Configuration for model selection and API keys
import os
from dotenv import load_dotenv

load_dotenv()

P2_MODEL = os.getenv("P2_MODEL", "gemini")  # 'openai' or 'gemini'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
# Placeholder for future config if needed
