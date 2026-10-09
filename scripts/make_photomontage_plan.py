#!/usr/bin/env python3
"""Create a first-pass overlapping 3x3 photo-layer plan from local image metadata."""
import argparse, json
from pathlib import Path
TILES = ["A","B","C","D","E","F","G","H","I"]
BG = "#F7F8F8"
MASKS = [
 [[0,.08],[.12,0],[.93,.04],[1,.22],[.92,.96],[.08,1],[0,.78]],
 [[.05,0],[.96,.08],[1,.85],[.82,1],[0,.91],[.08,.18]],
 [[0,.16],[.22,0],[1,.10],[.94,.92],[.12,1]]
]
def overlap_score(a,b):
 ac,bc=set(a.get("colors",[])),set(b.get("colors",[]))
 cs=len(ac&bc)/max(1,len(ac|bc))
 ae,be=set(a.get("elements",[])),set(b.get("elements",[]))
 ed=1-len(ae&be)/max(1,len(ae|be)) if ae or be else .25
 at,bt=set(a.get("texture",[])),set(b.get("texture",[]))
 td=1-len(at&bt)/max(1,len(at|bt)) if at or bt else .25
 return .45*cs+.35*ed+.20*td
def choose_heroes(photos):
 if len(photos)<9: raise ValueError(f"Need at least 9 photos; found {len(photos)}")
 pool=list(photos)
 first=max(pool,key=lambda p:(len(p.get("elements",[]))+len(p.get("narrative",[])),str(p.get("id",""))))
 chosen=[first]; pool.remove(first)
 while len(chosen)<9:
  p=max(pool,key=lambda p:(min(overlap_score(p,s) for s in chosen),len(p.get("elements",[])),str(p.get("id",""))))
  chosen.append(p); pool.remove(p)
 return chosen
def make_plan(data,photo_root):
 photos=data.get("photos") if isinstance(data,dict) else None
 if not isinstance(photos,list) or len(photos)<9: raise ValueError('Input JSON must contain a "photos" array with at least 9 records.')
 valid=[p for p in photos if p.get("image")]
 if len(valid)<9: raise ValueError("At least nine photo records need an 'image' path.")
 heroes=choose_heroes(valid); used={p["image"] for p in heroes}
 secondary_pool=[p for p in valid if p.get("image") not in used] or list(valid)
 layers=[]
 for i,tile in enumerate(TILES):
  hero=heroes[i]
  candidates=[p for p in secondary_pool if p.get("image")!=hero.get("image")]
  secondary=max(candidates,key=lambda p:(overlap_score(hero,p),str(p.get("id","")))) if candidates else valid[(i+1)%len(valid)]
  layers.append({"image":secondary["image"],"scope":"tile","tile":tile,"x":0,"y":0,"w":1,"h":1,
   "saturation":.58,"contrast":.92,"opacity":.48,"role":"ghost-underlay","source_id":secondary.get("id","")})
  layers.append({"image":hero["image"],"scope":"tile","tile":tile,"x":.045 if i%2==0 else .10,
   "y":.07 if i%3 else .12,"w":.90 if i%2==0 else .84,"h":.82 if i%3 else .78,
   "saturation":.92,"contrast":1.03,"opacity":1,"mask":MASKS[i%len(MASKS)],"feather":2,
   "role":"hero","source_id":hero.get("id","")})
 return {"background":BG,"palette":{"background":BG,"ink":"#17191B","accent":"#B52B35"},
  "notes":["First-pass automatic plan; review crops and layer order before export.",
  "Each tile has a distinct hero and a different partially visible underlay.",
  "Canvas-wide photo/text/line-art bridge layers may be added after reviewing the whole grid.",
  "No Tibetan text is generated automatically; only use verified text and a font with Tibetan support."],
  "source_photo_root":str(photo_root),"layers":layers}
def main():
 p=argparse.ArgumentParser(description=__doc__); p.add_argument("features"); p.add_argument("--photo-root",default="input/photos"); p.add_argument("--output",default="output/photomontage-plan.json"); a=p.parse_args()
 data=json.loads(Path(a.features).read_text(encoding="utf-8")); plan=make_plan(data,a.photo_root)
 out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(f"Wrote {len(plan['layers'])} photo layers for nine tiles -> {out}")
 print("Review the JSON before rendering; automatic selection is a first draft.")
if __name__=="__main__": main()
