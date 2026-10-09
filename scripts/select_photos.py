#!/usr/bin/env python3
"""Choose a diverse nine-photo shortlist from pixel-level feature metadata.

This is a heuristic shortlist, not semantic curation: it balances color, geometry,
brightness, and aspect ratio. Review the resulting nine photos before final export.
"""
import argparse
import json
from pathlib import Path


def color_distance(a, b):
    ca, cb = set(a.get("colors", [])), set(b.get("colors", []))
    union = ca | cb
    color = 1.0 - (len(ca & cb) / len(union) if union else 0.0)
    direction = abs(float(a.get("direction", 0)) - float(b.get("direction", 0))) % 180
    direction = min(direction, 180 - direction) / 90
    brightness = min(1.0, abs(float(a.get("brightness", 128)) - float(b.get("brightness", 128))) / 128)
    ratio = min(1.0, abs(float(a.get("aspect_ratio", 1)) - float(b.get("aspect_ratio", 1))) / 2)
    return 0.45 * color + 0.25 * direction + 0.20 * brightness + 0.10 * ratio


def choose_nine(photos):
    if len(photos) < 9:
        raise ValueError(f"Need at least 9 photos; got {len(photos)}")
    # Start with the image whose palette is closest to the collection's median palette
    # by selecting a deterministic first item, then greedily maximize minimum distance.
    selected = [photos[0]]
    remaining = photos[1:]
    while len(selected) < 9:
        candidate = max(
            remaining,
            key=lambda p: (min(color_distance(p, s) for s in selected), str(p.get("id", "")))
        )
        selected.append(candidate)
        remaining.remove(candidate)
    return selected


def main():
    parser = argparse.ArgumentParser(description="Select a diverse nine-photo shortlist.")
    parser.add_argument("input", help="JSON emitted by scripts/analyze_photos.py")
    parser.add_argument("--output", default="output/nine-photo-features.json")
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("photos"), list):
        parser.error('Input JSON must contain a "photos" array')
    chosen = choose_nine(data["photos"])
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"photos": chosen}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Shortlisted nine photos (heuristic; please review):")
    for photo in chosen:
        print(f"- {photo.get('id')}: {photo.get('image', '')}")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
