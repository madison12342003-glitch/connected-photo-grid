import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "make_photomontage_plan", ROOT / "scripts" / "make_photomontage_plan.py"
)
planner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(planner)


class PhotomontagePlanTests(unittest.TestCase):
    def sample_photos(self, count=12):
        return [
            {
                "id": f"p{i}",
                "image": f"p{i}.png",
                "colors": [f"color{i % 3}"],
                "elements": [f"element{i % 4}"],
                "texture": [f"texture{i % 3}"],
                "narrative": [f"role{i}"],
            }
            for i in range(count)
        ]

    def test_plan_has_two_distinct_layers_per_tile_and_bridge(self):
        plan = planner.make_plan({"photos": self.sample_photos()}, "input/photos")
        self.assertEqual(len(plan["layers"]), 19)
        bridges = [layer for layer in plan["layers"] if layer.get("role") == "cross-tile-bridge"]
        self.assertEqual(len(bridges), 1)
        bridge = bridges[0]
        self.assertEqual(bridge["scope"], "canvas")
        self.assertIs(plan["layers"][-1], bridge)
        self.assertLess(bridge["x"], 0.5)
        self.assertGreater(bridge["x"] + bridge["w"], 0.5)
        tile_layers = [layer for layer in plan["layers"] if "tile" in layer]
        self.assertEqual({layer["tile"] for layer in tile_layers}, set(planner.TILES))
        for tile in planner.TILES:
            layers = [layer for layer in tile_layers if layer["tile"] == tile]
            self.assertEqual(len(layers), 2)
            self.assertNotEqual(layers[0]["image"], layers[1]["image"])
            self.assertLess(layers[0]["opacity"], 1)
            self.assertTrue(layers[1].get("mask"))

    def test_generated_plan_renders_full_grid_and_nine_tiles(self):
        renderer_spec = importlib.util.spec_from_file_location(
            "compose_photomontage", ROOT / "scripts" / "compose_photomontage.py"
        )
        renderer = importlib.util.module_from_spec(renderer_spec)
        renderer_spec.loader.exec_module(renderer)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            photos_dir = root / "photos"
            photos_dir.mkdir()
            photos = self.sample_photos()
            for index, photo in enumerate(photos):
                Image.new(
                    "RGB", (80, 80),
                    ((index * 31) % 256, (index * 67) % 256, (index * 97) % 256),
                ).save(photos_dir / photo["image"])
            plan = planner.make_plan({"photos": photos}, photos_dir)
            plan_path = root / "plan.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            output_dir = root / "out"
            result = renderer.render(plan_path, photos_dir, output_dir, tile_size=200)
            self.assertTrue(result.is_file())
            with Image.open(result) as image:
                self.assertEqual(image.size, (600, 600))
            self.assertEqual(len(list(output_dir.glob("[A-I].png"))), 9)

    def test_requires_nine_photos(self):
        with self.assertRaises(ValueError):
            planner.make_plan({"photos": []}, "input/photos")


if __name__ == "__main__":
    unittest.main()
