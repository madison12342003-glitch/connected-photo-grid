#!/usr/bin/env python3
"""Create an editable renderer plan from selected photo feature metadata."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Generate a starter tile plan from selected photo metadata.")
    parser.add_argument("input", help="JSON emitted by scripts/select_photos.py")
    parser.add_argument("--output", default="output/render-plan.json")
    parser.add_argument("--photo-root", default="input/photos",
                        help="Folder used by compose_grid.py; paths in plan are stored as basenames")
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    photos = data.get("photos") if isinstance(data, dict) else None
    if not isinstance(photos, list) or len(photos) != 9:
        parser.error('Input must contain exactly 9 records in a "photos" array')
    tiles = {}
    for photo in photos:
        image = Path(photo.get("image", str(photo.get("id", "") + ".jpg"))).name
        photo_id = str(photo["id"])
        tiles[photo_id] = {"image": image, "title": "", "caption": ""}
    plan = {
        "background": "#F7F4EE", "ink": "#1E1D1B", "accent": "#B82E2E",
        "margin": 36, "gutter": 24, "font": None, "photo_root_hint": args.photo_root,
        "tiles": tiles,
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Created editable plan: {out}")
    print("Add title/caption text in the plan before rendering if desired.")


if __name__ == "__main__":
    main()
