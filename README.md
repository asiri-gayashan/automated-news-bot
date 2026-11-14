# Automated News Bot — Asiri Gayashan

Daily Sinhala news posts with cute 8-bit animations, made automatically.

```
Claude (8 AM · 12 PM · 7 PM)  →  queue/<date>/<slot_slug>/post.json + caption.txt
        ↓ push
GitHub Actions: render 15 s MP4 (1080×1080) + cover  →  copied to automated-news-posts (GitHub Pages)
        ↓ waits for your approval (environment "approval")
GitHub Actions: publish to Facebook Page (video) + Instagram (Reel)
```

| Folder | What |
|---|---|
| `engine/` | `template.html` (1:1 pixel news template + animation engine), `render_video.py`, `pixelkit.py` (palette + sprites), fonts, logo |
| `engine/examples/` | Example animated post |
| `queue/` | Posts written by Claude (one folder per post) + `status.json` written by Actions |
| `scripts/` | `validate_post.py`, `render_queue.py`, `publish_meta.py` |
| `RUNBOOK.md` | Rules Claude follows for every post |

## Secrets (Settings → Secrets and variables → Actions)
| Name | What |
|---|---|
| `AMERICAN_CAPTAIN_OTF_B64` | The licensed American Captain font (base64). Kept secret — the font file is **not** in this repo. |
| `POSTS_REPO_TOKEN` | Fine-grained token with *Contents: Read and write* on `automated-news-posts` |
| `META_PAGE_ID`, `META_PAGE_TOKEN`, `IG_USER_ID` | Facebook Page + Instagram publishing (optional until set) |

## Approving posts
GitHub app → this repo → Actions → the waiting run → **Review deployments** → tick `approval` → **Approve and deploy**.

## Fonts
Gemunu Libre and Poppins are under the SIL Open Font License (see `engine/fonts/OFL-*.txt`).
American Captain is licensed to the owner and is injected at build time from a secret.
