import importlib.util
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("analyze_photo", ROOT / "scripts" / "analyze_photo.py")
analyze_photo = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analyze_photo)

def sample_result():
    return {
        "subject": "Snowy mountain and grassland", "scene_type": "landscape",
        "colors": ["white", "blue", "green"], "elements": ["mountain", "cloud", "grassland"],
        "composition": {"subject_position": "center", "negative_space": "top", "dominant_direction_degrees": 12, "shape_tags": ["ridge", "diagonal"], "crop_flexibility": "high"},
        "edge_features": {"left": ["grass"], "right": ["mountain"], "top": ["sky"], "bottom": ["grass"]},
        "narrative_role": "establishing landscape", "confidence": 0.91, "notes": []}

class AnalyzePhotoTests(unittest.TestCase):
    def test_validates_structured_response(self):
        self.assertEqual(analyze_photo.validate_result(sample_result())["subject"], "Snowy mountain and grassland")
    def test_rejects_missing_required_fields(self):
        with self.assertRaisesRegex(ValueError, "missing required fields"):
            analyze_photo.validate_result({"subject": "mountain"})
    def test_rejects_invalid_confidence(self):
        data = sample_result(); data["confidence"] = 1.5
        with self.assertRaisesRegex(ValueError, "confidence"):
            analyze_photo.validate_result(data)
    def test_rejects_missing_nested_fields(self):
        data = sample_result(); data["edge_features"] = {}
        with self.assertRaisesRegex(ValueError, "edge_features"):
            analyze_photo.validate_result(data)
    def test_missing_image_fails_before_api_call(self):
        with self.assertRaises(FileNotFoundError):
            analyze_photo.analyze_image("/not/a/real/photo.jpg", api_key="dummy")
    def test_bad_extension_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "photo.gif"; path.write_bytes(b"not an image")
            with self.assertRaisesRegex(ValueError, "Supported image extensions"):
                analyze_photo.analyze_image(str(path), api_key="dummy")

if __name__ == "__main__":
    unittest.main()
