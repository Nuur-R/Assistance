# === FILE: handlers.py ===
import json
import asyncio
import base64
from fastapi import WebSocket
# from google.genai.aio import ClientSession
from config import client, MODEL
from utils import set_light_values, tool_set_light_values

async def gemini_session_handler(websocket: WebSocket):
    await websocket.accept()
    try:
        config_message = await websocket.receive_text()
        config_data = json.loads(config_message)
        config = config_data.get("setup", {})
        config["tools"] = [tool_set_light_values]
        
        async with client.aio.live.connect(model=MODEL, config=config) as session:
            print("Connected to Gemini API")

            async def send_to_gemini():
                try:
                    while True:
                        message = await websocket.receive_text()
                        data = json.loads(message)
                        if "realtime_input" in data:
                            for chunk in data["realtime_input"]["media_chunks"]:
                                await session.send(chunk)
                except Exception as e:
                    print(f"Error sending to Gemini: {e}")

            async def receive_from_gemini():
                try:
                    while True:
                        async for response in session.receive():
                            if response.server_content is None:
                                if response.tool_call is not None:
                                    function_responses = []
                                    for function_call in response.tool_call.function_calls:
                                        name = function_call.name
                                        args = function_call.args
                                        call_id = function_call.id

                                        if name == "set_light_values":
                                            result = set_light_values(int(args["brightness"]), args["color_temp"])
                                            function_responses.append(
                                                {
                                                    "name": name,
                                                    "response": {"result": result},
                                                    "id": call_id
                                                }
                                            )
                                            await websocket.send_json({"text": json.dumps(function_responses)})
                                    await session.send(function_responses)
                            else:
                                model_turn = response.server_content.model_turn
                                if model_turn:
                                    for part in model_turn.parts:
                                        if hasattr(part, 'text') and part.text is not None:
                                            await websocket.send_json({"text": part.text})
                                        elif hasattr(part, 'inline_data') and part.inline_data is not None:
                                            base64_audio = base64.b64encode(part.inline_data.data).decode('utf-8')
                                            await websocket.send_json({"audio": base64_audio})
                except Exception as e:
                    print(f"Error receiving from Gemini: {e}")

            send_task = asyncio.create_task(send_to_gemini())
            receive_task = asyncio.create_task(receive_from_gemini())
            await asyncio.gather(send_task, receive_task)
    finally:
        await websocket.close()
        print("Gemini session closed.")