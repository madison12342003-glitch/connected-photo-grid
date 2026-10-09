import importlib.util
import pathlib
import tempfile
import unittest

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("analyze_photos", ROOT / "scripts" / "analyze_photos.py")
analyze_photos = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analyze_photos)


class AnalyzePhotosTests(unittest.TestCase):
    def test_extracts_layout_features_from_local_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "sample.jpg"
            Image.new("RGB", (120, 80), (40, 120, 200)).save(path)
            result = analyze_photos.analyze_image(path)
            self.assertEqual(result["id"], "sample")
            self.assertEqual(result["width"], 120)
            self.assertTrue(result["colors"])
            self.assertIn("right_edge", result)
            self.assertIn("direction", result["right_edge"])


if __name__ == "__main__":
    unittest.main()
