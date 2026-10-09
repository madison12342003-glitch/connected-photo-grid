import importlib.util, unittest
from pathlib import Path
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
  self.assertEqual({x["tile"] for x in plan["layers"]},set(planner.TILES))
  for tile in planner.TILES:
   ls=[x for x in plan["layers"] if x.get("tile")==tile]
   self.assertEqual(len(ls),2); self.assertNotEqual(ls[0]["image"],ls[1]["image"])
   self.assertLess(ls[0]["opacity"],1); self.assertTrue(ls[1].get("mask"))
 def test_requires_nine_photos(self):
  with self.assertRaises(ValueError): planner.make_plan({"photos":[]},"input/photos")
if __name__=="__main__": unittest.main()
