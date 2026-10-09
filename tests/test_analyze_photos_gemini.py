import pathlib
import tempfile
import unittest
import sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from analyze_photos_gemini import find_images

class BatchInputTests(unittest.TestCase):
    def test_discovers_supported_images(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "b.jpg").write_bytes(b"x")
            (root / "a.png").write_bytes(b"x")
            (root / "skip.txt").write_text("x")
            self.assertEqual([p.name for p in find_images(root, False)], ["a.png", "b.jpg"])

if __name__ == "__main__":
    unittest.main()
