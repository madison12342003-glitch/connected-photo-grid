#!/usr/bin/env python3
"""Use a local Ollama vision model to describe photos and extract semantic tags.

No hosted API key is required. Install Ollama separately and pull a vision-capable
model first, for example: ollama pull gemma3:4b
"""
import argparse
import base64
import json
import re
import urllib.error
import urllib.request
from pathlib import Path

PROMPT = """Analyze this travel photograph for a photo-collage layout. Return ONLY valid JSON with:
{
  "caption": "one concise factual sentence describing visible content",
  "objects": ["specific visible objects, max 8"],
  "scene": ["landscape", "architecture", "people", "road", "flowers", "water", "animals", "prayer_flags", etc., only when visible],
  "mood": ["quiet", "dramatic", "festive", "serene", "dynamic", etc., max 3],
  "composition": {"subject_position": "left|center|right|distributed|unclear",
                  "negative_space": "left|center|right|top|bottom|little|unclear",
                  "foreground": "short description or empty string",
                  "background": "short description or empty string"},
  "text_visible": ["readable text only, otherwise empty"]
}
Do not infer cultural identity or location unless unmistakably visible. Do not invent objects.
"""


def ollama_describe(path, model, endpoint, timeout):
    raw = Path(path).read_bytes()
    payload = {
        "model": model,
        "stream": False,
        "format": "json",
        "messages": [{
            "role": "user",
            "content": PROMPT,
            "images": [base64.b64encode(raw).decode("ascii")],
        }],
        "options": {"temperature": 0},
    }
    request = urllib.request.Request(
        endpoint.rstrip("/") + "/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Cannot reach Ollama at {endpoint}. Start Ollama and pull the selected vision model first. Details: {exc}"
        ) from exc
    message = body.get("message", {}).get("content", "")
    try:
        return json.loads(message)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", message, flags=re.S)
        if not match:
            raise ValueError(f"Model did not return JSON for {path.name}")
        return json.loads(match.group(0))


def main():
    parser = argparse.ArgumentParser(description="Describe local photos using a free local Ollama vision model.")
    parser.add_argument("photo_dir", help="Folder of photos")
    parser.add_argument("--output", default="output/semantic-analysis.json")
    parser.add_argument("--model", default="gemma3:4b")
    parser.add_argument("--endpoint", default="http://localhost:11434")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--recursive", action="store_true")
    args = parser.parse_args()
    root = Path(args.photo_dir)
    extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    paths = sorted(p for p in (root.rglob("*") if args.recursive else root.iterdir())
                   if p.is_file() and p.suffix.lower() in extensions)
    if not paths:
        parser.error(f"No supported images found in {root}")
    results = []
    for index, path in enumerate(paths, 1):
        print(f"[{index}/{len(paths)}] Analyzing {path.name} ...")
        try:
            analysis = ollama_describe(path, args.model, args.endpoint, args.timeout)
            results.append({"id": path.stem, "image": str(path), **analysis})
        except Exception as exc:
            print(f"  Warning: skipped {path.name}: {exc}")
    if not results:
        raise SystemExit("No photos were successfully analyzed.")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"photos": results}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Analyzed {len(results)}/{len(paths)} photos -> {output}")


if __name__ == "__main__":
    main()
