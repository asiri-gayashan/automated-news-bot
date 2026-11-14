"""GitHub Actions step: render every queued post that has not been rendered yet.

queue/<YYYY-MM-DD>/<HHMM_slug>/post.json   (written by Claude)
queue/<YYYY-MM-DD>/<HHMM_slug>/caption.txt (written by Claude)
queue/<YYYY-MM-DD>/<HHMM_slug>/status.json (written by the workflow)

Rendered media go to  out/posts/<YYYY-MM-DD>/<HHMM_slug>.mp4 / .cover.png / .txt
and are later copied into the public automated-news-posts repo (served by GitHub Pages).
"""
import json, os, pathlib, sys, datetime, shutil, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))
from render_video import render  # noqa: E402

PAGES = os.environ.get("PAGES_BASE", "https://asiri-gayashan.github.io/automated-news-posts").rstrip("/")
OUT = ROOT / "out" / "posts"
summary = []
new = 0
rendered_ids = []

for post in sorted(ROOT.glob("queue/*/*/post.json")):
    d = post.parent
    status_f = d / "status.json"
    status = json.loads(status_f.read_text()) if status_f.exists() else {}
    if status.get("rendered"):
        continue
    day, slug = d.parent.name, d.name
    mp4 = OUT / day / f"{slug}.mp4"
    try:
        lines = render(post, mp4, loops=3)
    except Exception as e:  # keep going with other posts
        status.update(rendered=False, error=str(e)[:500])
        status_f.write_text(json.dumps(status, indent=1))
        summary.append(f"### ❌ {day}/{slug}\nRender failed: `{str(e)[:300]}`\n")
        continue
    # 9:16 version (1080x1920) for Facebook Reels and TikTok: the square post centred on the page colour
    reel = mp4.with_suffix(".reel.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "pad=1080:1920:0:420:color=0xFDFDFB", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(reel)], check=True)
    cap = d / "caption.txt"
    if cap.exists():
        shutil.copy(cap, OUT / day / f"{slug}.txt")
    base = f"{PAGES}/posts/{day}/{slug}"
    status.update(rendered=True, lines=lines, rendered_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  video_url=base + ".mp4", reel_url=base + ".reel.mp4", cover_url=base + ".cover.png",
                  published=status.get("published", {}))
    status_f.write_text(json.dumps(status, indent=1))
    warn = "" if lines == 3 else f"\n> ⚠️ Headline is {lines} lines (should be 3) — check before approving.\n"
    caption = cap.read_text(encoding="utf-8") if cap.exists() else "(no caption)"
    summary.append(f"### ✅ {day}/{slug}\n![cover]({base}.cover.png)\n\n[▶ video]({base}.mp4) · [▶ 9:16 for TikTok]({base}.reel.mp4){warn}\n\n```\n{caption}\n```\n")
    new += 1
    rendered_ids.append(f"{day}/{slug}")

if os.environ.get("GITHUB_STEP_SUMMARY"):
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
        f.write("## New posts waiting for approval\n\n" + ("\n".join(summary) or "Nothing new.") +
                "\n\n_Images can take ~1 minute to appear while GitHub Pages updates._\n")
if os.environ.get("GITHUB_OUTPUT"):
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write(f"new={new}\n")
        f.write("posts=" + ",".join(rendered_ids) + "\n")
print("rendered", new, "post(s)")
