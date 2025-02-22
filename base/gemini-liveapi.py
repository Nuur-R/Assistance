import asyncio
import base64
import os
import traceback
import pyaudio
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Constants for audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024
MODEL = "models/gemini-2.0-flash-exp"

# Initialize Google GenAI client
client = genai.Client(http_options={"api_version": "v1alpha"})
CONFIG = {
    "system_instruction": """
        Your name is  Rama, you are an assistance for Firdaus, your creator
        you have several main task:
        1. You give user what Information he want to ask.
        2. You will help user to improve their English.
    """,
    "generation_config": {
        "response_modalities": ["AUDIO"],
        "speech_config": {
            "voice_config": {
                "prebuilt_voice_config": {
                    "voice_name": "Aoede"
                }
            }
        }
    }
}

# Initialize PyAudio
pya = pyaudio.PyAudio()

class main:
    def __init__(self):
        self.audio_in_queue = None
        self.session = None
        self.listen_audio_task = None
        self.receive_audio_task = None
        self.play_audio_task = None

    async def listen_audio(self):
        """Task to capture audio from the microphone and send it to the queue."""
        mic_info = pya.get_default_input_device_info()
        self.audio_stream = await asyncio.to_thread(
            pya.open,
            format=FORMAT,
            channels=CHANNELS,
            rate=SEND_SAMPLE_RATE,
            input=True,
            input_device_index=mic_info["index"],
            frames_per_buffer=CHUNK_SIZE,
        )
        while True:
            data = await asyncio.to_thread(self.audio_stream.read, CHUNK_SIZE)
            await self.session.send(input={"data": data, "mime_type": "audio/pcm"})

    async def receive_audio(self):
        """Task to receive audio responses from the model and write them to the queue."""
        while True:
            turn = self.session.receive()
            async for response in turn:
                if data := response.data:
                    self.audio_in_queue.put_nowait(data)

    async def play_audio(self):
        """Task to play audio received from the model."""
        stream = await asyncio.to_thread(
            pya.open,
            format=FORMAT,
            channels=CHANNELS,
            rate=RECEIVE_SAMPLE_RATE,
            output=True,
        )
        while True:
            bytestream = await self.audio_in_queue.get()
            await asyncio.to_thread(stream.write, bytestream)

    async def run(self):
        """Main function to run the voice interaction loop."""
        try:
            async with (
                client.aio.live.connect(model=MODEL, config=CONFIG) as session,
                asyncio.TaskGroup() as tg,
            ):
                self.session = session
                self.audio_in_queue = asyncio.Queue()
                tg.create_task(self.listen_audio())
                tg.create_task(self.receive_audio())
                tg.create_task(self.play_audio())
                print("Voice interaction started. Press Ctrl+C to exit.")
                await asyncio.Event().wait()  # Keep running until interrupted
        except KeyboardInterrupt:
            print("\nExiting...")
        except Exception as e:
            traceback.print_exception(e)
        finally:
            self.audio_stream.close()

if __name__ == "__main__":
    # Ensure GOOGLE_API_KEY is set
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not set in the .env file.")
    
    # Run the voice interaction loop
    voice_interaction = main()
    asyncio.run(voice_interaction.run())