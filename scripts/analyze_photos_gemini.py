#!/usr/bin/env python3
"""Batch semantic analysis of local photos using the official Gemini API.

Input can be a photo directory or pixel-feature JSON emitted by analyze_photos.py.
Images are sent one at a time; only the explicitly selected directory/files are processed.
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

from analyze_photo import analyze_image

EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

def find_images(source: Path, recursive: bool):
    if source.is_file() and source.suffix.lower() == ".json":
        data = json.loads(source.read_text(encoding="utf-8"))
        photos = data.get("photos") if isinstance(data, dict) else None
        if not isinstance(photos, list):
            raise ValueError('Input JSON must contain a "photos" array')
        paths = []
        for record in photos:
            image = record.get("image")
            if image:
                path = Path(image)
                if not path.is_absolute():
                    path = Path.cwd() / path
                paths.append(path)
        return paths
    if not source.is_dir():
        raise FileNotFoundError(f"Source folder or feature JSON not found: {source}")
    iterator = source.rglob("*") if recursive else source.iterdir()
    return sorted(p for p in iterator if p.is_file() and p.suffix.lower() in EXTENSIONS)

def main():
    parser = argparse.ArgumentParser(description="Analyze local photos with Gemini and save semantic JSON.")
    parser.add_argument("source", help="Photo folder or photo-feature JSON with image paths")
    parser.add_argument("--output", default="output/gemini-photo-analysis.json")
    parser.add_argument("--model", default=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-lite"))
    parser.add_argument("--limit", type=int, help="Optional maximum number of photos (useful for a low-cost pilot)")
    parser.add_argument("--recursive", action="store_true", help="Search nested folders when source is a directory")
    parser.add_argument("--pause", type=float, default=0.0, help="Seconds to wait between requests")
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be at least 1")
    if args.pause < 0:
        parser.error("--pause cannot be negative")
    try:
        paths = find_images(Path(args.source), args.recursive)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    if args.limit:
        paths = paths[:args.limit]
    if not paths:
        parser.error("No supported images found")
    if not os.environ.get("GEMINI_API_KEY"):
        parser.error("Set GEMINI_API_KEY in your environment before running cloud analysis")

    records, errors = [], []
    for index, path in enumerate(paths, 1):
        print(f"[{index}/{len(paths)}] Analyzing {path}", file=sys.stderr)
        try:
            data = analyze_image(str(path), model=args.model)
            # Keep compatibility with merge_photo_analysis.py while preserving full Gemini output.
            records.append({
                "id": path.stem, "image": str(path),
                "objects": data["elements"], "scene": [data["scene_type"]],
                "mood": [data["narrative_role"]], "caption": data["subject"],
                "composition": data["composition"], "text_visible": [],
                "colors": data["colors"], "elements": data["elements"],
                "edge_features": data["edge_features"], "narrative_role": data["narrative_role"],
                "confidence": data["confidence"], "notes": data["notes"],
            })
        except Exception as exc:
            errors.append({"image": str(path), "error": str(exc)})
            print(f"  Skipped after error: {exc}", file=sys.stderr)
        if args.pause and index < len(paths):
            time.sleep(args.pause)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"photos": records, "errors": errors, "model": args.model}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(records)} analyses to {output}; {len(errors)} failed.")
    if not records:
        sys.exit(1)

if __name__ == "__main__":
    main()
