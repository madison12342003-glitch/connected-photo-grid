# Layout scoring prototype

This folder contains a small dependency-free prototype for ranking 3×3 layouts.

## What it does

It takes structured descriptions of nine photos and scores every possible arrangement (9! = 362,880 layouts). For each arrangement it evaluates the 12 horizontal/vertical neighbor relationships.

The current prototype scores seven dimensions:

- direction
- shape
- color
- object/element
- texture
- spatial relationship
- narrative relationship

This is deliberately **not** an image generator. It is the decision layer between image analysis and final composition.

## Usage

```bash
python scripts/score_layout.py examples/sichuan-features.json --top 10
```

The script returns the best layouts and the score of each of the 12 connections.

## Important limitation

The script does not understand pixels by itself. An upstream vision model, human annotation, or future image-analysis module must first convert each photograph into the structured feature record.

The scoring formula is a prototype and should be tuned against real examples. In particular, future versions can add edge-specific information such as:

- what enters from the right edge
- what exits from the left edge
- whether a mountain ridge actually touches the boundary
- whether a road/water line has a compatible endpoint
- whether a color exists specifically near the relevant edge

That edge-aware representation will be much closer to the real cross-grid continuity goal than comparing whole-image tags alone.
