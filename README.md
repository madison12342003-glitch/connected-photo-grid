# Connected Photo Grid

> An open-source AI Skill for designing a coherent 3×3 multi-layer editorial photo collage.

## Pipeline

1. **Pixel-level inventory** — `scripts/analyze_photos.py` estimates dominant colors, brightness, texture, direction, aspect ratio, and edge features locally.
2. **Cloud semantic analysis (optional)** — `scripts/analyze_photo.py` sends one selected local photo to Google's Gemini API and returns validated structured JSON for visible subject, scene, colors, elements, composition, edge features, narrative role, and confidence.
3. **Rank layouts** — combine semantic tags with photo metadata, then score the 12 horizontal/vertical neighbor relationships.
4. **Prepare tile plan** — map photo IDs to local file paths and optional title/caption text in `examples/sichuan-render-plan.json`.
5. **Render/export** — use `scripts/compose_grid.py` to export a high-resolution square PNG. The current renderer supports photo crops, warm-white gutters, a caption panel, typography, and a small red accent per tile.
6. **Review and refine** — inspect on a phone, check Chinese/Tibetan glyph support with a suitable local font, correct crops, and iterate.

## Gemini setup

Use Python 3.11+ and create an API key in [Google AI Studio](https://aistudio.google.com/apikey). The script uses the official `google-genai` SDK. The default model is `gemini-3.5-flash-lite`; model access and free quotas vary by account and can change. Check [official pricing and free-tier details](https://ai.google.dev/gemini-api/docs/pricing) before batch analysis. Free-tier requests may be subject to rate limits and Google data-use terms.

Install dependencies and set the key as an environment variable:

```bash
python -m pip install -r requirements.txt
# macOS/Linux
export GEMINI_API_KEY="your-key"
# PowerShell
$env:GEMINI_API_KEY="your-key"
```

Never commit a real key. `.env.example` is a placeholder only; `.gitignore` excludes `.env` and local photo/output folders.

Analyze one photo and save JSON:

```bash
python scripts/analyze_photo.py /path/to/photo.jpg --output output/photo-A.json
```

The photo is sent to Google's API for analysis. Do not use this for images you are not comfortable sending to a cloud service. The script never uploads your whole photo library automatically; run it only on the photos you choose.

## Gemini batch workflow

The batch script `scripts/analyze_photos_gemini.py` accepts a local image folder or the JSON emitted by `scripts/analyze_photos.py`. It analyzes images one at a time, writes merge-compatible semantic JSON, and supports `--limit` and `--pause` to help manage API quota. Records are matched by filename stem, so use unique filenames.

```bash
python scripts/analyze_photos.py input/photos --output output/pixel-features.json
python scripts/analyze_photos_gemini.py input/photos --limit 3 --output output/gemini-semantic.json
python scripts/merge_photo_analysis.py output/pixel-features.json output/gemini-semantic.json --output output/combined-features.json
python scripts/select_photos.py output/combined-features.json --output output/nine-photo-features.json
python scripts/score_layout.py output/nine-photo-features.json --top 1 --output output/layout.json
python scripts/make_render_plan.py output/nine-photo-features.json --photo-root input/photos --output output/render-plan.json
python scripts/compose_grid.py output/render-plan.json output/layout.json --photo-root input/photos --output output/sichuan-grid.png --size 3000
```

Start with a small `--limit` to check results and quota before analyzing the full collection. Selection remains heuristic; review the chosen photos and crops before publishing.

## Local layout and rendering

Keep original photos on your own computer; they do **not** need to be committed to GitHub.

```bash
# Put nine local photos in input/photos/ named A.jpg ... I.jpg
python scripts/score_layout.py examples/sichuan-features.json --top 1 --output output/layout.json
python scripts/compose_grid.py output/render-plan.json output/layout.json --photo-root input/photos --output output/sichuan-grid.png --size 3000
```

The example feature records and tile plan are demonstrations. Update metadata and image paths to match the actual photos before using them for a real trip.

## Repository map

- `SKILL.md` — main agent instructions
- `references/` — layout, photo, element, line-art, typography, color, and cross-grid rules
- `examples/sichuan-multilayer-plan.md` — Sichuan editorial collage planning guide
- `examples/sichuan-features.json` — sample metadata for the layout scorer
- `examples/sichuan-render-plan.json` — sample local-photo mapping and captions
- `scripts/analyze_photos.py` — local pixel-level feature extractor
- `scripts/analyze_photo.py` — Gemini cloud semantic analysis with structured JSON
- `scripts/describe_photos_ollama.py` — optional local vision-model semantic analysis
- `scripts/merge_photo_analysis.py` — combines semantic and pixel metadata
- `scripts/select_photos.py` — heuristic nine-photo shortlist selector
- `scripts/make_render_plan.py` — maps selected photos to an editable renderer plan
- `scripts/score_layout.py` — edge-aware layout scorer
- `scripts/compose_grid.py` — local PNG composition/export tool
- `tests/` — unit tests for analysis, scoring, and rendering
- `.github/workflows/tests.yml` — automated checks on pushes and pull requests

## Limits / next step

This adds a usable **single-photo Gemini semantic analysis → validated JSON** module alongside local pixel analysis. It does not yet batch-process the entire library, automatically decide the final nine, or create complex overlapping cutouts, line art, and cross-tile illustration. Those remain future pipeline steps. Original photographs remain local unless explicitly passed to the cloud analyzer.

## License

MIT. See [LICENSE](LICENSE).
