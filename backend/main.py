# === FILE: main.py ===
from fastapi import FastAPI, WebSocket
from handlers import gemini_session_handler

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await gemini_session_handler(websocket)