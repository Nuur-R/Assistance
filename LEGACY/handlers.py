# === FILE: handlers.py ===
import json
import asyncio
import base64
from fastapi import WebSocket
# from google.genai.aio import ClientSession
from config import client, MODEL
from tools.set_light_values import set_light_values, tool_set_light_values
from tools.play_music import play_music, tool_play_music
from tools.get_current_datetime import get_current_datetime, tool_get_current_datetime
from tools.type_text import type_text, tool_type_text

async def gemini_session_handler(websocket: WebSocket):
    await websocket.accept()
    try:
        config_message = await websocket.receive_text()
        config_data = json.loads(config_message)
        config = config_data.get("setup", {})
        config["tools"] = [tool_set_light_values, tool_play_music, tool_get_current_datetime, tool_type_text] # Tambahkan tool baru
        config["system_instruction"] =  """ Anda adalah adalah Rama, AI Asisten yang dibuat untuk membantu Firdaus,
                                            fungsi anda adalah :
                                            1. Menjawab user dengan bahasa Indonesia, termasuk melafalkan huruf dan simbol
                                            2. Mengeksekusi tools yg tersedia.
                                            3. Menjawab pertanyaan  yg di ajukan user.
                                        """
        config["generation_config"] = {
            "speech_config": {
                "voice_config": {
                    "prebuilt_voice_config": {
                        "voice_name": "Kore"
                    }
                }
            }
        }
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
                                        elif name == "play_music": # Tangani tool call baru
                                            result = play_music(args["artist"], args["song_title"])
                                            function_responses.append(
                                                {
                                                    "name": name,
                                                    "response": {"result": result},
                                                    "id": call_id
                                                }
                                            )
                                            await websocket.send_json({"text": json.dumps(function_responses)})
                                        elif name == "get_current_datetime":
                                            result = get_current_datetime()
                                            function_responses.append(
                                                {
                                                    "name": name,
                                                    "response": {"result": result},
                                                    "id": call_id
                                                }
                                            )
                                            await websocket.send_json({"text": json.dumps(function_responses)})
                                        elif name == "type_text":
                                            result = type_text(args["prompt"])
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
                                if model_turn and model_turn.parts:  # Pastikan model_turn dan parts tidak kosong
                                    for part in model_turn.parts:
                                        if hasattr(part, 'text') and part.text is not None:
                                            await websocket.send_json({"text": part.text})
                                        elif hasattr(part, 'inline_data') and part.inline_data is not None:
                                            base64_audio = base64.b64encode(part.inline_data.data).decode('utf-8')
                                            await websocket.send_json({"audio": base64_audio})
                                        elif hasattr(part, 'video_metadata') and part.video_metadata is not None:
                                            print(f"Menerima metadata video: {part.video_metadata}") # Tambahkan penanganan metadata video jika diperlukan
                                        elif hasattr(part, 'thought') and part.thought is not None:
                                            print(f"Menerima pemikiran model: {part.thought}") # Tambahkan penanganan pemikiran model jika diperlukan
                                        elif hasattr(part, 'code_execution_result') and part.code_execution_result is not None:
                                            await websocket.send_json({"code_result": part.code_execution_result.output}) # Kirim hasil eksekusi kode ke klien
                                        elif hasattr(part, 'executable_code') and part.executable_code is not None:
                                            print(f"Menerima kode yang dapat dieksekusi: {part.executable_code.code}")
                                            # TODO: Tambahkan logika untuk menjalankan kode jika diperlukan dan aman
                                        else:
                                            print(f"Menerima bagian respons tanpa teks, audio, video_metadata, thought, code_execution_result, atau executable_code: {part}") # Tambahkan logging
                                elif response.server_content is not None: # Handle kasus ketika model_turn adalah None tetapi server_content ada
                                    print(f"Menerima respons tanpa model_turn atau parts: {response.server_content}") # Tambahkan logging
                                else:
                                    print(f"Menerima respons server_content kosong: {response}") # Tambahkan logging untuk respons server_content kosong
                except Exception as e:
                    print(f"Error receiving from Gemini: {e}")

            send_task = asyncio.create_task(send_to_gemini())
            receive_task = asyncio.create_task(receive_from_gemini())
            await asyncio.gather(send_task, receive_task)
    finally:
        await websocket.close()
        print("Gemini session closed.")