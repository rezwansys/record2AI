#import warnings
#import soundcard as sc
#import numpy as np
import whisper
#import scipy.io.wavfile as wav
import platform

import pyaudio
import wave
 
FORMAT = pyaudio.paInt16
CHANNELS = 1  # Changed to mono
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"
 
audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
print("recording...")  # Updated for Python 3
frames = []
 
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("finished recording")  # Updated for Python 3
 
 
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
 
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
# raw
# formatted

# Transcribe with Whisper
model = whisper.load_model("small")
result = model.transcribe("file.wav")
transcription = result["text"]
print("Transcription:", transcription)

# Send to Ollama for summarization
import requests

def get_ollama_summary(text: str) -> str:
    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "deepseek-coder",
                "prompt": f"make a summarry of this : {text}",
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {str(e)}"

# Get summary from Ollama
summary = get_ollama_summary(transcription)
print("\nSummary:", summary)