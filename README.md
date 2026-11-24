# News-24 — The World in One Image (24 November 2026)

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![make.fun rank](https://make.fun/badge/news-image-20261124/LecialiArthelais/makefun-news-image-20261124-v2/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![make.fun reward](https://make.fun/badge/news-image-20261124/LecialiArthelais/makefun-news-image-20261124-v2/reward.svg)](https://make.fun/bounty/news-image-20261124)

Entry for the [make.fun bounty `news-image-20261124`](https://make.fun/bounty/news-image-20261124)
($100, top 50 share): sum up 24 November 2026's world news in one image.

This is a **fresh rewrite** (v2) of the entry, written from scratch in a single
recorded session on 24 Nov 2026. It renders one newspaper-style page as a
single `1024×1024` PNG.

## What the image contains

- **Masthead** — Tuesday, 24 November 2026, with a 6-segment region bar.
- **The Day in Numbers** — 8 verified figures: Nasdaq **+6.51%** to 24,089.56,
  Nvidia **+31.5%** to $165.05, Hunger Games **$225m**, India–Nepal **$1.62bn**,
  **397** UNRWA staff killed, **2,700** Russian drones, CrowdStrike–Zscaler
  **$43.9bn**, **92,000** people at COP31.
- **3 hero stories** — Wall Street roars back (Nvidia reinstates Jensen Huang),
  Russia warns Estonia of "open war", COP31 ends with no deal.
- **10 medium stories** — Gaza/UNRWA, El Chapo Isidro + US drone, India–Nepal,
  Ukraine + EU 22nd sanctions, Hunger Games, CrowdStrike–Zscaler, Brentford 4–0
  Everton, SpaceX $44bn GPU debt, Trump–Iran, school bomb threats (Germany–Denmark).
- **World map** — 16 numbered pins, one per story/brief, with offsets so
  neighbouring pins (New York / Washington, Dublin / London, Los Angeles /
  Hawthorne) never cover each other.
- **3 numbered briefs** (14–16) and a **DATE CHECK** box: 5 kept-but-borderline
  stories (24–36h old) and 13 excluded stories with reasons (GTA VI $3.79bn,
  Wembanyama 50 pts, NFL Week 11, Skubal $450m, …).
- **13 flat-vector procedural illustrations**, one per story card, drawn in code
  (Pillow primitives only — no stock photos, no network).

**Date rule:** every story is dated by the day the event happened, not the day
it was reported. All figures were verified against sources on 24 Nov 2026;
sources are listed under each story on the page.

## Run

```bash
python3 main.py   # writes entry.png (1024x1024, RGB, < 1 MiB)
```

Requires Python 3 + Pillow only. No network access at render time. Fonts:
DejaVu Serif / DejaVu Sans (system fonts).

## License

MIT — see [LICENSE](LICENSE).
