"""Check a queued post before committing it (run by Claude inside the scheduled task).

Usage: python scripts/validate_post.py queue/2026-11-14/1900_first-bug
- checks required fields, sprite widths and palette letters
- loads the template, plays the animation at several moments, and reports headline line count
  (American Captain is a GitHub secret, so here the browser uses a fallback font: line count is approximate)
- writes preview.png (mid-story frame) next to post.json so you can look at it
"""
import json, sys, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
d = pathlib.Path(sys.argv[1]).resolve()
post = json.loads((d / "post.json").read_text(encoding="utf-8"))
problems = []

for k in ("tag", "date", "headline", "footerLeft", "footerRight", "pixel", "anim"):
    if k not in post: problems.append(f"missing field: {k}")
if not (d / "caption.txt").exists(): problems.append("missing caption.txt")
if post.get("headline", "").count("*") % 2: problems.append("unbalanced *highlight* markers in headline")
pal = set(post.get("pixel", {}).get("palette", {}).keys()) | {".", " "}


def check_rows(rows, where):
    if len(set(map(len, rows))) > 1: problems.append(f"{where}: rows have different widths")
    bad = {c for r in rows for c in r} - pal
    if bad: problems.append(f"{where}: unknown palette letters {sorted(bad)}")


for i, L in enumerate(post.get("pixel", {}).get("layers", [])):
    if L.get("type") == "sprite": check_rows(L["rows"], f"layer {i}")
for i, A in enumerate(post.get("anim", {}).get("actors", [])):
    for fr in (A.get("frames") or ([A["rows"]] if "rows" in A else [])): check_rows(fr, f"actor {i}")
    for _, frs in A.get("swap", []):
        for fr in frs: check_rows(fr, f"actor {i} swap")

errors = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1080})
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.add_init_script("window.POST = " + json.dumps(post, ensure_ascii=False) + ";")
    pg.goto((ROOT / "engine" / "template.html").as_uri())
    pg.wait_for_function("document.title === 'ready'", timeout=30000)
    dur = post["anim"]["duration"]
    for t in (0, dur * .25, dur * .5, dur * .75, dur - .05):
        pg.evaluate(f"window.setT({t})")
    pg.evaluate(f"window.setT({dur * .6})")
    pg.locator("#post").screenshot(path=str(d / "preview.png"))
    lines = pg.evaluate("window.LINES"); b.close()
problems += [f"template error: {e}" for e in errors]
print("approx headline lines:", lines, "(target 3)")
print("preview:", d / "preview.png")
if problems:
    print("PROBLEMS:"); [print(" -", x) for x in problems]; sys.exit(1)
print("OK")
