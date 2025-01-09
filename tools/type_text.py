# === FILE: tools/type_text.py ===
import pyautogui
import time

def type_text(text):
    """Mengetik teks ke posisi kursor aktif."""
    time.sleep(1)  # Beri waktu sejenak agar kursor fokus
    pyautogui.write(text)
    return f"Berhasil mengetik: {text}"

tool_type_text = {
    "function_declarations": [
        {
            "name": "type_text",
            "description": "Mengetik teks ke posisi kursor aktif di dokumen atau aplikasi.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "text": {
                        "type": "STRING",
                        "description": "Teks yang akan diketik."
                    }
                },
                "required": ["text"]
            }
        }
    ]
}