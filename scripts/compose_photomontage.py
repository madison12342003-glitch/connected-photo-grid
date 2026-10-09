#!/usr/bin/env python3
"""Render an overlapping 3x3 photomontage from a JSON layer plan.

All source photos remain local. Layers can live on the full canvas (for
cross-tile continuity) or within a named tile A-I. Coordinates are normalized
fractions of the relevant canvas/tile. Requires Pillow.
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

DEFAULT_BG = "#F7F8F8"
TILES = {"A": (0, 0), "B": (1, 0), "C": (2, 0),
         "D": (0, 1), "E": (1, 1), "F": (2, 1),
         "G": (0, 2), "H": (1, 2), "I": (2, 2)}


def open_layer_image(path, box, spec):
    image = Image.open(path).convert("RGBA")
    # Apply restrained, non-destructive tonal treatment to this rendered layer.
    rgb = image.convert("RGB")
    rgb = ImageEnhance.Color(rgb).enhance(float(spec.get("saturation", 1.0)))
    rgb = ImageEnhance.Contrast(rgb).enhance(float(spec.get("contrast", 1.0)))
    brightness = float(spec.get("brightness", 1.0))
    if brightness != 1.0:
        rgb = ImageEnhance.Brightness(rgb).enhance(brightness)
    image = rgb.convert("RGBA")
    image = ImageOps.fit(
        image, box, method=Image.Resampling.LANCZOS,
        centering=tuple(spec.get("centering", [0.5, 0.5]))
    )
    opacity = max(0.0, min(1.0, float(spec.get("opacity", 1.0))))
    if opacity < 1.0:
        alpha = image.getchannel("A").point(lambda p: round(p * opacity))
        image.putalpha(alpha)
    return image


def make_mask(size, polygon=None, feather=0):
    mask = Image.new("L", size, 255)
    if polygon:
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        pts = [(round(float(x) * size[0]), round(float(y) * size[1]))
               for x, y in polygon]
        draw.polygon(pts, fill=255)
    if feather and feather > 0:
        mask = mask.filter(ImageFilter.GaussianBlur(radius=float(feather)))
    return mask


def paste_layer(canvas, spec, photo_root, tile_size):
    source = spec.get("image")
    if not source:
        raise ValueError("Every photo layer must specify an 'image' path.")
    path = Path(source)
    if not path.is_absolute():
        path = photo_root / path
    if not path.is_file():
        raise FileNotFoundError(f"Layer image not found: {path}")

    scope = spec.get("scope", "tile")
    if scope == "canvas":
        base_size = canvas.size
        ox = oy = 0
        target = canvas
    elif scope == "tile":
        tile = str(spec.get("tile", "")).upper()
        if tile not in TILES:
            raise ValueError("Tile-scoped layer needs tile A-I.")
        col, row = TILES[tile]
        base_size = tile_size
        ox, oy = col * tile_size[0], row * tile_size[1]
        target = canvas
    else:
        raise ValueError("Layer scope must be 'canvas' or 'tile'.")

    x = round(float(spec.get("x", 0)) * base_size[0])
    y = round(float(spec.get("y", 0)) * base_size[1])
    w = round(float(spec.get("w", 1)) * base_size[0])
    h = round(float(spec.get("h", 1)) * base_size[1])
    if w < 1 or h < 1:
        raise ValueError("Layer w/h must be positive normalized dimensions.")
    layer = open_layer_image(path, (w, h), spec)
    if spec.get("mask"):
        mask = make_mask((w, h), spec["mask"], spec.get("feather", 0))
        layer.putalpha(ImageChops_multiply(layer.getchannel("A"), mask))
    target.alpha_composite(layer, (ox + x, oy + y))


def ImageChops_multiply(a, b):
    # Pillow's channel multiplication without relying on external packages.
    from PIL import ImageChops
    return ImageChops.multiply(a, b)


def render(plan_path, photo_root, output_dir, tile_size=1000):
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    if tile_size < 200:
        raise ValueError("tile_size must be at least 200.")
    root = Path(photo_root)
    bg = plan.get("background", DEFAULT_BG)
    canvas = Image.new("RGBA", (tile_size * 3, tile_size * 3), bg)
    layers = plan.get("layers")
    if not isinstance(layers, list) or not layers:
        raise ValueError("Plan must contain a non-empty 'layers' array.")
    # Array order is back-to-front z-order. Shared canvas layers naturally cross seams.
    for layer in layers:
        paste_layer(canvas, layer, root, (tile_size, tile_size))

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    full_path = out / "connected-grid.png"
    canvas.convert("RGB").save(full_path, format="PNG", optimize=True)
    for tile, (col, row) in TILES.items():
        crop = canvas.crop((col * tile_size, row * tile_size,
                            (col + 1) * tile_size, (row + 1) * tile_size))
        crop.convert("RGB").save(out / f"{tile}.png", format="PNG", optimize=True)
    return full_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", help="JSON multi-layer render plan")
    parser.add_argument("--photo-root", default="input/photos")
    parser.add_argument("--output-dir", default="output/photomontage")
    parser.add_argument("--tile-size", type=int, default=1000)
    args = parser.parse_args()
    result = render(args.plan, args.photo_root, args.output_dir, args.tile_size)
    print(f"Exported full grid and nine tiles to: {result.parent}")


if __name__ == "__main__":
    main()
