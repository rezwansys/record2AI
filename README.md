# Audio Transcription and Summarization Tool

This tool records audio, transcribes it using Whisper, and generates a summary using Ollama's deepseek-coder model.

## Prerequisites

- Python 3.x
- Ollama running locally with deepseek-coder model
- FFmpeg (required for Whisper)

## Installation

1. Install required Python packages:
    ```bash
    pip install pyaudio whisper requests
    ```

2. Install FFmpeg:
    ```bash
    brew install ffmpeg
    ```

3. Install and run Ollama:
    ```bash
    # Install Ollama
    curl https://ollama.ai/install.sh | sh
    
    # Pull and run the deepseek-coder model
    ollama run deepseek-coder
    ```

## Usage

1. Run the script:
    ```bash
    python whisper_test.py
    ```

2. The script will:
    - Record 5 seconds of audio
    - Transcribe the audio using Whisper
    - Send the transcription to Ollama for summarization
    - Display both the transcription and summary

## Configuration

You can modify these variables in the script:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `RECORD_SECONDS` | Recording duration in seconds | 5 |
| `RATE` | Sample rate in Hz | 44100 |
| `CHANNELS` | Audio channels | 1 (mono) |

## Requirements

| Package | Purpose |
|---------|---------|
| `pyaudio` | Audio recording |
| `whisper` | Speech-to-text transcription |
| `requests` | Communicating with Ollama API |
| `wave` | Audio file handling |

## Important Notes

- Ensure your microphone permissions are enabled in System Preferences
- Ollama must be running locally on port 11434
- The script saves the audio as "file.wav" in the same directory

## Troubleshooting

1. If you encounter microphone permission issues:
    - Go to System Preferences > Security & Privacy > Microphone
    - Enable microphone access for your terminal or IDE

2. If Ollama is not responding:
    - Ensure Ollama is running: `ollama serve`
    - Verify the deepseek-coder model is installed: `ollama list`

## License

This project is open source and available under the MIT License.