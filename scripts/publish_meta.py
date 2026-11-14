"""GitHub Actions step (runs only after you approve): publish rendered posts to Facebook + Instagram.

Secrets used (set them in GitHub → Settings → Secrets and variables → Actions):
  META_PAGE_ID      Facebook Page ID
  META_PAGE_TOKEN   long-lived Page access token (pages_manage_posts, instagram_content_publish, ...)
  IG_USER_ID        Instagram Business/Creator account ID linked to the Page
Optional variable: META_API_VERSION (default v23.0)

If the secrets are not set yet, this step just skips publishing.
"""
import json, os, pathlib, sys, time, urllib.request, urllib.parse, urllib.error

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGE, TOKEN, IG = (os.environ.get(k, "").strip() for k in ("META_PAGE_ID", "META_PAGE_TOKEN", "IG_USER_ID"))
VER = os.environ.get("META_API_VERSION", "").strip() or "v23.0"
G = f"https://graph.facebook.com/{VER}"
GV = f"https://graph-video.facebook.com/{VER}"


def call(url, data=None, method="POST", token=None):
    body = urllib.parse.urlencode({**(data or {}), "access_token": token or TOKEN}).encode()
    if method == "GET":
        req = urllib.request.Request(url + "?" + body.decode())
    else:
        req = urllib.request.Request(url, data=body, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{e.code}: {e.read().decode()[:400]}")


def wait_public(url, tries=20):
    for _ in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=30) as r:
                if r.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(15)
    return False


def _fb_reel(url, caption):
    v = call(f"{G}/{PAGE}/video_reels", {"upload_phase": "start"}, token=PAGE_TOKEN)
    vid = v["video_id"]
    req = urllib.request.Request(f"https://rupload.facebook.com/video-upload/{VER}/{vid}", method="POST",
                                 headers={"Authorization": f"OAuth {PAGE_TOKEN}", "file_url": url})
    with urllib.request.urlopen(req, timeout=300) as r:
        json.loads(r.read())
    call(f"{G}/{PAGE}/video_reels", {"upload_phase": "finish", "video_id": vid,
                                     "video_state": "PUBLISHED", "description": caption}, token=PAGE_TOKEN)
    return vid


def publish_facebook(st, caption):
    """Facebook Page Reel. Tries the SQUARE video first (same as Instagram); if Facebook refuses the
    square format, uses the 9:16 version; if Reels fail completely, posts the cover image as a photo."""
    for label, url in (("square", st.get("video_url")), ("9:16", st.get("reel_url"))):
        if not url:
            continue
        try:
            return f"reel-{label}:" + _fb_reel(url, caption)
        except Exception as e:
            print(f"  facebook {label} reel failed ->", str(e)[:300])
    r = call(f"{G}/{PAGE}/photos", {"url": st["cover_url"], "caption": caption}, token=PAGE_TOKEN)
    return "photo:" + r.get("post_id", r.get("id", ""))


def publish_instagram(video_url, caption):
    c = call(f"{G}/{IG}/media", {"media_type": "REELS", "video_url": video_url, "caption": caption, "share_to_feed": "true"})["id"]
    for _ in range(40):  # up to ~10 minutes of processing
        st = call(f"{G}/{c}", {"fields": "status_code"}, method="GET").get("status_code")
        if st == "FINISHED":
            break
        if st == "ERROR":
            raise RuntimeError("Instagram could not process the video")
        time.sleep(15)
    return call(f"{G}/{IG}/media_publish", {"creation_id": c})["id"]


if not (PAGE and TOKEN):
    print("Meta secrets not set yet - skipping publishing. Posts are rendered and saved in automated-news-posts.")
    sys.exit(0)

# Facebook Page posts need a *Page* token. If the secret holds a user token, ask Meta for the Page's own token.
PAGE_TOKEN = TOKEN
try:
    pt = call(f"{G}/{PAGE}", {"fields": "access_token"}, method="GET").get("access_token")
    if pt:
        PAGE_TOKEN = pt
        if pt != TOKEN:
            print("note: META_PAGE_TOKEN is a user token; using the Page token derived from it.")
except Exception as e:
    print("could not look up Page token:", str(e)[:200])

failed = False
for sf in sorted(ROOT.glob("queue/*/*/status.json")):
    st = json.loads(sf.read_text())
    if not st.get("rendered"):
        continue
    pub = st.setdefault("published", {})
    if pub.get("facebook") and (pub.get("instagram") or not IG):
        continue
    cap_f = sf.parent / "caption.txt"
    caption = cap_f.read_text(encoding="utf-8") if cap_f.exists() else ""
    if not wait_public(st["video_url"]) or (st.get("reel_url") and not wait_public(st["reel_url"])):
        print("video not reachable yet:", st["video_url"]); failed = True; continue
    for name, fn, enabled in (("facebook", lambda: publish_facebook(st, caption), True),
                              ("instagram", lambda: publish_instagram(st["video_url"], caption), bool(IG))):
        if not enabled or pub.get(name):
            continue
        try:
            pub[name] = fn()
            pub.pop(name + "_error", None)
            print(f"{sf.parent.name}: {name} OK -> {pub[name]}")
        except Exception as e:
            pub[name + "_error"] = str(e)[:400]; failed = True
            print(f"{sf.parent.name}: {name} FAILED -> {e}")
    sf.write_text(json.dumps(st, indent=1))

sys.exit(1 if failed else 0)
