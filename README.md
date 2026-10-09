# Connected Photo Grid

> An open-source AI Skill for designing a coherent 3×3 multi-layer editorial photo collage.

## What is this?

**Connected Photo Grid** helps an AI agent turn a collection of photographs into one designed composition. Each tile can contain multiple layers—photography, background, secondary details, illustration, line art, typography, and graphic accents—while the nine tiles share a consistent visual system.

It goes beyond a conventional nine-photo grid. The design combines:
- **per-tile composition**: each tile has its own hierarchy and optional layer stack
- **whole-grid cohesion**: consistent palette, typography, margins, and recurring motifs
- **cross-grid relationships**: literal continuity where appropriate, plus visual echoes between tiles
- **photographic integrity**: real source images remain recognizable and are not casually transformed into synthetic scenes

## Workflow

1. Inventory and analyze all accessible source photos.
2. Select nine varied images based on quality, story, color, and crop flexibility.
3. Analyze the visual reference for transferable design rules.
4. Map the role and layer stack of each tile.
5. Define the palette, typography, background, and motif family.
6. Source or create individual illustration and line-art assets as needed.
7. Plan all 12 neighbor relationships and any full-canvas cross-tile paths.
8. Render a proof, inspect it at phone size, and revise.
9. Verify text, cultural context, cropping, alignment, and export.

## Repository map

- `SKILL.md` — main agent instructions
- `references/layout-system.md` — tile roles and multi-layer layout
- `references/photo-layer.md` — photo selection and realism
- `references/element-layer.md` — illustration sources and asset metadata
- `references/line-art-layer.md` — line-art style and continuity
- `references/typography-layer.md` — text accuracy and hierarchy
- `references/color-system.md` — palette and distribution
- `references/cross-grid-rules.md` — adjacency and full-canvas paths
- `references/reference-analysis.md` — how to extract rules from a visual reference
- `examples/sichuan-multilayer-plan.md` — example planning guide for Western Sichuan travel photos
- `scripts/score_layout.py` — lightweight edge-aware layout-scoring prototype\n- `tests/test_score_layout.py` — unit tests for scoring behavior and input validation\n- `.github/workflows/tests.yml` — runs unit tests and a CLI smoke test on pushes and pull requests

## Western Sichuan example

The first example uses a restrained warm-white, black, and red graphic system while retaining natural colors in photographs of mountains, roads, prayer flags, architecture, and flowers. Regional motifs are optional and should be grounded in the actual source material; do not add symbols just because they are stereotypically associated with a place.

## Limits

The scoring script ranks layouts from structured metadata; it does not inspect image pixels or replace visual judgment. Final text accuracy, cultural context, and image quality require review. A Skill supplies reusable instructions and tools; it does not guarantee that every host application can execute image editing automatically.

## License

MIT. See [LICENSE](LICENSE).

## Status

Multi-layer design system in progress. The repository includes composition references, a planning example, a layout-scoring prototype, unit tests, and a GitHub Actions test workflow. The scorer still depends on manually or externally generated metadata; automated pixel analysis and a complete layered rendering/export pipeline remain separate implementation tasks. Check the Actions tab for the first CI run after the workflow is triggered.
