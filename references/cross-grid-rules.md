# Cross-Grid Connection Rules

## Two kinds of cohesion
1. Literal continuation: a line, ridge, road, river, or graphic path aligns across a boundary.
2. Visual echo: similar color, shape, texture, subject, or typography recurs in separate tiles.

Use both. Do not force all twelve adjacent pairs to create a literal seam.

## Plan on the full canvas
For any element intended to cross tiles, design it on one shared 3×3 canvas first and slice it afterward. Do not independently draw the same line in separate tiles and hope the endpoints align.

## Edge metadata
For a photo or layer, record edge features using normalized coordinates:
- element or contour name
- start and end coordinates along the edge or in the tile
- direction angle
- dominant color
- shape and texture tags
- whether it is a literal continuation or an echo
- confidence that the connection is supported by the source

Example fields may include right_edge, left_edge, top_edge, and bottom_edge. Edge-level metadata is more useful than one direction value for the whole image.

## Connection strength
Score each adjacent pair from 0 to 5:
- 0: conflicts or accidental collision
- 1: weak or incidental relation
- 2: mild echo
- 3: clear color, shape, subject, or narrative relation
- 4: strong intentional bridge
- 5: near-seamless continuation with matching geometry

A lower score can be acceptable when deliberate contrast improves rhythm. The score is a review aid, not an automatic artistic verdict.

## Cultural and photographic integrity
Never invent a real-world continuation that falsely implies two photographs depict the same physical scene. Graphic lines and colors may bridge separate scenes, but documentary content must remain truthful.

## Final adjacency review
Inspect all horizontal and vertical neighbor pairs at full size, then inspect the full grid at phone size. Fix accidental tangencies, abrupt line endings, repetitive motifs, and edges that pull attention away from the main subject.
