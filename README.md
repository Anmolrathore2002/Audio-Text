# Audio Transcription & Translation with Whisper

This project uses OpenAI's Whisper model to transcribe and translate audio files (mp3, opus, wav) with automatic language detection. It converts speech to text in the original language and translates non-English audio to English.

---

## Features

- Supports `.mp3`, `.wav`, and `.opus` audio files  
- Automatically detects the spoken language  
- Transcribes audio to text in the original language  
- Translates non-English audio to English  
- Converts `.opus` files to `.mp3` using FFmpeg  
- Compatible with CPU and GPU (auto-detects CUDA)  

---

## Requirements

- Python 3.8 or higher  
- [FFmpeg](https://ffmpeg.org/) installed and added to system PATH  
- Python packages:
  - `torch`
  - `whisper`
  - `argparse`
  - `subprocess`

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Anmolrathore2002/Audio-Text.git
cd Audio-Text

