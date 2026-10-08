# Connected Photo Grid

> An open-source AI Skill for turning a collection of photographs into one coherent 3×3 connected photo composition.

## What is this?

**Connected Photo Grid** is an AI-agent Skill for creating photographic 3×3 grids where the nine images are designed to read as **one visual composition**, rather than nine unrelated photo cards.

The key idea is **cross-grid visual continuity**:

- a mountain ridge can continue into the neighboring image
- a road can visually lead into the next tile
- a river can flow across a boundary
- a prayer flag can echo or continue into another frame
- colors, textures, shapes, clouds, architecture, and visual direction can connect adjacent photographs

The Skill is designed to work with a collection of photographs, select the strongest nine, analyze their relationships, and build a coherent 3×3 composition.

## Core workflow

1. Analyze all input photographs.
2. Select the strongest nine rather than simply taking the first nine.
3. Build a visual connection graph for the 3×3 layout.
4. Evaluate the 12 main neighboring relationships.
5. Assign incoming and outgoing visual anchors to each tile.
6. Compose the nine images as one visual system.
7. Preserve photographic realism unless the user explicitly requests stylization.
8. Run a final quality check and rearrange weak connections when necessary.

## Why this is different from a normal collage

A normal collage asks:

> "How should I arrange nine nice pictures?"

Connected Photo Grid asks:

> "How can these nine photographs become one image when viewed together?"

That difference is the central design principle of this Skill.

## Example use cases

- travel photography
- landscape photography
- city photography
- architectural photography
- cultural documentation
- portrait series
- editorial photo stories

The first reference case for this project is **Western Sichuan travel photography**, but the core Skill is intentionally location-independent.

## Repository structure

```text
connected-photo-grid/
├── SKILL.md
├── README.md
├── LICENSE
├── agents/
├── references/
└── examples/
```

## License

MIT License. See [LICENSE](LICENSE).

## Status

Early open-source version: **v0.1.0**

The Skill is intentionally focused on composition logic first. Future versions may add automated image analysis, scoring, layout optimization, and tool-specific adapters.
