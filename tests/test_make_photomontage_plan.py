import importlib.util, unittest, tempfile, json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("make_photomontage_plan",ROOT/"scripts"/"make_photomontage_plan.py")
planner=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(planner)
class PhotomontagePlanTests(unittest.TestCase):
 def test_plan_has_two_distinct_layers_per_tile(self):
  photos=[]
  for i in range(12):
   photos.append({"id":f"p{i}","image":f"p{i}.jpg","colors":[["white","blue"],["red","black"],["gray","green"]][i%3],"elements":[["mountain"],["flag"],["road"],["yak"]][i%4],"texture":[["rock"],["fabric"],["water"]][i%3],"narrative":[f"role{i}"]})
  plan=planner.make_plan({"photos":photos},"input/photos")
  self.assertEqual(len(plan["layers"]),19)
  bridges=[x for x in plan["layers"] if x.get("role")=="cross-tile-bridge"]
  self.assertEqual(len(bridges),1)
  self.assertEqual(bridges[0]["scope"],"canvas")
  self.assertIs(plan["layers"][-1], bridges[0])
  self.assertLess(bridges[0]["x"],0.5)
  self.assertGreater(bridges[0]["x"]+bridges[0]["w"],0.5)
  self.assertEqual({x["tile"] for x in plan["layers"] if "tile" in x},set(planner.TILES))
  for tile in planner.TILES:
   ls=[x for x in plan["layers"] if x.get("tile")==tile]
   self.assertEqual(len(ls),2); self.assertNotEqual(ls[0]["image"],ls[1]["image"])
   self.assertLess(ls[0]["opacity"],1); self.assertTrue(ls[1].get("mask"))

 def test_generated_plan_renders_full_grid_and_nine_tiles(self):
  from importlib.util import spec_from_file_location, module_from_spec
  renderer_spec=spec_from_file_location("compose_photomontage",ROOT/"scripts"/"compose_photomontage.py")
  renderer=module_from_spec(renderer_spec); renderer_spec.loader.exec_module(renderer)
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp); photos_dir=root/"photos"; photos_dir.mkdir()
   photos=[]
   for i in range(12):
    name=f"p{i}.png"
    Image.new("RGB",(80,80),((i*31)%256,(i*67)%256,(i*97)%256)).save(photos_dir/name)
    photos.append({"id":f"p{i}","image":name,"colors":[f"color{i%3}"],"elements":[f"element{i%4}"],"texture":[f"texture{i%3}"],"narrative":[f"role{i}"]})
   plan=planner.make_plan({"photos":photos},photos_dir)
   plan_path=root/"plan.json"; plan_path.write_text(json.dumps(plan),encoding="utf-8")
   out=root/"out"
   result=renderer.render(plan_path,photos_dir,out,tile_size=200)
   self.assertTrue(result.is_file())
   with Image.open(result) as im: self.assertEqual(im.size,(600,600))
   self.assertEqual(len(list(out.glob("[A-I].png"))),9)
\n def test_requires_nine_photos(self):
  with self.assertRaises(ValueError): planner.make_plan({"photos":[]},"input/photos")
if __name__=="__main__": unittest.main()
