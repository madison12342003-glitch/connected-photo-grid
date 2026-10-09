import importlib.util
import json
import pathlib
import tempfile
import unittest
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('compose_photomontage', ROOT / 'scripts' / 'compose_photomontage.py')
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)

class PhotomontageRendererTests(unittest.TestCase):
    def test_exports_full_canvas_and_nine_tiles(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp); photos = root / 'photos'; photos.mkdir()
            Image.new('RGB', (80, 80), (30, 90, 160)).save(photos / 'blue.png')
            Image.new('RGB', (80, 80), (180, 30, 40)).save(photos / 'red.png')
            plan = {'background':'#F7F8F8','layers':[
              {'image':'blue.png','scope':'canvas','x':0,'y':0,'w':1,'h':1},
              {'image':'red.png','scope':'tile','tile':'B','x':0.25,'y':0.25,'w':0.5,'h':0.5}]}
            p = root / 'plan.json'; p.write_text(json.dumps(plan), encoding='utf-8')
            out = root / 'out'; result = renderer.render(p, photos, out, tile_size=200)
            self.assertTrue(result.is_file()); self.assertEqual(len(list(out.glob('[A-I].png'))), 9)
            with Image.open(result) as im:
                self.assertEqual(im.size, (600,600))
                self.assertEqual(im.getpixel((199,100))[:3], (30,90,160))
                self.assertEqual(im.getpixel((201,100))[:3], (30,90,160))
                self.assertEqual(im.getpixel((300,100))[:3], (180,30,40))
                self.assertEqual(im.getpixel((100,300))[:3], (30,90,160))

    def test_canvas_bridge_is_continuous_across_A_B_seam_and_tile_crops(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            photos = root / 'photos'
            photos.mkdir()
            Image.new('RGB', (100, 100), (40, 120, 70)).save(photos / 'base.png')
            Image.new('RGB', (100, 100), (210, 20, 30)).save(photos / 'bridge.png')
            plan = {'background': '#F7F8F8', 'layers': [
                {'image': 'base.png', 'scope': 'canvas', 'x': 0, 'y': 0, 'w': 1, 'h': 1},
                {'image': 'bridge.png', 'scope': 'canvas', 'x': 0.285, 'y': 0.035, 'w': 0.43, 'h': 0.19, 'role': 'cross-tile-bridge'}]}
            plan_path = root / 'plan.json'
            plan_path.write_text(json.dumps(plan), encoding='utf-8')
            out = root / 'out'
            full_path = renderer.render(plan_path, photos, out, tile_size=200)
            with Image.open(full_path) as full, Image.open(out / 'A.png') as tile_a, Image.open(out / 'B.png') as tile_b:
                self.assertEqual(full.getpixel((195, 20))[:3], (210, 20, 30))
                self.assertEqual(full.getpixel((205, 20))[:3], (210, 20, 30))
                self.assertEqual(tile_a.getpixel((195, 20))[:3], full.getpixel((195, 20))[:3])
                self.assertEqual(tile_b.getpixel((5, 20))[:3], full.getpixel((205, 20))[:3])

    def test_missing_image_fails_clearly(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp); p = root / 'plan.json'
            p.write_text(json.dumps({'layers':[{'image':'missing.jpg','scope':'canvas'}]}), encoding='utf-8')
            with self.assertRaises(FileNotFoundError): renderer.render(p, root, root / 'out', tile_size=200)
if __name__ == '__main__': unittest.main()
