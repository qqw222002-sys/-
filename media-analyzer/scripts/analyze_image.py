#!/usr/bin/env python3
"""Analyze an image file: dimensions, format, color profile, dominant colors, face detection."""

import sys
import json
import os

def analyze_image(image_path: str) -> dict:
    result = {
        "path": os.path.abspath(image_path),
        "filename": os.path.basename(image_path),
        "size_bytes": os.path.getsize(image_path),
    }
    try:
        from PIL import Image, ExifTags
        img = Image.open(image_path)
        result["format"] = img.format
        result["mode"] = img.mode
        result["width"] = img.width
        result["height"] = img.height
        result["aspect_ratio"] = f"{img.width}:{img.height}" if img.height else "N/A"
        result["megapixels"] = round((img.width * img.height) / 1_000_000, 2)
        exif_data = img.getexif()
        if exif_data:
            exif = {}
            for tag_id, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
                try:
                    exif[tag_name] = str(value)
                except Exception:
                    exif[tag_name] = "<unprintable>"
            if exif:
                result["exif"] = exif
        img.close()
    except Exception as e:
        result["pillow_error"] = str(e)
    try:
        import cv2
        import numpy as np
        bgr = cv2.imread(image_path)
        if bgr is not None:
            h, w = bgr.shape[:2]
            result["opencv_width"] = w
            result["opencv_height"] = h
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            pixels = rgb.reshape(-1, 3)
            r_hist = cv2.calcHist([rgb], [0], None, [64], [0, 256])
            g_hist = cv2.calcHist([rgb], [1], None, [64], [0, 256])
            b_hist = cv2.calcHist([rgb], [2], None, [64], [0, 256])
            def peak_color(ch_hist, name):
                max_idx = int(np.argmax(ch_hist))
                center = max_idx * 4 + 2
                return {"channel": name, "peak_bin": max_idx, "center_value": center}
            result["histogram_peaks"] = [
                peak_color(r_hist, "R"), peak_color(g_hist, "G"), peak_color(b_hist, "B"),
            ]
            mean_rgb = np.mean(pixels, axis=0).astype(int)
            std_rgb = np.std(pixels, axis=0).astype(int)
            result["mean_rgb"] = [int(mean_rgb[0]), int(mean_rgb[1]), int(mean_rgb[2])]
            result["std_rgb"] = [int(std_rgb[0]), int(std_rgb[1]), int(std_rgb[2])]
            gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
            result["mean_brightness"] = round(float(np.mean(gray)), 1)
            result["brightness_label"] = (
                "dark" if result["mean_brightness"] < 85
                else "bright" if result["mean_brightness"] > 170
                else "moderate"
            )
            cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            face_cascade = cv2.CascadeClassifier(cascade_path)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            result["faces_detected"] = len(faces)
            if len(faces) > 0:
                result["face_boxes"] = [
                    {"x": int(f[0]), "y": int(f[1]), "w": int(f[2]), "h": int(f[3])}
                    for f in faces.tolist()
                ]
        else:
            result["opencv_error"] = "Could not read image with OpenCV"
    except Exception as e:
        result["opencv_error"] = str(e)
    return result

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: analyze_image.py IMAGE_PATH"}, indent=2))
        sys.exit(1)
    image_path = sys.argv[1]
    if not os.path.isfile(image_path):
        print(json.dumps({"error": f"File not found: {image_path}"}, indent=2))
        sys.exit(1)
    result = analyze_image(image_path)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

if __name__ == "__main__":
    main()