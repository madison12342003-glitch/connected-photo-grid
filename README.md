# Connected Photo Grid

> An open-source AI Skill for designing a coherent 3×3 multi-layer editorial photo collage.

## Pipeline

1. **Photo inventory and visual analysis** — record subjects, colors, direction, negative space, crop flexibility, and edge-specific features. At present this metadata is supplied manually or by an external vision model; the scorer itself does not analyze pixels.
2. **Rank layouts** — score the 12 horizontal/vertical neighbor relationships among nine selected photos.
3. **Prepare tile plan** — map photo IDs to local file paths and optional title/caption text in `examples/sichuan-render-plan.json`.
4. **Render/export** — use `scripts/compose_grid.py` to export a high-resolution square PNG. The current renderer supports photo crops, warm-white gutters, a caption panel, typography, and a small red accent per tile.
5. **Review and refine** — inspect on a phone, check Chinese/Tibetan glyph support with a suitable local font, correct crops, and iterate.

## Quick start

Keep original photos on your own computer; they do **not** need to be committed to GitHub.

```bash
python -m pip install Pillow
# Put nine local photos in input/photos/ named A.jpg ... I.jpg
python scripts/score_layout.py examples/sichuan-features.json --top 1 --output output/layout.json
python scripts/compose_grid.py examples/sichuan-render-plan.json output/layout.json --photo-root input/photos --output output/sichuan-grid.png --size 3000
```

The example feature records and tile plan are demonstrations. Before using them for a real trip, update metadata and image paths to match the actual photos. You may set a font file path in the render plan; use a font that supports the scripts used in your captions.

## What the Skill covers

- Per-tile composition and optional layer stacks
- Whole-grid palette, typography, margins, and recurring motifs
- Twelve adjacent tile relationships and full-canvas paths
- Photographic integrity and culturally grounded graphic elements

## Repository map

- `SKILL.md` — main agent instructions
- `references/` — layout, photo, element, line-art, typography, color, and cross-grid rules
- `examples/sichuan-multilayer-plan.md` — Sichuan editorial collage planning guide
- `examples/sichuan-features.json` — sample metadata for the layout scorer
- `examples/sichuan-render-plan.json` — sample local-photo mapping and captions
- `scripts/score_layout.py` — edge-aware layout scorer
- `scripts/compose_grid.py` — local PNG composition/export tool
- `tests/test_score_layout.py` — scorer tests
- `.github/workflows/tests.yml` — automated checks on pushes and pull requests

## Limits / next step

This is now a usable **metadata → ranked layout → basic PNG export** path, but it is not yet the full automated visual-analysis and art-directed multilayer pipeline. The scorer does not inspect photo pixels, and the renderer currently creates a clean editorial grid rather than arbitrary overlapping cutouts, complex line art, or cross-tile illustration. Those are the next implementation layer. Original photographs remain local, so large images need not be uploaded to the repository.

## License

MIT. See [LICENSE](LICENSE).
