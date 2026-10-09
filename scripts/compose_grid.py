#!/usr/bin/env python3
"""Render a ranked 3x3 photo layout into a high-resolution PNG.

Input photos stay local; the repository only contains scripts and example plans.
Requires Pillow: python -m pip install Pillow
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

DEFAULT_BG = "#F7F4EE"
DEFAULT_INK = "#1E1D1B"
DEFAULT_ACCENT = "#B82E2E"


def load_font(font_path, size):
    if font_path:
        return ImageFont.truetype(font_path, size=size)
    # Pillow's default font is a safe fallback, but non-Latin glyphs may be missing.
    try:
        candidates = [
            "/System/Library/Fonts/PingFang.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "C:/Windows/Fonts/msyh.ttc",
        ]
        for candidate in candidates:
            if Path(candidate).exists():
                return ImageFont.truetype(candidate, size=size)
    except OSError:
        pass
    return ImageFont.load_default()


def crop_cover(image, size):
    return ImageOps.fit(image.convert("RGB"), size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def render(plan_path, layout_path, output_path, photo_root, size=3000):
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    ranked = json.loads(Path(layout_path).read_text(encoding="utf-8"))
    if isinstance(ranked, dict) and "layout" in ranked:
        ranked = [ranked]
    if not isinstance(ranked, list) or not ranked or "layout" not in ranked[0]:
        raise ValueError("Layout JSON must be the scorer output (a list containing a layout).")
    grid = ranked[0]["layout"]
    if len(grid) != 3 or any(len(row) != 3 for row in grid):
        raise ValueError("Layout must be exactly 3x3.")
    tiles = plan.get("tiles", {})
    root = Path(photo_root)
    gutter = int(plan.get("gutter", 24))
    margin = int(plan.get("margin", 36))
    bg = plan.get("background", DEFAULT_BG)
    ink = plan.get("ink", DEFAULT_INK)
    accent = plan.get("accent", DEFAULT_ACCENT)
    cell = (size - 2 * margin - 2 * gutter) // 3
    canvas = Image.new("RGB", (size, size), bg)
    draw = ImageDraw.Draw(canvas)

    for r, row in enumerate(grid):
        for c, photo_id in enumerate(row):
            spec = tiles.get(str(photo_id), {})
            image_path = root / spec.get("image", f"{photo_id}.jpg")
            if not image_path.is_file():
                raise FileNotFoundError(f"Missing photo for {photo_id}: {image_path}")
            image = Image.open(image_path)
            tile = crop_cover(image, (cell, cell))
            x = margin + c * (cell + gutter)
            y = margin + r * (cell + gutter)
            canvas.paste(tile, (x, y))
            overlay = Image.new("RGBA", (cell, cell), (0, 0, 0, 0))
            od = ImageDraw.Draw(overlay)
            # A restrained gradient-like bottom panel keeps captions readable.
            panel_h = int(cell * 0.23)
            od.rectangle((0, cell - panel_h, cell, cell), fill=(247, 244, 238, 220))
            title = spec.get("title", "")
            caption = spec.get("caption", "")
            title_font = load_font(plan.get("font"), max(18, int(cell * 0.075)))
            caption_font = load_font(plan.get("font"), max(14, int(cell * 0.032)))
            if title:
                od.text((int(cell * 0.055), cell - panel_h + int(cell * 0.025)),
                        title, font=title_font, fill=ink)
            if caption:
                od.text((int(cell * 0.055), cell - int(cell * 0.055)),
                        caption, font=caption_font, fill=ink)
            # Small red editorial marker; does not alter source photo pixels.
            od.rectangle((int(cell * 0.055), int(cell * 0.055),
                          int(cell * 0.11), int(cell * 0.065)), fill=accent)
            canvas.paste(overlay, (x, y), overlay)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, format="PNG", optimize=True)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Render a 3x3 editorial photo collage from a ranked layout.")
    parser.add_argument("plan", help="JSON tile plan containing local image paths and optional text")
    parser.add_argument("layout", help="JSON output from scripts/score_layout.py")
    parser.add_argument("--photo-root", default="input/photos", help="Directory holding local source photos")
    parser.add_argument("--output", default="output/sichuan-grid.png")
    parser.add_argument("--size", type=int, default=3000, help="Square output size in pixels")
    args = parser.parse_args()
    if args.size < 600:
        parser.error("--size must be at least 600 pixels")
    path = render(args.plan, args.layout, args.output, args.photo_root, args.size)
    print(f"Exported: {path}")


if __name__ == "__main__":
    main()
