import pyaudio

pya = pyaudio.PyAudio()

def open_audio_stream(format, channels, rate, input=True, output=False, input_device_index=None, frames_per_buffer=1024):
    return pya.open(
        format=format,
        channels=channels,
        rate=rate,
        input=input,
        output=output,
        input_device_index=input_device_index,
        frames_per_buffer=frames_per_buffer
    )

def close_audio_stream(stream):
    stream.stop_stream()
    stream.close()