# === FILE: tools/get_current_datetime.py ===
from datetime import datetime

def get_current_datetime():
    now = datetime.now()
    print(f"[FUNCTION] Date Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    return now.strftime('%Y-%m-%d %H:%M:%S')

tool_get_current_datetime = {
    "function_declarations": [
        {
            "name": "get_current_datetime",
            "description": "Mendapatkan tanggal dan waktu saat ini.",
        }
    ]
}