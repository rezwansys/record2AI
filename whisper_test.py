#import warnings
#import soundcard as sc
#import numpy as np
import whisper
#import scipy.io.wavfile as wav
import platform

import pyaudio
import wave
import requests
import time
import json
import os
from datetime import datetime

class AudioTranscriber:
    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.audio = pyaudio.PyAudio()
        self.output_dir = "recordings"
        self.ensure_output_dir()
        
    def ensure_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def record_audio(self, duration=5):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/recording_{timestamp}.wav"
        
        print(f"\n🎙️ Recording for {duration} seconds...")
        stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                               rate=self.RATE, input=True,
                               frames_per_buffer=self.CHUNK)
        
        frames = []
        for _ in range(0, int(self.RATE / self.CHUNK * duration)):
            data = stream.read(self.CHUNK)
            frames.append(data)
        
        print("✅ Recording complete!")
        
        stream.stop_stream()
        stream.close()
        
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))
        
        return filename

    def transcribe_audio(self, filename, model_size="small"):
        print(f"\n🔄 Transcribing audio using Whisper {model_size} model...")
        model = whisper.load_model(model_size)
        result = model.transcribe(filename)
        return result["text"]

    def get_ai_analysis(self, text, analysis_type="summary"):
        prompts = {
            "summary": "Provide a concise summary of this text",
            "key_points": "Extract the main key points from this text",
            "action_items": "Identify any action items or tasks mentioned",
            "sentiment": "Analyze the sentiment and tone of this text",
            "questions": "Generate relevant follow-up questions based on this text"
        }
        
        try:
            response = requests.post(
                "http://127.0.0.1:11434/api/generate",
                json={
                    "model": "deepseek-coder",
                    "prompt": f"{prompts[analysis_type]}: {text}",
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            return f"Error connecting to Ollama: {str(e)}"

    def save_results(self, filename, transcription, analyses):
        output_file = filename.replace('.wav', '_analysis.json')
        results = {
            "timestamp": datetime.now().isoformat(),
            "audio_file": filename,
            "transcription": transcription,
            "analyses": analyses
        }
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        return output_file

def main():
    transcriber = AudioTranscriber()
    
    while True:
        print("\n🎤 Audio Transcription and Analysis Tool")
        print("1. Start new recording")
        print("2. Analyze existing audio file")
        print("3. Exit")
        
        choice = input("\nChoose an option (1-3): ")
        
        if choice == "1":
            duration = int(input("Enter recording duration in seconds (default: 5): ") or "5")
            filename = transcriber.record_audio(duration)
        elif choice == "2":
            filename = input("Enter the path to audio file: ")
            if not os.path.exists(filename):
                print("❌ File not found!")
                continue
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice!")
            continue

        transcription = transcriber.transcribe_audio(filename)
        print("\n📝 Transcription:", transcription)

        analyses = {}
        print("\n🤖 Generating AI analyses...")
        for analysis_type in ["summary", "key_points", "action_items", "sentiment", "questions"]:
            print(f"\n⏳ Generating {analysis_type}...")
            analyses[analysis_type] = transcriber.get_ai_analysis(transcription, analysis_type)
            print(f"\n{analysis_type.upper()}:")
            print(analyses[analysis_type])

        output_file = transcriber.save_results(filename, transcription, analyses)
        print(f"\n💾 Results saved to: {output_file}")

if __name__ == "__main__":
    main()
