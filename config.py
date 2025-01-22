import os, json
from dotenv import load_dotenv
import pyaudio
from tools import tool_set_light_values, set_light_values
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
    "tools": [tool_set_light_values],
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

def handle_tool_call(tool_call):
    """
    Menangani tool_call dan memanggil fungsi tool yang sesuai.
    """
    # Periksa struktur tool_call dan sesuaikan
    if hasattr(tool_call, 'call_id'):  # Jika tool_call memiliki call_id
        tool_id = tool_call.call_id
    elif hasattr(tool_call, 'request_id'):  # Jika tool_call memiliki request_id
        tool_id = tool_call.request_id
    else:
        tool_id = "default_tool_id"  # Gunakan ID default jika tidak ada

    tool_name = tool_call.function.name  # Nama fungsi tool
    tool_args = json.loads(tool_call.function.arguments)  # Argumen fungsi tool

    # Panggil fungsi tool yang sesuai
    if tool_name == "set_light_values":
        result = set_light_values(tool_args["brightness"], tool_args["color_temp"])
    else:
        result = {"error": f"Tool '{tool_name}' tidak ditemukan."}

    # Kembalikan hasil eksekusi tool
    return {
        "tool_call_id": tool_id,
        "tool_response": result
    }