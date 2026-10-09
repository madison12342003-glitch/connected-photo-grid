#!/usr/bin/env python3
"""Analyze one local photo with Google's Gemini API and emit validated JSON.

API key is read from GEMINI_API_KEY; never place it in source files or CLI args.
"""
import argparse
import json
import os
from pathlib import Path
from typing import Any

PHOTO_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "subject": {"type": "STRING"},
        "scene_type": {"type": "STRING"},
        "colors": {"type": "ARRAY", "items": {"type": "STRING"}},
        "elements": {"type": "ARRAY", "items": {"type": "STRING"}},
        "composition": {
            "type": "OBJECT",
            "properties": {
                "subject_position": {"type": "STRING", "enum": ["left", "center", "right", "top", "bottom", "distributed", "unclear"]},
                "negative_space": {"type": "STRING", "enum": ["left", "center", "right", "top", "bottom", "minimal", "distributed", "unclear"]},
                "dominant_direction_degrees": {"type": "INTEGER"},
                "shape_tags": {"type": "ARRAY", "items": {"type": "STRING"}},
                "crop_flexibility": {"type": "STRING", "enum": ["high", "medium", "low"]},
            },
            "required": ["subject_position", "negative_space", "dominant_direction_degrees", "shape_tags", "crop_flexibility"],
        },
        "edge_features": {
            "type": "OBJECT",
            "properties": {
                "left": {"type": "ARRAY", "items": {"type": "STRING"}},
                "right": {"type": "ARRAY", "items": {"type": "STRING"}},
                "top": {"type": "ARRAY", "items": {"type": "STRING"}},
                "bottom": {"type": "ARRAY", "items": {"type": "STRING"}},
            },
            "required": ["left", "right", "top", "bottom"],
        },
        "narrative_role": {"type": "STRING"},
        "confidence": {"type": "NUMBER"},
        "notes": {"type": "ARRAY", "items": {"type": "STRING"}},
    },
    "required": ["subject", "scene_type", "colors", "elements", "composition", "edge_features", "narrative_role", "confidence", "notes"],
}

PROMPT = """Analyze this photograph for a travel photo-collage layout. Return only data matching the supplied JSON schema.
Describe visible evidence only; do not infer a person's identity or invent objects. Keep subject concise.
Colors should be plain color names. Elements should be visible objects/scene features, not stereotypes.
For composition, estimate the main visual direction in degrees modulo 180 (0 horizontal, 90 vertical).
Edge features describe what visually touches or dominates each edge, to help decide neighboring tiles.
Negative space is the clearest low-detail area for type. Crop flexibility estimates whether a square crop can preserve the main subject.
Narrative role should be a short editorial role such as establishing landscape, cultural detail, movement, transition, or closing image.
Use confidence from 0 to 1. If uncertain, say so in notes."""


def validate_result(data: Any) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Model response must be a JSON object")
    required = PHOTO_SCHEMA["required"]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError("Model response is missing required fields: " + ", ".join(missing))
    if not isinstance(data["colors"], list) or not isinstance(data["elements"], list):
        raise ValueError("colors and elements must be arrays")
    confidence = data["confidence"]
    if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        raise ValueError("confidence must be between 0 and 1")
    nested_fields = {
        "composition": ["subject_position", "negative_space", "dominant_direction_degrees", "shape_tags", "crop_flexibility"],
        "edge_features": ["left", "right", "top", "bottom"],
    }
    for group, fields in nested_fields.items():
        if not isinstance(data.get(group), dict) or any(field not in data[group] for field in fields):
            raise ValueError(f"{group} is missing required fields")
    return data


def analyze_image(image_path: str, model: str = "gemini-3.5-flash-lite", api_key: str | None = None, client=None) -> dict:
    path = Path(image_path)
    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if client is None and not key:
        raise RuntimeError("GEMINI_API_KEY is not set. Create a key in Google AI Studio and set it as an environment variable.")
    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:
        raise RuntimeError("Install the official SDK with: python -m pip install -r requirements.txt") from exc

    if client is None:
        client = genai.Client(api_key=key)
    suffix = path.suffix.lower()
    mime_types = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
    if suffix not in mime_types:
        raise ValueError("Supported image extensions: .jpg, .jpeg, .png, .webp")
    image_part = types.Part.from_bytes(data=path.read_bytes(), mime_type=mime_types[suffix])
    response = client.models.generate_content(
        model=model,
        contents=[PROMPT, image_part],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=PHOTO_SCHEMA,
            temperature=0.1,
        ),
    )
    text = getattr(response, "text", None)
    if not text:
        raise ValueError("Gemini returned an empty response")
    try:
        result = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Gemini response was not valid JSON") from exc
    return validate_result(result)


def main():
    parser = argparse.ArgumentParser(description="Analyze a local photo with Gemini and save structured JSON.")
    parser.add_argument("image", help="Local image path; the image is sent to Gemini for analysis")
    parser.add_argument("--model", default=os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite"))
    parser.add_argument("--output", help="JSON output path; defaults to stdout")
    args = parser.parse_args()
    result = analyze_image(args.image, model=args.model)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(f"Saved analysis: {output}")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
