# Codex Media Analyzer

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-6E42D4)](https://codex.openai.com)
[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey)]()
[![Cut](https://img.shields.io/badge/CapCut-JianyingPro-orange)]()

> **Give codex the ability to see your photos and videos, then edit them in CapCut/Jianying — entirely through natural language.**

---

## What It Does

| You tell Codex | Codex executes |
|---|---|
| *"What's in this photo?"* | Reads EXIF metadata, analyzes color histogram, detects faces, then describes the scene using AI vision |
| *"Summarize this video"* | Extracts duration/FPS/codec, detects scene cuts via HSV histogram comparison, samples key frames, describes each scene |
| *"Open CapCut, import this clip, trim first 5s, add 'My Trip' title, export 1080p"* | Launches Jianying via Computer Use, splits and deletes the intro, adds text, exports — no manual clicks |

---

## Capabilities

### Image Recognition `analyze_image.py`

| Feature | Description |
|---|---|
| **Format detection** | JPEG / PNG / WebP / BMP / TIFF — with color mode and dimensions |
| **EXIF extraction** | Camera model, date taken, GPS coordinates, ISO, aperture, shutter speed |
| **Color analysis** | Per-channel histogram peaks, mean RGB, standard deviation |
| **Brightness score** | Numeric value + auto-labeling (dark / moderate / bright) |
| **Face detection** | OpenCV Haar cascade — face count + bounding box coordinates |
| **AI scene description** | Codex vision model describes subjects, lighting, mood, artifacts |

**Why it's useful:**
- Batch-analyze photo folders: find shots with people, flag underexposed images, sort by camera body
- Pre-upload QA: verify product photo dimensions, color accuracy, brightness
- Legal/forensic: extract EXIF timestamps and GPS for timeline reconstruction

### Video Analysis `analyze_video.py`

| Feature | Description |
|---|---|
| **Technical metadata** | Duration, FPS, resolution, codec (FourCC), frame count, file size |
| **Scene-change detection** | HSV histogram comparison between consecutive frames — finds natural cut points |
| **Key frame extraction** | Saves JPEG snapshots at uniform intervals + every detected scene change |
| **Configurable sensitivity** | `--count N` for uniform frames, `--scene-threshold T` (0-100), `--max-frames N` |
| **AI scene narration** | Codex describes each extracted frame, synthesizes into timeline narrative |

**Why it's useful:**
- "Before I watch this 2-hour lecture, show me the slides" → extracts whiteboard/key frame moments
- "Where does the scene change from indoors to outdoors?" → scene detection pinpoints the exact timestamp
- "Generate 10 thumbnails from this drone footage" → uniform sampling + scene cuts

### CapCut / Jianying Automation

| Operation | How |
|---|---|
| **Launch** | Auto-detects JianyingPro install path, opens app |
| **Import** | Clicks import button or triggers drag-and-drop on media panel |
| **Cut / Split** | `Ctrl+B` at playhead, `Delete` to remove selected clip |
| **Trim** | Drags clip edges on timeline |
| **Text & Subtitles** | Navigates to text panel, selects style, types content |
| **Effects & Transitions** | Opens effects panel, drags onto timeline, places between clips |
| **Export** | `Ctrl+M`, configures format/resolution/bitrate, clicks Export |

**Why it's useful:**
- *"Join today's 5 best takes, add crossfade, put 'Highlights' at the start, export 1080p"* — done in one sentence
- *"Remove the intro from this screen recording and add a watermark"* — no timeline scrubbing
- *"Add auto-generated Chinese subtitles to this interview"* — one command

---

## Quick Start

```bash
# Install dependencies
pip install opencv-python Pillow

# Analyze an image
python scripts/analyze_image.py photo.jpg

# Analyze a video (8 uniform frames + scene detection)
python scripts/analyze_video.py video.mp4 --count 8 --scene-threshold 30

# Use in Codex
# Just say: "What's in this photo?" or "Open CapCut and edit this video"
```

### Example: Image Analysis Output

```json
{
  "filename": "DSC_0421.jpg",
  "format": "JPEG",
  "width": 4032,
  "height": 3024,
  "megapixels": 12.19,
  "exif": {"Model": "NIKON D750", "DateTime": "2024:07:15 14:22:08", "ISOSpeedRatings": "400"},
  "mean_rgb": [128, 145, 160],
  "mean_brightness": 142.3,
  "brightness_label": "moderate",
  "faces_detected": 2,
  "face_boxes": [{"x": 1200, "y": 800, "w": 300, "h": 380}]
}
```

### Example: Video Analysis Output

```json
{
  "filename": "drone_footage.mp4",
  "duration_seconds": 124.5,
  "fps": 30.0,
  "total_frames": 3735,
  "width": 1920,
  "height": 1080,
  "codec_fourcc": "avc1",
  "frames_extracted": 12,
  "frames": [
    {"file": "frame_0000.jpg", "timestamp": "0:00", "reason": "uniform"},
    {"file": "frame_0003.jpg", "timestamp": "0:18", "reason": "scene_change(45.2)"}
  ]
}
```

---

## Architecture

```
User says: "What's in this photo?"
        │
        ▼
┌──────────────────┐     ┌─────────────────┐
│  Codex (LLM)     │────▶│ analyze_image.py │──▶ JSON metadata
│  orchestrates    │     │ OpenCV + Pillow  │    + face boxes
└──────────────────┘     └─────────────────┘
        │                        │
        ▼                        ▼
┌──────────────────┐     ┌─────────────────┐
│  view_image tool │     │  work/frames/    │
│  AI vision desc  │     │  extracted JPEGs │
└──────────────────┘     └─────────────────┘
                                  │
User says: "Edit in CapCut"      │
        │                        │
        ▼                        ▼
┌──────────────────┐     ┌─────────────────┐
│  Computer Use    │────▶│  Jianying/CapCut │
│  desktop control │     │  desktop app     │
└──────────────────┘     └─────────────────┘
```

---

## Why This Skill

Most AI assistants are text-only. `media-analyzer` gives Codex **multimodal perception + desktop agency**:

- **All local** — no cloud uploads, everything runs on your machine via Python + OpenCV
- **No learning curve** — you speak natural language, Codex handles APIs and app UIs
- **End-to-end** — from "what's in this video" to "now edit it in CapCut" in one conversation
- **Extensible** — the JSON output from analysis scripts feeds any downstream workflow

---

## Project Structure

```
media-analyzer/
  SKILL.md              # Codex skill definition
  README.md             # This file
  LICENSE               # MIT
  .gitignore
  scripts/
    analyze_image.py    # EXIF + histogram + brightness + face detection
    analyze_video.py    # Metadata + scene-cut detection + key frame extraction
  work/
    frames/             # Extracted frame JPEGs
```

---

## Dependencies

- Python 3.9+ with `opencv-python`, `Pillow`
- Windows / macOS (for Computer Use + Jianying)
- [JianyingPro](https://www.capcut.cn/) (CapCut desktop)

---

## License

MIT — see [LICENSE](LICENSE)
