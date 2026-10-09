import importlib.util
import json
import pathlib
import tempfile
import unittest

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("compose_grid", ROOT / "scripts" / "compose_grid.py")
compose_grid = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(compose_grid)


class ComposeGridTests(unittest.TestCase):
    def test_renders_nine_local_photos_to_square_png(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            photos = root / "photos"
            photos.mkdir()
            ids = list("ABCDEFGHI")
            for index, photo_id in enumerate(ids):
                Image.new("RGB", (120, 80), (index * 20, 100, 180)).save(photos / f"{photo_id}.jpg")
            layout_path = root / "layout.json"
            layout_path.write_text(json.dumps([{"layout": [ids[:3], ids[3:6], ids[6:]]}]), encoding="utf-8")
            plan_path = root / "plan.json"
            plan_path.write_text(json.dumps({"tiles": {key: {"image": f"{key}.jpg", "title": key} for key in ids}}), encoding="utf-8")
            output = root / "output.png"
            compose_grid.render(plan_path, layout_path, output, photos, size=600)
            with Image.open(output) as result:
                self.assertEqual(result.size, (600, 600))
                self.assertEqual(result.format, "PNG")


if __name__ == "__main__":
    unittest.main()
