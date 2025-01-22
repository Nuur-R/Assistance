# === FILE: tools/type_text.py ===
import pyautogui
import time
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)

def type_text(prompt):
    """Menghasilkan teks menggunakan Groq API dan mengetiknya ke posisi kursor aktif."""
    try:
        response = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Atau model Groq lain yang Anda inginkan
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        generated_text = response.choices[0].message.content
        time.sleep(1)  # Beri waktu sejenak

        # Coba aktifkan jendela (ganti "Judul Jendela Anda" dengan judul yang sesuai)
        try:
            window_to_activate = pyautogui.getWindowsWithTitle("Judul Jendela Anda")[0]
            window_to_activate.activate()
            time.sleep(0.5) # Beri waktu jendela untuk aktif
        except IndexError:
            return "Jendela dengan judul 'Judul Jendela Anda' tidak ditemukan."

        pyautogui.write(generated_text)
        return f"Berhasil menghasilkan dan mengetik (Groq): {generated_text}"
    except Exception as e:
        return f"Terjadi kesalahan saat menghasilkan atau mengetik teks (Groq): {e}"

tool_type_text = {
    "function_declarations": [
        {
            "name": "type_text",
            "description": "Menghasilkan teks menggunakan Groq API berdasarkan prompt yang diberikan dan mengetiknya ke posisi kursor aktif di dokumen atau aplikasi.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "prompt": {
                        "type": "STRING",
                        "description": "Prompt untuk menghasilkan teks."
                    }
                },
                "required": ["prompt"]
            }
        }
    ]
}