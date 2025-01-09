# === FILE: tools/play_music.py ===
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