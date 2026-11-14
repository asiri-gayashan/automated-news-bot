"""Render an animated pixel news post to MP4 (+ a cover PNG).

Usage:  python engine/render_video.py post.json out.mp4 [loops=3]
One loop = post["anim"]["duration"] seconds; the video repeats it `loops` times (5 s x 3 = 15 s).
Needs: playwright (chromium) + ffmpeg on PATH.
"""
import json, sys, pathlib, subprocess, tempfile, shutil
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent


def render(post_path, out, loops=3):
    post = json.loads(pathlib.Path(post_path).read_text(encoding="utf-8"))
    A = post["anim"]; fps = A.get("fps", 24); n = int(A["duration"] * fps)
    tmp = pathlib.Path(tempfile.mkdtemp())
    errors = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1080})
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.add_init_script("window.POST = " + json.dumps(post, ensure_ascii=False) + ";")
        pg.goto((HERE / "template.html").as_uri())
        pg.wait_for_function("document.title === 'ready'", timeout=30000)
        el = pg.locator("#post")
        for i in range(n):
            pg.evaluate(f"window.setT({i / fps})")
            el.screenshot(path=str(tmp / f"f{i:04d}.png"))
        lines = pg.evaluate("window.LINES")
        b.close()
    if errors:
        raise RuntimeError("template error: " + "; ".join(errors))
    out = pathlib.Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", str(loops - 1), "-framerate", str(fps),
                    "-i", str(tmp / "f%04d.png"), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-r", str(fps), "-movflags", "+faststart", str(out)], check=True)
    # cover = the most "eventful" moment: 60% through the story
    shutil.copy(tmp / f"f{int(n * 0.6):04d}.png", out.with_suffix(".cover.png"))
    shutil.rmtree(tmp)
    return lines


if __name__ == "__main__":
    loops = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    n = render(sys.argv[1], sys.argv[2], loops)
    print("headline lines:", n)
    print("saved", sys.argv[2])
