#!/usr/bin/env python3
"""Analyze a video file: metadata, key frame extraction with scene-change detection."""

import sys, json, os, argparse

def analyze_video(video_path: str, uniform_count=8, scene_threshold=30, max_frames=20) -> dict:
    import cv2, numpy as np
    result = {"path": os.path.abspath(video_path), "filename": os.path.basename(video_path), "size_bytes": os.path.getsize(video_path)}
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        result["error"] = "Could not open video file"; cap.release(); return result
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc_int = int(cap.get(cv2.CAP_PROP_FOURCC))
    fourcc = "".join([chr((fourcc_int >> 8 * i) & 0xFF) for i in range(4)])
    duration = total_frames / fps if fps > 0 else 0
    duration_str = f"{int(duration // 60)}:{int(duration % 60):02d}"
    result.update({"duration_seconds": round(duration, 2), "duration_hms": duration_str, "fps": round(fps, 2), "total_frames": total_frames, "width": width, "height": height, "codec_fourcc": fourcc})
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frames_dir = os.path.join(skill_dir, "work", "frames"); os.makedirs(frames_dir, exist_ok=True)
    for old in os.listdir(frames_dir):
        if old.startswith("frame_") and old.endswith(".jpg"): os.remove(os.path.join(frames_dir, old))
    extracted_frames = []
    target_interval = max(1, total_frames // uniform_count) if uniform_count > 0 else total_frames
    uniform_targets = set(i * target_interval for i in range(uniform_count))
    prev_hist, saved_count, frame_idx = None, 0, 0
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    while True:
        ret, frame = cap.read()
        if not ret: break
        should_save, reason = False, ""
        if frame_idx in uniform_targets: should_save, reason = True, "uniform"
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
        cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
        if prev_hist is not None:
            diff = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CHISQR)
            if diff > scene_threshold * 10: should_save, reason = True, f"scene_change({diff:.1f})"
        prev_hist = hist
        if should_save and saved_count < max_frames:
            frame_filename = f"frame_{saved_count:04d}.jpg"
            frame_path = os.path.join(frames_dir, frame_filename)
            cv2.imwrite(frame_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            timestamp = frame_idx / fps if fps > 0 else 0
            ts_str = f"{int(timestamp // 60)}:{int(timestamp % 60):02d}"
            extracted_frames.append({"file": frame_filename, "frame_index": frame_idx, "timestamp": ts_str, "reason": reason})
            saved_count += 1
        frame_idx += 1
    cap.release()
    result["frames_extracted"] = saved_count; result["frames"] = extracted_frames
    result["frames_directory"] = frames_dir; result["uniform_interval"] = target_interval
    return result

def main():
    parser = argparse.ArgumentParser(description="Analyze video and extract key frames")
    parser.add_argument("video_path")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--scene-threshold", type=int, default=30)
    parser.add_argument("--max-frames", type=int, default=20)
    args = parser.parse_args()
    if not os.path.isfile(args.video_path):
        print(json.dumps({"error": f"File not found: {args.video_path}"}, indent=2)); sys.exit(1)
    result = analyze_video(args.video_path, args.count, args.scene_threshold, args.max_frames)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

if __name__ == "__main__":
    main()