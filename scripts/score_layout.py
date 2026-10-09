#!/usr/bin/env python3
"""Rank 3x3 photo layouts using supplied visual-feature metadata.

This dependency-free prototype does not inspect image pixels. It scores touching
edges when edge metadata exists, falling back to whole-photo features.
"""
import argparse
import heapq
import json
from itertools import permutations
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
    elif orientation == "vertical":
        ea, eb = a.get("bottom_edge", {}), b.get("top_edge", {})
    else:
        raise ValueError(f"Unknown orientation: {orientation}")

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
    """Yield the 12 touching pairs in A B C / D E F / G H I order."""
    for row in range(3):
        for col in range(2):
            yield layout[row * 3 + col], layout[row * 3 + col + 1], "horizontal"
    for row in range(2):
        for col in range(3):
            yield layout[row * 3 + col], layout[(row + 1) * 3 + col], "vertical"


def score_all(photos: List[dict], top_k: int) -> List[dict]:
    if len(photos) != 9:
        raise ValueError(f"Expected exactly 9 photo records; got {len(photos)}")
    try:
        ids = [p["id"] for p in photos]
    except (KeyError, TypeError) as exc:
        raise ValueError('Every photo record must contain an "id"') from exc
    if len(set(ids)) != 9:
        raise ValueError("Photo IDs must be unique")
    if top_k < 1:
        raise ValueError("--top must be at least 1")

    by_id = {p["id"]: p for p in photos}
    cache = {}

    def pair(a_id, b_id, orientation):
        key = (a_id, b_id, orientation)
        if key not in cache:
            cache[key] = score_edges(by_id[a_id], by_id[b_id], orientation)
        return cache[key]

    # Keep only the best K candidates in memory instead of retaining all 9!
    # layouts and their 12 edge-detail records.
    best = []
    for perm in permutations(ids):
        total = sum(pair(a, b, orientation)[0]
                    for a, b, orientation in adjacency_pairs(perm))
        entry = (total, perm)
        if len(best) < top_k:
            heapq.heappush(best, entry)
        elif total > best[0][0]:
            heapq.heapreplace(best, entry)

    ranked = sorted(best, key=lambda item: item[0], reverse=True)
    results = []
    for total, perm in ranked:
        edge_data = []
        for a, b, orientation in adjacency_pairs(perm):
            value, details = pair(a, b, orientation)
            edge_data.append({"from": a, "to": b, "orientation": orientation,
                              "score": round(value, 3),
                              "details": {k: round(v, 3) for k, v in details.items()}})
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
    if args.top < 1:
        parser.error("--top must be at least 1")
    with open(args.input, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or not isinstance(data.get("photos"), list):
        parser.error('Input JSON must contain a "photos" array')
    results = score_all(data["photos"], args.top)
    rendered = json.dumps(results, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered + "\\n")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
