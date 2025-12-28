# Aksa TTS - Indonesian Text-to-Speech with Regional Accents

<div align="center">

![Aksa TTS](https://img.shields.io/badge/Aksa-TTS-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**A powerful Indonesian Text-to-Speech system with support for various regional accents**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [API Documentation](#api-documentation) • [Supported Accents](#supported-accents) • [Contributing](#contributing)

</div>

---

## 📖 About

Aksa TTS is an advanced Text-to-Speech (TTS) system specifically designed for the Indonesian language with support for various regional accents. Built on top of the Chatterbox-TTS framework, it provides high-quality speech synthesis with voice cloning capabilities, allowing users to generate speech in different Indonesian regional accents.

## ✨ Features

- 🗣️ **Multi-Accent Support**: Generate speech in 16+ different Indonesian regional accents
- 🎯 **Voice Cloning**: Clone voice characteristics from reference audio samples
- 🚀 **Fast API**: Built with FastAPI for quick and efficient API requests
- 📦 **Easy Integration**: Simple REST API for seamless integration with applications
- 🔄 **Streaming Support**: Stream audio output for real-time playback
- 💾 **Multiple Output Formats**: Export audio in WAV format
- 🎛️ **Flexible Configuration**: Customizable text and accent selection
- 🌐 **Cross-Platform**: Works on Windows, Linux, and macOS

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- CUDA-capable GPU (recommended) or CPU
- FFmpeg (required for audio processing)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/tts-aksa.git
cd tts-aksa
```

### Step 2: Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\Activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to your system PATH.

## 📚 Usage

### Running the TTS Server

Start the FastAPI server:

```bash
python main.py
```

The server will start on `http://0.0.0.0:8000`

### Generating Speech with Accent

Use the `run_tts.py` script to generate speech with a specific accent:

```python
import os
from run_tts import generate_speech_with_accent

# Generate speech with Sundanese accent
generate_speech_with_accent(
    text_to_speak="Tah, ieu abdi, Gemini. Abdi nuju nyobian nyarios ku basa Sunda.",
    accent_audio_path=os.path.join("audio_referensi", "aksen_sunda_pria.wav"),
    output_filename="hasil_sunda.wav"
)
```

## 📡 API Documentation

### Endpoints

#### 1. Health Check

**GET** `/`

Check if the server is running.

**Response:**
```json
{
  "status": "Aksa TTS Backend is running."
}
```

#### 2. Stream Speech

**POST** `/stream-speech/`

Generate and stream speech with a specific accent.

**Request Body:**
```json
{
  "text": "Halo, apa kabar?",
  "accent_id": "sunda"
}
```

**Parameters:**
- `text` (string, required): The text to convert to speech
- `accent_id` (string, required): The accent ID to use (see [Supported Accents](#supported-accents))

**Response:**
- Content-Type: `audio/wav`
- Streaming audio data

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/stream-speech/"   -H "Content-Type: application/json"   -d '{"text": "Halo, apa kabar?", "accent_id": "sunda"}'   --output output.wav
```

**Example using Python:**
```python
import requests

url = "http://localhost:8000/stream-speech/"
data = {
    "text": "Halo, apa kabar?",
    "accent_id": "sunda"
}

response = requests.post(url, json=data)

with open("output.wav", "wb") as f:
    f.write(response.content)
```

## 🎭 Supported Accents

Aksa TTS supports the following Indonesian regional accents:

| Accent ID | Name | Gender | Reference File |
|-----------|------|--------|----------------|
| `aceh` | Acehnese | Male | aksen_aceh_pria.wav |
| `bali` | Balinese | Male | aksen_bali_pria.wav |
| `banjar` | Banjarese | Female | aksen_banjar_wanita.wav |
| `batak` | Batak | Male | aksen_batak_pria.wav |
| `betawi` | Betawi | Male | aksen_betawi_pria.wav |
| `jawa` | Javanese | Male | aksen_jawa_pria.wav |
| `maluku` | Moluccan | Male | aksen_maluku_pria.wav |
| `melayu` | Malay | Male | aksen_melayu_pria.wav |
| `minang` | Minangkabau | Male | aksen_minang_pria.wav |
| `ntt` | East Nusa Tenggara | Male | aksen_ntt_pria.wav |
| `papua` | Papuan | Male | aksen_papua_pria.wav |
| `pontianak` | Pontianak | Female | aksen_pontianak_wanita.wav |
| `sulsel` | South Sulawesi | Male | aksen_sulsel_pria.wav |
| `sulut` | North Sulawesi | Male | aksen_sulut_pria.wav |
| `sunda` | Sundanese | Male | aksen_sunda_pria.wav |
| `sunda_v2` | Sundanese V2 | Male | aksen_sunda_pria.wav |
| `default` | Default | Male | aksen_default_pria.wav |

## 📁 Project Structure

```
tts-aksa/
├── audio_referensi/      # Reference audio files for each accent
├── output/              # Generated audio files
├── main.py              # FastAPI server implementation
├── run_tts.py           # Script for generating speech with accent
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔧 Configuration

### Device Selection

The system automatically detects and uses CUDA if available, otherwise falls back to CPU. To force CPU usage, modify the device setting in `main.py` or `run_tts.py`:

```python
device = "cpu"  # Force CPU usage
```

### Model Configuration

The model is loaded from Hugging Face Hub:
- Repository: `grandhigh/Chatterbox-TTS-Indonesian`
- Checkpoint: `t3_cfg.safetensors`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [Chatterbox-TTS](https://github.com/yourusername/chatterbox-tts) - The underlying TTS framework
- [Hugging Face](https://huggingface.co/) - For model hosting and distribution
