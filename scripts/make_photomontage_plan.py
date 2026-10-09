#!/usr/bin/env python3
"""Create a first-pass overlapping 3x3 photo-layer plan from local image metadata."""
import argparse
import json
from pathlib import Path

TILES = list("ABCDEFGHI")
BACKGROUND = "#F7F8F8"
MASKS = [
    [[0, .08], [.12, 0], [.93, .04], [1, .22], [.92, .96], [.08, 1], [0, .78]],
    [[.05, 0], [.96, .08], [1, .85], [.82, 1], [0, .91], [.08, .18]],
    [[0, .16], [.22, 0], [1, .10], [.94, .92], [.12, 1]],
]


def overlap_score(a, b):
    """Balance shared colors with distinct subjects/textures."""
    ac, bc = set(a.get("colors", [])), set(b.get("colors", []))
    color_similarity = len(ac & bc) / max(1, len(ac | bc))
    ae, be = set(a.get("elements", [])), set(b.get("elements", []))
    element_difference = 1 - len(ae & be) / max(1, len(ae | be)) if ae or be else 0.25
    at, bt = set(a.get("texture", [])), set(b.get("texture", []))
    texture_difference = 1 - len(at & bt) / max(1, len(at | bt)) if at or bt else 0.25
    return 0.45 * color_similarity + 0.35 * element_difference + 0.20 * texture_difference


def choose_heroes(photos):
    if len(photos) < 9:
        raise ValueError(f"Need at least 9 photos; found {len(photos)}")
    pool = list(photos)
    first = max(
        pool,
        key=lambda p: (
            len(p.get("elements", [])) + len(p.get("narrative", [])),
            str(p.get("id", "")),
        ),
    )
    chosen = [first]
    pool.remove(first)
    while len(chosen) < 9:
        candidate = max(
            pool,
            key=lambda p: (
                min(overlap_score(p, selected) for selected in chosen),
                len(p.get("elements", [])),
                str(p.get("id", "")),
            ),
        )
        chosen.append(candidate)
        pool.remove(candidate)
    return chosen


def make_plan(data, photo_root):
    photos = data.get("photos") if isinstance(data, dict) else None
    if not isinstance(photos, list):
        raise ValueError('Input JSON must contain a "photos" array.')
    valid = [p for p in photos if isinstance(p, dict) and p.get("image")]
    if len(valid) < 9:
        raise ValueError("At least nine photo records need an 'image' path.")

    heroes = choose_heroes(valid)
    used = {p["image"] for p in heroes}
    secondary_pool = [p for p in valid if p["image"] not in used] or list(valid)
    bridge_pool = [p for p in valid if p["image"] not in used] or list(valid)
    bridge = max(
        bridge_pool,
        key=lambda p: (len(p.get("elements", [])), str(p.get("id", ""))),
    )

    layers = []
    for index, tile in enumerate(TILES):
        hero = heroes[index]
        candidates = [p for p in secondary_pool if p["image"] != hero["image"]]
        if candidates:
            secondary = max(
                candidates,
                key=lambda p: (overlap_score(hero, p), str(p.get("id", ""))),
            )
        else:
            secondary = valid[(index + 1) % len(valid)]

        layers.append({
            "image": secondary["image"], "scope": "tile", "tile": tile,
            "x": 0, "y": 0, "w": 1, "h": 1,
            "saturation": 0.58, "contrast": 0.92, "opacity": 0.48,
            "role": "ghost-underlay", "source_id": secondary.get("id", ""),
        })
        layers.append({
            "image": hero["image"], "scope": "tile", "tile": tile,
            "x": 0.045 if index % 2 == 0 else 0.10,
            "y": 0.07 if index % 3 else 0.12,
            "w": 0.90 if index % 2 == 0 else 0.84,
            "h": 0.82 if index % 3 else 0.78,
            "saturation": 0.92, "contrast": 1.03, "opacity": 1,
            "mask": MASKS[index % len(MASKS)], "feather": 2,
            "role": "hero", "source_id": hero.get("id", ""),
        })

    # Draw after tile layers so the shared bridge remains visible across A/B.
    layers.append({
        "image": bridge["image"], "scope": "canvas",
        "x": 0.285, "y": 0.035, "w": 0.43, "h": 0.19,
        "saturation": 0.72, "contrast": 0.98, "opacity": 0.82,
        "mask": [[0, .18], [.12, 0], [.9, .06], [1, .28], [.88, .92], [.1, 1]],
        "feather": 5, "role": "cross-tile-bridge",
        "source_id": bridge.get("id", ""),
    })
    return {
        "background": BACKGROUND,
        "palette": {"background": BACKGROUND, "ink": "#17191B", "accent": "#B52B35"},
        "notes": [
            "First-pass automatic plan; review crops and layer order before export.",
            "Each tile has a distinct hero and a partially transparent underlay.",
            "One shared photo bridge crosses the A/B boundary; review its crop and position.",
            "No Tibetan text is generated automatically; use verified text and a Tibetan-capable font.",
        ],
        "source_photo_root": str(photo_root),
        "layers": layers,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("features")
    parser.add_argument("--photo-root", default="input/photos")
    parser.add_argument("--output", default="output/photomontage-plan.json")
    args = parser.parse_args()
    data = json.loads(Path(args.features).read_text(encoding="utf-8"))
    plan = make_plan(data, args.photo_root)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(plan['layers'])} photo layers for nine tiles -> {output}")
    print("Review the JSON before rendering; automatic selection is a first draft.")


if __name__ == "__main__":
    main()
