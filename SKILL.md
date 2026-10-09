---
name: connected-photo-grid
description: Design a coherent 3×3 multi-layer editorial photo collage from a collection of photographs. Select nine images, plan per-tile photo and graphic layers, build a restrained visual system, and review both literal cross-grid continuity and visual echoes.
---

# Connected Photo Grid — Multi-Layer Edition

Turn a collection of photographs into one intentional 3×3 editorial composition. Each tile may contain a stack of photographs, background, illustration, line art, typography, and graphic accents. The result must feel like one designed work, not merely nine photos in a grid.

## Core principles

1. Preserve the truth and recognizable subject of source photographs.
2. Design the whole nine-tile system and individual tile compositions together.
3. Use a consistent background, palette, typography, and limited motif family.
4. Use both literal continuity and visual echoes; do not force every boundary to connect.
5. Use relevant, respectful illustrations and real editable typography.
6. Prioritize hierarchy, phone-size readability, and believable photographic texture.
7. A tile is a photomontage, not a single photo card: use visibly overlapping and partly occluding photo layers where suitable.
8. Plan selected shared photo, text, and line-art layers on one full 3×3 canvas, then slice into nine exports so they align exactly.
9. Keep color alive but restrained: clean near-white, black, and red are the design palette; preserve muted natural colors in the source photos.

## Workflow

### 1. Inventory every source
Analyze all accessible photos before selecting. Assign each image an ID and record subject, scene, colors, light/weather, focal point, safe crop, horizon/direction, edge features, texture, negative space, narrative value, and cultural/documentary details. Use local pixel analysis for measurable features and optional Gemini semantic analysis for scene understanding. Never claim to inspect photos unavailable in the current local workspace.

### Optional Gemini cloud analysis
Install dependencies with `python -m pip install -r requirements.txt`, create a key in [Google AI Studio](https://aistudio.google.com/apikey), and set `GEMINI_API_KEY`. Run:

```bash
python scripts/analyze_photo.py /path/to/selected-photo.jpg --output output/photo-analysis.json
```

The script returns validated JSON. The default model is `gemini-2.5-flash-lite`; availability and free quota depend on the account. Images sent for analysis go to Google's cloud API. Keep API keys out of source control and never ask the user to commit original photos.

### 2. Select and sequence the nine
Choose for variety, image quality, story, color, and design flexibility. Avoid near-duplicates. The center should be a visually substantive anchor, not automatically a blank title panel.

### 3. Analyze the visual reference
Extract transferable rules: grid, margins, background, photo-to-graphic ratio, layer stacks, palette, typography hierarchy, line-art style, motifs, cross-grid paths, density, and negative-space rhythm. See `references/reference-analysis.md` and `references/overlapping-photomontage.md`.

### 4. Build the nine-tile plan
Use the A–I grid:
```text
A B C
D E F
G H I
```
For every tile specify its role, primary photo/crop, secondary photo/detail layer, background, illustration/line art, exact text, accents/colors, neighbor connections, and layers to omit. Vary the photo combinations; do not repeat the same base photo across a row by default.

### 5. Establish the visual system
Use clean neutral/cool near-white matched to pale sky, snow, mist, or grey-white source-photo edges; black/ink; and restrained red accents. Avoid yellowed paper, beige vintage textures, oversaturated travel-poster color, and heavy global grayscale. Preserve subdued natural colors. Reduce saturation/contrast selectively on support or ghost layers, not uniformly across all photos.

### 6. Source graphic elements
Prioritize details extracted from the user's photos, then contextually supported elements. Suitable line art may include Gesang flowers, yak contours, mountain ridges, roads, monastery/stupa silhouettes, and prayer-flag cords when relevant. Vary motifs. Tibetan script must be verified and rendered with a font that supports its glyphs; keep it restrained and varied rather than repeating large ornamental text in every tile. Chinese is optional secondary text. Treat religious and cultural imagery respectfully.

### 7. Plan connections
Review all 12 horizontal and vertical neighbor pairs. Use literal continuation, visual echoes, or deliberate contrast. For strong connections, place a shared photo, Tibetan text line, flower drawing, mountain contour, road, or red mark once on the full 3×3 canvas and slice afterward. A shared photo can span two or more tiles so its visible portions align naturally. Do not independently scale a shared layer per tile. Do not imply different photos show the same physical scene unless using an actual shared image layer.

### 8. Compose and render
Work from whole-grid photo layout to per-tile photomontage, tonal treatments, illustrations/line art, verified typography, accents, and export. Each tile may combine multiple distinct source photos. Make overlap visible through z-order, occlusion, irregular masks, and selective opacity/tone adjustments. Avoid tidy rows of intact photo rectangles. Match edge treatment to the photo: avoid repeated harsh white brush borders. Keep photo coverage generous and gutters narrow. Plan canvas-wide shared layers before slicing.

### 9. Quality gate
Check focal points, phone-size readability, recognizable but restrained photo color, clean/cool near-white background, overlap/occlusion, tile diversity, all 12 boundaries, exact shared-layer alignment, varied motifs, verified sparse Tibetan typography, center-tile substance, clean crops, cultural respect, and final dimensions/order.

## References
Use the focused guides in `references/`, including layout, photo, element, line-art, typography, color, cross-grid rules, reference analysis, and overlapping photomontage direction.

## Output contract
Unless asked for a finished render, start with a concise design plan: photo choices, tile roles, layer stacks, palette, typography, and cross-grid relationships. Distinguish observed facts from proposals. Ask only for essential information.
