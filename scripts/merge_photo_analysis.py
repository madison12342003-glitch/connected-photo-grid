#!/usr/bin/env python3
"""Merge pixel features with semantic descriptions from describe_photos_ollama.py."""
import argparse
import json
from pathlib import Path


def merge(pixel_data, semantic_data):
    semantic_by_id = {str(p.get("id")): p for p in semantic_data.get("photos", [])}
    merged = []
    for photo in pixel_data.get("photos", []):
        semantic = semantic_by_id.get(str(photo.get("id")), {})
        item = dict(photo)
        objects = semantic.get("objects", [])
        scene = semantic.get("scene", [])
        mood = semantic.get("mood", [])
        item["elements"] = sorted({str(x).lower() for x in objects + scene})
        item["narrative"] = sorted({str(x).lower() for x in mood})
        item["caption"] = semantic.get("caption", "")
        item["composition"] = semantic.get("composition", {})
        item["text_visible"] = semantic.get("text_visible", [])
        item["semantic_analysis_available"] = bool(semantic)
        merged.append(item)
    return {"photos": merged}


def main():
    parser = argparse.ArgumentParser(description="Merge pixel and semantic photo analysis JSON.")
    parser.add_argument("pixel_json")
    parser.add_argument("semantic_json")
    parser.add_argument("--output", default="output/combined-features.json")
    args = parser.parse_args()
    pixel = json.loads(Path(args.pixel_json).read_text(encoding="utf-8"))
    semantic = json.loads(Path(args.semantic_json).read_text(encoding="utf-8"))
    result = merge(pixel, semantic)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Merged {len(result['photos'])} photo records -> {output}")


if __name__ == "__main__":
    main()
