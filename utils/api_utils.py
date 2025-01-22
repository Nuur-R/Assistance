# api_utils.py
from google import genai
from config import GOOGLE_API_KEY, CONFIG, MODEL

client = genai.Client(api_key=GOOGLE_API_KEY, http_options={"api_version": "v1alpha"})

async def connect_to_gemini():
    return client.aio.live.connect(model=MODEL, config=CONFIG)