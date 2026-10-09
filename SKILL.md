---
name: connected-photo-grid
description: Design a coherent 3×3 multi-layer editorial photo collage from a collection of photographs. Select nine images, plan per-tile photo and graphic layers, build a restrained visual system, and review both literal cross-grid continuity and visual echoes.
---

# Connected Photo Grid — Multi-Layer Edition

Turn a collection of photographs into one intentional 3×3 editorial composition. Each tile may contain a stack of photographs, background, illustration, line art, typography, and graphic accents. The result must feel like one designed work, not merely nine photos in a grid.

## Core principles

1. Preserve the truth and recognizable subject of source photographs.
2. Design the whole nine-tile system and the individual tile compositions together.
3. Use a consistent background, palette, typography, and limited motif family.
4. Use both literal continuity and visual echoes; do not force every boundary to connect seamlessly.
5. Use illustrations only when they are relevant, respectful, and stylistically consistent.
6. Add meaningful text as real editable typography, not AI-generated lettering.
7. Prioritize hierarchy, breathing room, mobile readability, and a believable photographic feel.

## Workflow

### 1. Inventory every source

Analyze all accessible photos before selecting. Assign each image an ID and record subject, scene, colors, light/weather, focal point, safe crop, horizon/direction, edge features, texture, negative space, narrative value, and cultural/documentary details. Use local pixel analysis for measurable features and optional Gemini semantic analysis for scene understanding. Never claim to inspect photos that are not available in the current local workspace.

#### Optional Gemini cloud analysis

Install dependencies with `python -m pip install -r requirements.txt`, create a key in [Google AI Studio](https://aistudio.google.com/apikey), and set `GEMINI_API_KEY` in the shell environment. Run:

```bash
python scripts/analyze_photo.py /path/to/selected-photo.jpg --output output/photo-analysis.json
```

The script returns validated JSON containing `subject`, `scene_type`, `colors`, `elements`, `composition`, `edge_features`, `narrative_role`, `confidence`, and `notes`. The default model is `gemini-2.5-flash`; availability and free quota are account-dependent. A chosen image is sent to Google's cloud API, so use this only when appropriate for the image's privacy. Keep API keys out of source control; never ask the user to commit original travel photos.

### 2. Select and sequence the nine

Choose for variety, image quality, story, color, and design flexibility. Avoid nine near-duplicates. Keep a shortlist and backups. Explain exclusions briefly if asked. The center should usually anchor the story, while corners and edge tiles frame or direct the eye; these are heuristics, not rigid rules.

### 3. Analyze the visual reference

Extract transferable rules rather than copying unrelated content: grid, margins, background, photo-to-graphic ratio, layer stacks, palette, typography hierarchy, line-art style, motifs, cross-grid paths, density, and negative-space rhythm. See `references/reference-analysis.md`.

### 4. Build the nine-tile plan

Use the A–I grid:
```text
A B C
D E F
G H I
```
For every tile specify its role, primary photo/crop, optional detail, background, illustration/line art, exact text, accents/colors, neighbor connections, and layers to omit to preserve negative space.

### 5. Establish the visual system

Define background, palette, typography, line weights, photo treatments, margins, and motifs before detailed tiles. For a white social-feed context, consider warm white/off-white backgrounds, charcoal/black typography and line art, and restrained red accents while preserving natural photo colors.

### 6. Source and make graphic elements

Prioritize details extracted from the user's photos, contextually supported elements, permitted assets, then generated assets only where needed. Avoid stereotypical regional symbols without scene evidence or user approval. Treat religious and cultural imagery respectfully.

### 7. Plan connections

Review all 12 horizontal and vertical neighbor pairs. Use literal continuation, visual echoes, or deliberate contrast. Plan cross-tile artwork on one full canvas and slice afterward. Do not imply separate photos are the same continuous real-world scene.

### 8. Compose and render

Work from rough photo layout to whole-grid balance, per-tile details, illustrations/line art, verified typography, accents, and final export. Never claim to have exported a final image unless the file was actually created.

### 9. Quality gate

Check focal point, phone-size readability, realistic photos, all 12 boundaries, path alignment, varied echoes, suitable margins, correct text, culturally respectful details, clean crops, and final dimensions/order.

## References

Use relevant focused guides in `references/`: layout, photo, element, line-art, typography, color, cross-grid rules, and reference analysis.

## Output contract

Unless asked for a finished render, start with a concise design plan: photo choices, tile roles, layer stacks, palette, typography, and cross-grid relationships. Distinguish observed facts from proposals. Ask only for information essential to proceed.
