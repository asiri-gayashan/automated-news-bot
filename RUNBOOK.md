# RUNBOOK — making one news post (for the scheduled Claude runs)

Page: **Asiri Gayashan** (Sinhala tech & news page). Each run makes **exactly one** post and commits it to `queue/`.
**Never push a second post in the same run.** If you change your mind after pushing, stop and tell Asiri instead (he can reject it in GitHub).
GitHub Actions then renders the video, waits for Asiri's approval, and publishes to Facebook + Instagram.

## 0. Set-up inside the run
```bash
git clone --depth 1 https://github.com/asiri-gayashan/automated-news-bot && cd automated-news-bot
pip install -q --break-system-packages playwright 2>/dev/null; python -m playwright install chromium >/dev/null 2>&1 || true
```
Today's date and time: use the Asia/Colombo time zone. Slot = `0800`, `1200` or `1900` (the run's prompt says which).

## 1. Pick the topic (by slot)
| Slot | Preferred topics (pick the strongest story) |
|---|---|
| 0800 | Tech · Geek / science · Global news |
| 1200 | Game releases · Movie releases · Interesting facts |
| 1900 | Global news · Politics · Tech |

**Avoid repeats:** list `queue/` for the last 14 days and skip any story (or topic angle) already covered.

## 2. Research rules
- News must be **recent** (last 48 h) or an **upcoming release within 7 days**. Interesting facts may be timeless but must be well documented.
- Confirm the key facts with **at least 2 independent, reputable sources**. Prefer original sources (company blogs, official sites, Reuters/AP/BBC, etc.).
- **Skip:** rumours, leaks, personal scandals or allegations about named people, graphic tragedies, medical advice.
- **Politics:** strictly factual and neutral. No opinions, no loaded words, no predictions, report what happened and who said what. Give each side equal treatment.
- Never copy article text. Write everything in your own words.

## 3. Write the text
**Headline** (`headline` field) — formal, professional Sinhala news style, **exactly 3 lines** when rendered (≈ 85–120 characters).
- Brand names, products, places in **English CAPS**.
- Wrap 3–5 key words/phrases in `*stars*` → shown in clay orange. Usually: the company/product, the number, the place.
- Example: `*GOOGLE* සමාගම ඇමරිකාවේ *WYOMING* ප්‍රාන්තයේ *ඩොලර් බිලියන 17ක* ආයෝජනයකින් නව *AI DATA CENTER* එකක් ඉදිකිරීමට සූදානම් වෙයි`

**Other fields:** `tag` (e.g. "Tech Daily", "Space & Tech", "Game Release", "Movie Release", "Interesting Facts", "World News", "Politics"),
`date` (e.g. "14 Nov 2026"), `footerLeft`: "AI Automated News", `footerRight`: "Source: <main source>", `maxLines`: 3.

**caption.txt** — Sinhala, 2–4 short sentences explaining the story + 5–7 hashtags (always end with `#SinhalaNews #AsiriGayashan`) + a `Sources:` line naming the outlets.

## 4. Make the 5-second pixel animation
Read `engine/pixelkit.py` (palette, sprites, Scene helpers) and copy the structure of `engine/examples/first-bug/post.json`.

- Canvas: `w 90, h 44, scale 10`. Sky panel `Scene().sky()`, ground at y = 40 (`.ground()`). Characters stand on y = 40.
- Static background → `pixel.layers`. Moving things → `anim.actors` (`duration: 5`, `fps: 24`).
- **Tell a tiny cute cartoon story in 3–4 beats** (e.g. something arrives → something happens → reaction → result/punchline).
- Style: childish, cute, round, big eyes, simple shapes. **Bright colours** (blue, red, pink, yellow, neon green, cyan) on the light sky.
- Actor options: `frames` + `fps` (flapping/walking), `path` [[t,x,y],…] with `ease:"io"`, `show` [t0,t1], `shake` [t0,t1,amp],
  `swap` [[t, frames]], `blink` [hz], `bob` [amp,hz], bursts `{type:"burst", t0,x,y,n,colors,speed,life,gravity}`.
- Pixel text: layer `{type:"text", text:"2027", c:"D"}` (A–Z, 0–9, $, %, ., -).
- Make the last beat readable (it is also the cover frame at 60%).
- **Never draw** logos, brand mascots, game/movie characters, real people's likeness, flags of a party, weapons or gore.
  Use generic symbols instead (controller, rocket, phone, calendar, globe, ballot box, handshake, coin…).
- Serious stories (deaths, disasters, conflict, politics): calm, respectful animation only — no explosions, jokes or happy faces.

## 5. Save, check, commit
```
queue/<YYYY-MM-DD>/<HHMM>_<short-slug>/post.json
queue/<YYYY-MM-DD>/<HHMM>_<short-slug>/caption.txt
```
```bash
python scripts/validate_post.py queue/<date>/<HHMM_slug>    # must print OK; look at preview.png
git add queue && git commit -m "Post <date> <HHMM>: <short title>" && git push
```
(`preview.png` is git-ignored. The American Captain font is a secret, so the preview uses a fallback font for English words — the real render is done by GitHub Actions.)

## 6. Report
Send Asiri a short message: the headline, the topic, the sources, and that the post is waiting for approval in GitHub
(Actions → "Render & publish news posts" → Review deployments → Approve).
