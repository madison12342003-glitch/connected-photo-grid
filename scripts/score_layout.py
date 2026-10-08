#!/usr/bin/env python3
"""
Score 3x3 connected-photo layouts.

This is a lightweight, dependency-free prototype. It does not inspect pixels.
Instead, it scores structured visual features supplied by an upstream vision model
or a human annotator.

Input JSON:
{
  "photos": [
    {
      "id": "A",
      "direction": 30,
      "shape": ["ridge", "diagonal"],
      "colors": ["green", "white"],
      "elements": ["mountain", "cloud"],
      "texture": ["rock"],
      "space": "left"
    }
  ]
}

All numeric fields are optional. The script also accepts per-photo tags.
Direction is an angle in degrees describing the dominant visual movement.

Output: top layouts ranked by the sum of the 12 adjacent-pair scores.
"""

import argparse
import itertools
import json
import math
from typing import Dict, Iterable, List, Sequence, Tuple

DIMENSIONS = ("direction", "shape", "color", "object", "texture", "space", "narrative")
WEIGHTS = {
    "direction": 2.0,
    "shape": 1.5,
    "color": 1.0,
    "object": 1.0,
    "texture": 0.75,
    "space": 0.75,
    "narrative": 0.5,
}


def as_set(value) -> set:
    if value is None:
        return set()
    if isinstance(value, str):
        return {value.lower()}
    return {str(x).lower() for x in value}


def tag_score(a, b) -> float:
    sa, sb = as_set(a), as_set(b)
    if not sa or not sb:
        return 0.0
    inter = len(sa & sb)
    union = len(sa | sb)
    return 5.0 * inter / union if union else 0.0


def direction_score(a, b) -> float:
    """Higher when dominant directions are compatible.

    A 180-degree flip can still connect because a visual line can leave one
    tile and continue into its neighbor. We therefore use the smaller angle
    between the two orientations.
    """
    if a is None or b is None:
        return 0.0
    diff = abs((float(a) - float(b)) % 180.0)
    diff = min(diff, 180.0 - diff)
    return 5.0 * (1.0 - diff / 90.0)


def scalar_score(a, b) -> float:
    if a is None or b is None:
        return 0.0
    try:
        return 5.0 * (1.0 - min(abs(float(a) - float(b)), 1.0))
    except (TypeError, ValueError):
        return 0.0


def edge_score(a: dict, b: dict, edge: str) -> Tuple[float, Dict[str, float]]:
    """Score the two edges that actually touch.

    The edge-specific fields are optional:
      right_edge / left_edge for horizontal neighbors
      bottom_edge / top_edge for vertical neighbors

    Each edge may contain direction, shapes, colors, elements, texture,
    and space. When edge data is absent, the function falls back to the
    whole-photo features.
    """
    if edge == "horizontal":
        ea = a.get("right_edge", {})
        eb = b.get("left_edge", {})
    else:
        ea = a.get("bottom_edge", {})
        eb = b.get("top_edge", {})

    def pick(name, whole_a, whole_b):
        va = ea.get(name, whole_a)
        vb = eb.get(name, whole_b)
        return va, vb

    ad, bd = pick("direction", a.get("direction"), b.get("direction"))
    ashape, bshape = pick("shape", a.get("shape"), b.get("shape"))
    acolor, bcolor = pick("colors", a.get("colors", a.get("color")), b.get("colors", b.get("color")))
    aobj, bobj = pick("elements", a.get("elements", a.get("object")), b.get("elements", b.get("object")))
    atex, btex = pick("texture", a.get("texture"), b.get("texture"))
    aspace, bspace = pick("space", a.get("space"), b.get("space"))
    anar, bnar = pick("narrative", a.get("narrative"), b.get("narrative"))

    details = {
        "direction": direction_score(ad, bd),
        "shape": tag_score(ashape, bshape),
        "color": tag_score(acolor, bcolor),
        "object": tag_score(aobj, bobj),
        "texture": tag_score(atex, btex),
        "space": tag_score(aspace, bspace),
        "narrative": tag_score(anar, bnar),
    }
    total_weight = sum(WEIGHTS.values())
    weighted = sum(details[k] * WEIGHTS[k] for k in DIMENSIONS)
    return weighted / total_weight * 5.0, details


def adjacency_pairs(layout: Sequence[str]) -> Iterable[Tuple[str, str]]:
    # A B C
    # D E F
    # G H I
    for row in range(3):
        for col in range(2):
            yield layout[row * 3 + col], layout[row * 3 + col + 1]
    for row in range(2):
        for col in range(3):
            yield layout[row * 3 + col], layout[(row + 1) * 3 + col]


def layout_score(layout: Sequence[str], matrix: Dict[Tuple[str, str], float]) -> float:
    return sum(matrix[(a, b)] for a, b in adjacency_pairs(layout))


def score_all(photos: List[dict], top_k: int) -> List[dict]:
    ids = [p["id"] for p in photos]
    by_id = {p["id"]: p for p in photos}

    matrix: Dict[Tuple[str, str], float] = {}
    details: Dict[Tuple[str, str], Dict[str, float]] = {}
    for i, a in enumerate(photos):
        for b in photos[i + 1:]:
            score, d = pair_score(a, b)
            matrix[(a["id"], b["id"])] = score
            matrix[(b["id"], a["id"])] = score
            details[(a["id"], b["id"])] = d
            details[(b["id"], a["id"])] = d

    ranked = []
    for perm in itertools.permutations(ids):
        total = layout_score(perm, matrix)
        ranked.append((total, perm))
    ranked.sort(reverse=True, key=lambda x: x[0])

    results = []
    for total, perm in ranked[:top_k]:
        edges = []
        for a, b in adjacency_pairs(perm):
            edges.append({
                "from": a,
                "to": b,
                "score": round(matrix[(a, b)], 3),
            })
        results.append({
            "layout": [list(perm[0:3]), list(perm[3:6]), list(perm[6:9])],
            "score": round(total, 3),
            "average_edge_score": round(total / 12.0, 3),
            "edges": edges,
        })
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank 3x3 connected-photo layouts.")
    parser.add_argument("input", help="JSON file containing exactly 9 photo feature records")
    parser.add_argument("--top", type=int, default=10, help="Number of layouts to return")
    parser.add_argument("--output", help="Optional JSON output file")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    photos = data["photos"]
    if len(photos) != 9:
        raise SystemExit("Expected exactly 9 photos. Select the nine candidates before layout scoring.")

    ids = [p.get("id") for p in photos]
    if any(not x for x in ids) or len(set(ids)) != 9:
        raise SystemExit("Each photo must have a unique non-empty 'id'.")

    results = score_all(photos, max(1, args.top))
    payload = {
        "method": {
            "adjacency_edges": 12,
            "dimensions": DIMENSIONS,
            "weights": WEIGHTS,
            "note": "Prototype score; it ranks supplied feature descriptions and does not inspect image pixels."
        },
        "results": results,
    }

    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    else:
        print(text)


if __name__ == "__main__":
    main()
