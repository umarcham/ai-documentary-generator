# 🇮🇳 Freedom Fighter Video Generator

**An AI-powered Python pipeline that automatically generates cinematic 10-second documentary videos about Indian freedom fighters — from script to screen, fully automated.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)](https://python.org)
[![Gemini](https://img.shields.io/badge/Powered%20by-Gemini%202.5%20Flash-4285F4?style=flat-square&logo=google)](https://ai.google.dev)
[![Vertex AI](https://img.shields.io/badge/Vertex%20AI-Supported-orange?style=flat-square&logo=googlecloud)](https://cloud.google.com/vertex-ai)

---

## ✨ What It Does

Give it a name. It builds you a video.

The script takes an Indian freedom fighter's name and — entirely on its own — writes the script, generates AI art, synthesizes voiceover audio, adds animated subtitles, mixes in background music, and stitches it all into a polished MP4.

```bash
python3 generate_video.py --fighter "Bhagat Singh"
```

That's it. One command. Full cinematic video out.

---

## 🎬 How It Works

```
┌─────────────────────────────────────────────────────────┐
│                  generate_video.py                       │
│                                                          │
│  1. ─► Gemini 2.5 Flash ──► Script + Image Prompts      │
│         (Vertex AI / AI Studio / local fallback)         │
│                                                          │
│  2. ─► Pollinations AI ───► AI-generated cinematic art   │
│                                                          │
│  3. ─► Edge TTS ──────────► Natural Indian English voice  │
│                                                          │
│  4. ─► MoviePy ───────────► Ken Burns zoom/pan animation │
│                             + subtitle overlay           │
│                             + background music mix       │
│                                                          │
│  5. ─► 🎥 OUTPUT: Cinematic MP4 video (~10 seconds)     │
└─────────────────────────────────────────────────────────┘
```

### Pipeline Stages

| Stage | Technology | Description |
|-------|-----------|-------------|
| 📝 Script | Google Gemini 2.5 Flash | Generates 3-segment narration + image prompts |
| 🎨 Visuals | Pollinations AI | Free AI image generation at 1280×720 |
| 🎙️ Voice | Microsoft Edge TTS | Natural `en-IN-NeerjaNeural` voice |
| 🎞️ Effects | MoviePy + PIL | Ken Burns zoom/pan, subtitle overlays |
| 🎵 Music | SoundHelix (configurable) | Ambient background score at 15% volume |
| 📦 Output | FFmpeg via MoviePy | H.264 MP4, 24fps, AAC audio |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- `ffmpeg` installed on your system

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg
```

### Installation

```bash
# Clone the repo
git clone https://github.com/your-username/freedom-fighter-video-generator.git
cd freedom-fighter-video-generator

# Install Python dependencies
pip install -r requirements.txt
```

### Google Cloud / Vertex AI Setup

The script uses **Vertex AI** (via a service account) as the primary AI backend. Place your credentials file in the project root:

```
freedom-fighter-video-generator/
├── generate_video.py
├── GOOGLE_APPLICATION_CREDENTIALS.json   ← place it here
└── requirements.txt
```

> ⚠️ **Never commit your credentials file.** It is already listed in `.gitignore`.

If no credentials are found, the script automatically falls back to:
1. A `GEMINI_API_KEY` environment variable (Google AI Studio)
2. Pre-written local scripts (no internet needed)

---

## 🎯 Usage

### Basic

```bash
# Default: Subhas Chandra Bose
python3 generate_video.py

# Pick a fighter
python3 generate_video.py --fighter "Bhagat Singh"
python3 generate_video.py --fighter "Mahatma Gandhi"
python3 generate_video.py --fighter "Rani Lakshmibai"
```

### All Options

```bash
python3 generate_video.py \
  --fighter "Bhagat Singh" \
  --output bhagat_singh.mp4 \
  --voice en-IN-NeerjaNeural \
  --music-url https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3 \
  --no-music \
  --api-key YOUR_GEMINI_API_KEY \
  --creds /path/to/credentials.json
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--fighter` | `Subhas Chandra Bose` | Name of the Indian freedom fighter |
| `--output` | `freedom_fighter.mp4` | Output video filename |
| `--voice` | `en-IN-NeerjaNeural` | Edge TTS voice to use |
| `--music-url` | SoundHelix MP3 | URL for background music |
| `--no-music` | `False` | Disable background music |
| `--api-key` | env var / auto | Gemini AI Studio API key |
| `--creds` | auto-detect | Path to Google credentials JSON |

### Using an Environment Variable

```bash
export GEMINI_API_KEY="your-key-here"
python3 generate_video.py --fighter "Rani Lakshmibai"
```

---

## 📁 Project Structure

```
freedom-fighter-video-generator/
├── generate_video.py          # Main pipeline script
├── requirements.txt           # Python dependencies
├── .gitignore                 # Ignores credentials, outputs, temp files
├── README.md                  # You are here
└── temp_assets/               # Auto-created during generation (gitignored)
    ├── image_1.png
    ├── image_2.png
    ├── image_3.png
    ├── voiceover_1.mp3
    ├── voiceover_2.mp3
    ├── voiceover_3.mp3
    └── background_music.mp3
```

---

## 🧠 AI Integration Details

### Gemini API Priority Chain

```
GOOGLE_APPLICATION_CREDENTIALS.json  (Vertex AI — preferred)
        ↓ if not found / fails
GEMINI_API_KEY env var               (Google AI Studio fallback)
        ↓ if not set / fails
Local pre-written scripts            (offline fallback)
```

### Built-in Freedom Fighters (Offline Mode)

These fighters work without any API credentials:

- **Subhas Chandra Bose** ← default
- **Bhagat Singh**
- **Mahatma Gandhi**
- **Rani Lakshmibai**

With API credentials, Gemini generates fully customized content for **any** freedom fighter.

---

## 📦 Dependencies

```
requests       — HTTP calls to image and music APIs
moviepy>=2.0   — Video assembly, audio mixing, clip effects
edge-tts       — Microsoft Edge Text-to-Speech synthesis
pillow         — Image processing and subtitle rendering
numpy          — Frame array manipulation
google-auth    — Vertex AI service account credential loading
```

---

## ⚙️ Troubleshooting

| Problem | Fix |
|---------|-----|
| `edge-tts` not found | `pip install edge-tts` |
| `ffmpeg` not found | `brew install ffmpeg` (macOS) / `sudo apt install ffmpeg` (Linux) |
| Image download fails | Pollinations AI retries 4× automatically; check your internet connection |
| Vertex AI 429 error | Quota exhausted; script auto-falls back to local scripts |

---

## 🤝 Assignment Context

This project was built as a Junior AI Developer assignment. It demonstrates:

- Practical integration of **Generative AI APIs** (Gemini via Vertex AI and AI Studio)
- **Automated multimedia pipeline** design (script → image → audio → video)
- Clean, human-readable Python with graceful fallbacks
- Real-world multi-service AI coordination

---

*Made with ❤️ — AI-Powered Documentary Generator*
