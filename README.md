<div align="center">

# 🎬 AI Documentary Generator
### *Cinematic Freedom Fighter Video Pipeline — Powered by Gemini AI*

<br/>

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-AI_Brain-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![Vertex AI](https://img.shields.io/badge/Vertex_AI-Supported-FF6F00?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com/vertex-ai)
[![Edge TTS](https://img.shields.io/badge/Edge_TTS-Voice_Synthesis-0078D4?style=for-the-badge&logo=microsoft&logoColor=white)](https://github.com/rany2/edge-tts)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

<br/>

> **One command. One name. A full cinematic documentary — generated entirely by AI.**

<br/>

```bash
python3 generate_video.py --fighter "Bhagat Singh"
```

</div>

---

## ✨ What It Does

Give it the name of any Indian freedom fighter. The pipeline takes over completely:

| Step | What Happens |
|------|-------------|
| 🧠 **Think** | Gemini 2.5 Flash writes a 3-segment cinematic script with AI image prompts |
| 🎨 **Paint** | Pollinations AI generates 1280×720 oil-painting-style historical art |
| 🎙️ **Speak** | Microsoft Edge TTS synthesizes a natural Indian-English voiceover |
| 🎞️ **Animate** | Ken Burns zoom/pan effect breathes life into every still image |
| 📝 **Subtitle** | Auto-rendered subtitles with a styled rounded overlay |
| 🎵 **Score** | Background ambient music mixed at 15% volume beneath the voiceover |
| 📦 **Export** | Finishes as a clean H.264 MP4 @ 24fps, ready to share |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     generate_video.py                        │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  1. SCRIPT GENERATION                               │    │
│  │     Google Gemini 2.5 Flash                         │    │
│  │     ├── Vertex AI  (service account — preferred)    │    │
│  │     ├── AI Studio  (GEMINI_API_KEY — fallback)      │    │
│  │     └── Local SCRIPTS dict  (offline — fallback)    │    │
│  └────────────────────┬────────────────────────────────┘    │
│                       │  3 segments: {text, image_prompt}   │
│  ┌────────────────────▼────────────────────────────────┐    │
│  │  2. ASSET GENERATION (per segment)                  │    │
│  │     ├── Pollinations AI  →  PNG image  1280×720     │    │
│  │     └── Edge TTS         →  MP3 voiceover           │    │
│  └────────────────────┬────────────────────────────────┘    │
│                       │                                      │
│  ┌────────────────────▼────────────────────────────────┐    │
│  │  3. VIDEO ASSEMBLY  (MoviePy)                       │    │
│  │     ├── Ken Burns zoom + pan animation              │    │
│  │     ├── Subtitle overlay  (PIL / rounded box)       │    │
│  │     └── Background music  (15% volume mix)          │    │
│  └────────────────────┬────────────────────────────────┘    │
│                       │                                      │
│              🎥  OUTPUT.mp4  (~10 seconds)                   │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+**
- **FFmpeg** (required by MoviePy)

```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg

# Windows (via Chocolatey)
choco install ffmpeg
```

---

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/umarcham/ai-documentary-generator.git
cd ai-documentary-generator

# 2. Install Python dependencies
pip install -r requirements.txt
```

---

### API Setup (Optional but Recommended)

The pipeline has **three layers of intelligence** — it always produces output, even offline.

#### 🥇 Option A — Vertex AI (Best Quality)

1. Create a Google Cloud service account with `Vertex AI User` role
2. Download the JSON key
3. Place it in the project root as `GOOGLE_APPLICATION_CREDENTIALS.json`

> ⚠️ **The credentials file is listed in `.gitignore` and will never be committed.**

#### 🥈 Option B — Google AI Studio API Key

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Get a free key at [aistudio.google.com](https://aistudio.google.com).

#### 🥉 Option C — Offline (No setup needed)

Four fighters are built-in and work with zero credentials:
`Subhas Chandra Bose` · `Bhagat Singh` · `Mahatma Gandhi` · `Rani Lakshmibai`

---

## 🎯 Usage

### Quickstart

```bash
# Default (Subhas Chandra Bose)
python3 generate_video.py

# Generate for any fighter
python3 generate_video.py --fighter "Bhagat Singh"
python3 generate_video.py --fighter "Mahatma Gandhi"
python3 generate_video.py --fighter "Rani Lakshmibai"
python3 generate_video.py --fighter "Sarojini Naidu"   # dynamic via Gemini
```

### Full Options Reference

```bash
python3 generate_video.py \
  --fighter    "Bhagat Singh"              \
  --output     bhagat_singh.mp4            \
  --voice      en-IN-NeerjaNeural          \
  --music-url  https://example.com/bg.mp3  \
  --no-music                               \
  --api-key    YOUR_GEMINI_API_KEY         \
  --creds      /path/to/credentials.json
```

| Flag | Default | Description |
|------|---------|-------------|
| `--fighter` | `Subhas Chandra Bose` | Name of the Indian freedom fighter |
| `--output` | `freedom_fighter.mp4` | Output MP4 filename |
| `--voice` | `en-IN-NeerjaNeural` | Microsoft Edge TTS voice ID |
| `--music-url` | SoundHelix Song 1 | URL to download background music from |
| `--no-music` | `False` | Skip background music entirely |
| `--api-key` | env `GEMINI_API_KEY` | Google AI Studio API key |
| `--creds` | auto-detected | Path to Google service account JSON |

---

## 📁 Project Structure

```
ai-documentary-generator/
│
├── generate_video.py       ← 🧠 Main pipeline — all logic lives here
├── requirements.txt        ← 📦 Python dependencies
├── .gitignore              ← 🔒 Excludes credentials, outputs & temp files
├── README.md               ← 📖 You are here
│
└── temp_assets/            ← ⚡ Auto-created at runtime (gitignored)
    ├── image_1.png
    ├── image_2.png
    ├── image_3.png
    ├── voiceover_1.mp3
    ├── voiceover_2.mp3
    ├── voiceover_3.mp3
    └── background_music.mp3
```

---

## 🧠 AI Priority Chain

```
GOOGLE_APPLICATION_CREDENTIALS.json   ──►  Vertex AI Gemini 2.5 Flash
          ↓ (not found or fails)
    GEMINI_API_KEY env variable        ──►  Google AI Studio Gemini 2.5 Flash
          ↓ (not set or fails)
    Local pre-written SCRIPTS dict     ──►  Offline, no internet required
```

The script **never crashes due to missing credentials** — it gracefully steps down the chain.

---

## 📦 Dependencies

```
requests        HTTP calls to image, music, and Gemini REST APIs
moviepy>=2.0    Video assembly, clip concatenation, audio mixing
edge-tts        Microsoft Edge Text-to-Speech (async)
pillow          Image processing, subtitle rendering, Ken Burns frames
numpy           Frame array manipulation between PIL and MoviePy
google-auth     Loads Vertex AI service account credentials
```

Install all at once:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Troubleshooting

| Symptom | Fix |
|---------|-----|
| `ffmpeg not found` | `brew install ffmpeg` · `sudo apt install ffmpeg` |
| `edge-tts` import error | `pip install edge-tts` |
| Image download fails | Pollinations AI retries 4× automatically — check internet |
| Vertex AI 429 (quota) | Script auto-falls back to AI Studio or local scripts |
| Video has no audio | Confirm `ffmpeg` is installed and accessible in `$PATH` |
| Blank/corrupt image | Re-run — Pollinations occasionally returns empty responses |

---

## 🗺️ Roadmap

- [ ] 🌐 Support for more regional languages via Edge TTS voices
- [ ] 🖼️ Add crossfade transitions between segments
- [ ] ☁️ One-click Google Cloud Run deployment
- [ ] 🎭 Multi-fighter compilation videos (e.g. Top 5 Freedom Fighters)
- [ ] 📱 Vertical 9:16 format for Reels / Shorts output

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

```bash
# Fork → Clone → Branch → Commit → PR
git checkout -b feature/your-feature-name
git commit -m "feat: describe your change"
git push origin feature/your-feature-name
```

---

## 📜 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with ❤️ using Google Gemini · Pollinations AI · Microsoft Edge TTS · MoviePy**

*Honoring the heroes who gave everything for freedom.*

</div>
