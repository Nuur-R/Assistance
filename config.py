import os
from dotenv import load_dotenv
import pyaudio

# Muat variabel dari file .env
load_dotenv()

# Konfigurasi Audio
FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024

# Konfigurasi Model dan Generasi Respons
MODEL = "models/gemini-2.0-flash-exp"
GENERATION_CONFIG = {
    "response_modalities": ["AUDIO"],
    "temperature": 0.7,
    "max_tokens": 100,
    "top_p": 0.9,
    "stop_sequences": ["\n", "."]
}
CONFIG = {
    "system_instruction": """
        Anda adalah Rama, AI Asisten yang dibuat untuk membantu Firdaus.
        Fungsi Anda adalah:
        1. Menjawab user dengan bahasa Indonesia, termasuk melafalkan huruf dan simbol.
        2. Mengeksekusi tools yang tersedia.
        3. Menjawab pertanyaan yang diajukan user.
    """,
    "generation_config": {
        "speech_config": {
            "voice_config": {
                "prebuilt_voice_config": {
                    "voice_name": "Kore"
                }
            }
        }
    }
}
# API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("API key not found in .env file. Please add GOOGLE_API_KEY to .env.")