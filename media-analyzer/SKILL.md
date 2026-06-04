---
name: media-analyzer
description: Analyze images and videos, then automate video editing in Jianying/CapCut.
---

# Media Analyzer

## Overview

Three workflows:

1. **Image analysis** -- describe what is in a photo
2. **Video analysis** -- extract key frames and describe video content
3. **Jianying automation** -- open Jianying and perform editing operations

## Image Analysis

1. Run `python "<skill>/scripts/analyze_image.py" "<image_path>"` for metadata
2. Use `view_image` for visual inspection
3. Synthesize description: subjects, colors, lighting, text, objects, faces

## Video Analysis

1. Run `python "<skill>/scripts/analyze_video.py" "<video_path>"` to extract frames
2. Review frames with `view_image`
3. Describe content: scenes, pacing, overlays

## Jianying Automation

Prerequisites: Jianying installed, Computer Use plugin loaded.
Launch: list_apps(), filter for JianyingPro, or launch by exe path.
Common operations: import, trim/cut (Ctrl+B), text/subtitles, effects, export (Ctrl+M)

## Dependencies

Python 3, opencv-python, Pillow, Computer Use plugin, JianyingPro