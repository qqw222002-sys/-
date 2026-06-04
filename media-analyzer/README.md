# Codex Media Analyzer

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-8A2BE2.svg)](https://codex.openai.com)

> AI-powered image recognition and video analysis skill for Codex, with Jianying/CapCut desktop automation.

## Features

### Image Analysis — `analyze_image.py`
Metadata extraction (dimensions, format, EXIF), color histogram analysis (RGB peaks, mean/std, brightness), face detection (OpenCV Haar cascades), JSON output.

### Video Analysis — `analyze_video.py`
Metadata (duration, FPS, codec), scene-change detection (HSV histogram comparison), uniform-interval frame sampling, configurable sensitivity and frame limits.

### Jianying (CapCut) Automation
Launch and control Jianying via Computer Use: import media, timeline splitting/trimming, text/subtitles, effects/transitions, export via Ctrl+M.

## Quick Start

```bash
pip install opencv-python Pillow
python scripts/analyze_image.py photo.jpg
python scripts/analyze_video.py video.mp4 --count 8
```

## License

MIT — see LICENSE