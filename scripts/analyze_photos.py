#!/usr/bin/env python3
"""Extract lightweight, reproducible visual features from local photos.

This is pixel-level analysis, not semantic vision: it can estimate color, brightness,
texture, and dominant edge direction, but cannot reliably name objects or infer story.
"""
import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

COLOR_NAMES = {
    "red": (210, 55, 45), "orange": (225, 135, 55), "yellow": (225, 200, 75),
    "green": (75, 135, 80), "cyan": (80, 175, 180), "blue": (70, 115, 175),
    "purple": (135, 95, 160), "pink": (215, 145, 165), "brown": (125, 85, 55),
    "gray": (145, 145, 140), "white": (235, 232, 222), "black": (40, 40, 38),
}


def color_label(rgb):
    r, g, b = rgb
    if max(r, g, b) < 65:
        return "black"
    if min(r, g, b) > 205:
        return "white"
    if max(r, g, b) - min(r, g, b) < 24:
        return "gray" if sum(rgb) / 3 < 175 else "white"
    return min(COLOR_NAMES, key=lambda name: sum((rgb[i] - ref[i]) ** 2 for i in range(3))
               for ref in [COLOR_NAMES[name]])


def dominant_colors(image, count=4):
    palette = image.convert("RGB").resize((96, 96)).quantize(colors=count, method=Image.Quantize.MEDIANCUT)
    rgb_palette = palette.convert("RGB")
    histogram = palette.getcolors(96 * 96) or []
    colors = []
    for _, index in sorted(histogram, reverse=True):
        rgb = rgb_palette.getpixel((0, 0)) if False else palette.getpalette()[index * 3:index * 3 + 3]
        label = color_label(tuple(rgb))
        if label not in colors:
            colors.append(label)
    return colors[:count]


def analyze_region(gray, box):
    region = gray.crop(box).resize((48, 48))
    px = region.load()
    gx_total = gy_total = edge_total = 0.0
    for y in range(1, 47):
        for x in range(1, 47):
            gx = float(px[x + 1, y]) - float(px[x - 1, y])
            gy = float(px[x, y + 1]) - float(px[x, y - 1])
            magnitude = math.hypot(gx, gy)
            gx_total += abs(gx)
            gy_total += abs(gy)
            edge_total += magnitude
    if gx_total + gy_total < 1:
        direction = 0
    else:
        # Approximate orientation of prominent edges, expressed in degrees modulo 180.
        direction = round(math.degrees(math.atan2(gy_total, gx_total)) % 180)
    if direction < 25 or direction > 155:
        shape = ["horizontal"]
    elif 65 <= direction <= 115:
        shape = ["vertical"]
    else:
        shape = ["diagonal"]
    return {"direction": direction, "shape": shape, "texture": ["detailed"] if edge_total / (46 * 46) > 18 else ["soft"]}


def analyze_image(path):
    with Image.open(path) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
        width, height = image.size
        small = image.resize((min(320, width), max(1, round(height * min(320, width) / width))))
        colors = dominant_colors(small)
        gray = ImageOps.grayscale(small)
        stat = ImageStatFallback(gray)
        w, h = gray.size
        left = analyze_region(gray, (0, 0, max(1, w // 3), h))
        right = analyze_region(gray, (2 * w // 3, 0, w, h))
        top = analyze_region(gray, (0, 0, w, max(1, h // 3)))
        bottom = analyze_region(gray, (0, 2 * h // 3, w, h))
        whole = analyze_region(gray, (0, 0, w, h))
        return {
            "id": path.stem,
            "image": str(path),
            "width": width,
            "height": height,
            "aspect_ratio": round(width / height, 4),
            "colors": colors,
            "brightness": stat["mean"],
            "direction": whole["direction"],
            "shape": whole["shape"],
            "texture": whole["texture"],
            "space": "wide" if width / height > 1.25 else "tall" if height / width > 1.25 else "balanced",
            "left_edge": {**left, "colors": colors},
            "right_edge": {**right, "colors": colors},
            "top_edge": {**top, "colors": colors},
            "bottom_edge": {**bottom, "colors": colors},
            "elements": [],
            "narrative": [],
        }


def ImageStatFallback(image):
    histogram = image.histogram()
    count = sum(histogram)
    mean = sum(value * amount for value, amount in enumerate(histogram)) / max(1, count)
    return {"mean": round(mean, 2)}


def main():
    parser = argparse.ArgumentParser(description="Analyze local photos and emit layout-scoring metadata.")
    parser.add_argument("photo_dir", help="Folder of local image files")
    parser.add_argument("--output", default="output/photo-features.json")
    parser.add_argument("--recursive", action="store_true")
    args = parser.parse_args()
    root = Path(args.photo_dir)
    extensions = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp"}
    paths = sorted(p for p in (root.rglob("*") if args.recursive else root.iterdir())
                   if p.is_file() and p.suffix.lower() in extensions)
    if len(paths) < 9:
        parser.error(f"Need at least 9 supported images; found {len(paths)}")
    records = []
    for path in paths:
        try:
            records.append(analyze_image(path))
        except (OSError, ValueError) as exc:
            print(f"Skipping unreadable image {path}: {exc}")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"photos": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Analyzed {len(records)} images -> {output}")
    print("Note: object names and narrative tags remain empty; add vision-model or human annotations for semantic matching.")


if __name__ == "__main__":
    main()
