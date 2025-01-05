# === FILE: config.py ===
import os
from google import genai

# Load API key from environment
os.environ['GOOGLE_API_KEY'] = 'AIzaSyBTtRe2IA3o14lxAMOsO83Xhsy2KxSIlMg'
MODEL = "gemini-2.0-flash-exp"  # use your model ID

client = genai.Client(
    http_options={
        'api_version': 'v1alpha',
    }
)