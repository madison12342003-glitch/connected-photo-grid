#!/usr/bin/env python3
"""Rank 3x3 photo layouts using supplied visual-feature metadata.

This dependency-free prototype does not inspect image pixels. It scores the
actual touching edges when edge metadata exists, falling back to whole-photo
features when it does not.

Input JSON contains exactly nine records under "photos". Each record needs an
"id" and may include direction, shape, colors, elements/object, texture, space,
narrative, plus right_edge/left_edge/top_edge/bottom_edge dictionaries.
"""
import argparse
import itertools
import json
from typing import Dict, Iterable, List, Sequence, Tuple

DIMENSIONS = ("direction", "shape", "color", "object", "texture", "space", "narrative")
WEIGHTS = {"direction": 2.0, "shape": 1.5, "color": 1.0, "object": 1.0,
           "texture": 0.75, "space": 0.75, "narrative": 0.5}


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
    return 5.0 * len(sa & sb) / len(sa | sb)


def direction_score(a, b) -> float:
    if a is None or b is None:
        return 0.0
    diff = abs((float(a) - float(b)) % 180.0)
    diff = min(diff, 180.0 - diff)
    return 5.0 * (1.0 - diff / 90.0)


def score_edges(a: dict, b: dict, orientation: str) -> Tuple[float, Dict[str, float]]:
    if orientation == "horizontal":
        ea, eb = a.get("right_edge", {}), b.get("left_edge", {})
    else:
        ea, eb = a.get("bottom_edge", {}), b.get("top_edge", {})

    def values(name, whole_a, whole_b):
        return ea.get(name, whole_a), eb.get(name, whole_b)

    ad, bd = values("direction", a.get("direction"), b.get("direction"))
    ash, bsh = values("shape", a.get("shape"), b.get("shape"))
    ac, bc = values("colors", a.get("colors", a.get("color")), b.get("colors", b.get("color")))
    ao, bo = values("elements", a.get("elements", a.get("object")), b.get("elements", b.get("object")))
    at, bt = values("texture", a.get("texture"), b.get("texture"))
    asp, bsp = values("space", a.get("space"), b.get("space"))
    an, bn = values("narrative", a.get("narrative"), b.get("narrative"))
    details = {
        "direction": direction_score(ad, bd),
        "shape": tag_score(ash, bsh),
        "color": tag_score(ac, bc),
        "object": tag_score(ao, bo),
        "texture": tag_score(at, bt),
        "space": tag_score(asp, bsp),
        "narrative": tag_score(an, bn),
    }
    weight_sum = sum(WEIGHTS.values())
    return sum(details[k] * WEIGHTS[k] for k in DIMENSIONS) / weight_sum, details


def adjacency_pairs(layout: Sequence[str]) -> Iterable[Tuple[str, str, str]]:
    # A B C / D E F / G H I
    for row in range(3):
        for col in range(2):
            yield layout[row * 3 + col], layout[row * 3 + col + 1], "horizontal"
    for row in range(2):
        for col in range(3):
            yield layout[row * 3 + col], layout[(row + 1) * 3 + col], "vertical"


def score_all(photos: List[dict], top_k: int) -> List[dict]:
    if len(photos) != 9:
        raise ValueError(f"Expected exactly 9 photo records; got {len(photos)}")
    ids = [p["id"] for p in photos]
    if len(set(ids)) != 9:
        raise ValueError("Photo IDs must be unique")
    by_id = {p["id"]: p for p in photos}
    cache = {}

    def pair(a_id, b_id, orientation):
        key = (a_id, b_id, orientation)
        if key not in cache:
            cache[key] = score_edges(by_id[a_id], by_id[b_id], orientation)
        return cache[key]

    ranked = []
    for perm in itertools.permutations(ids):
        edge_data = []
        total = 0.0
        for a, b, orientation in adjacency_pairs(perm):
            value, details = pair(a, b, orientation)
            total += value
            edge_data.append({"from": a, "to": b, "orientation": orientation,
                              "score": round(value, 3),
                              "details": {k: round(v, 3) for k, v in details.items()}})
        ranked.append((total, perm, edge_data))
    ranked.sort(key=lambda item: item[0], reverse=True)

    results = []
    for total, perm, edge_data in ranked[:max(1, top_k)]:
        results.append({
            "layout": [list(perm[0:3]), list(perm[3:6]), list(perm[6:9])],
            "score": round(total, 3),
            "average_edge_score": round(total / 12.0, 3),
            "edges": edge_data,
        })
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank 3x3 connected-photo layouts.")
    parser.add_argument("input", help="JSON file containing exactly 9 photo feature records")
    parser.add_argument("--top", type=int, default=10, help="Number of layouts to return")
    parser.add_argument("--output", help="Optional JSON output file")
    args = parser.parse_args()
    with open(args.input, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    results = score_all(data["photos"], args.top)
    rendered = json.dumps(results, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
