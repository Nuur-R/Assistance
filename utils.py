# === FILE: utils.py ===
def get_current_datetime():
    from datetime import datetime
    now = datetime.now()
    print(f"[FUNCTION] Date Time: {now.strftime("%Y-%m-%d %H:%M:%S")}")
    return now.strftime("%Y-%m-%d %H:%M:%S")

tool_get_current_datetime = {
    "function_declarations": [
        {
            "name": "get_current_datetime",
            "description": "Mendapatkan tanggal dan waktu saat ini.",
        }
    ]
}

def play_music(artist, song_title):
    # Kode untuk memutar musik (misalnya, menggunakan library seperti vlc atau pygame)
    print(f"[FUNCTION] Memutar lagu {song_title} oleh {artist}.")
    return f"Memutar lagu {song_title} oleh {artist}."

tool_play_music = {
    "function_declarations": [
        {
            "name": "play_music",
            "description": "Memutar lagu berdasarkan judul dan nama penyanyi.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "artist": {
                        "type": "STRING",
                        "description": "Nama penyanyi."
                    },
                    "song_title": {
                        "type": "STRING",
                        "description": "Judul lagu."
                    }
                },
                "required": ["artist", "song_title"]
            }
        }
    ]
}

def set_light_values(brightness, color_temp):
    print(f"[FUNCTION] kecerahan: {brightness} dan temperatur: {color_temp}.")   
    return {
        "brightness": brightness,
        "colorTemperature": color_temp,
    }

tool_set_light_values = {
    "function_declarations": [
        {
            "name": "set_light_values",
            "description": "Set the brightness and color temperature of a room light.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "brightness": {
                        "type": "NUMBER",
                        "description": "Light level from 0 to 100. Zero is off and 100 is full brightness"
                    },
                    "color_temp": {
                        "type": "STRING",
                        "description": "Color temperature of the light fixture, which can be `daylight`, `cool` or `warm`."
                    }
                },
                "required": ["brightness", "color_temp"]
            }
        }
    ]
}