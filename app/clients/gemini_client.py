from google import genai
from app.config import settings

gemini_api_key = settings.GEMINI_GOOGLE_API_KEY
if not gemini_api_key:
    raise ValueError("GEMINI_GOOGLE_API_KEY is not configured")

client = genai.Client(api_key=gemini_api_key)

def get_gemini_client():
    return client
