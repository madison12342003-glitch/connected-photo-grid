# Layout scoring prototype

This dependency-free script ranks 3×3 arrangements from structured photo metadata. It does not inspect pixels or create the collage.

## What it does

- Requires exactly nine uniquely identified photo records.
- Evaluates all 9! (362,880) possible arrangements.
- Scores the 12 horizontal and vertical neighbor relationships.
- Reports per-edge scores and dimension details for the top layouts.

Dimensions are direction, shape, color, object/element, texture, spatial relationship, and narrative relationship.

## Usage

```bash
python scripts/score_layout.py examples/sichuan-features.json --top 10
```

## Edge-specific metadata

For better continuity, each photo may provide:
- `right_edge` and `left_edge` for horizontal neighbors
- `bottom_edge` and `top_edge` for vertical neighbors

Each edge object may contain `direction`, `shape`, `colors`, `elements`, `texture`, `space`, and `narrative`. When a field is absent, the script falls back to the corresponding whole-photo feature. Direction describes a visual orientation in degrees; it is not a compass bearing.

Example:

```json
{
  "id": "photo-01",
  "right_edge": {
    "direction": 32,
    "shape": ["mountain_ridge", "diagonal"],
    "colors": ["white", "blue"],
    "elements": ["snow_mountain"]
  }
}
```

The score is a sorting aid, not an artistic verdict. Literal continuity, visual echo, and intentional contrast must still be reviewed by a person.

## Limits

An upstream vision model or human annotator must first describe each photograph. This script does not identify subjects, inspect image pixels, crop photos, render layers, or export the final collage. The formula is a prototype and should be validated against real compositions.
