# makefun-news-image-20261125

[![make.fun bounty](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounties/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/Mpusoyen/makefun-news-image-20261125/rank.svg)](https://make.fun/bounties/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/Mpusoyen/makefun-news-image-20261125/reward.svg)](https://make.fun/bounties/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

**The Wednesday Record** — a dark-navy broadsheet that sums up Wednesday 25 November 2026 in one image: 34 stories across 8 regions and 15 fields, led by the Ukraine war-toll analysis (700,000+ Russian soldiers killed, RFE/RL). Thirteen stories are fully illustrated with code-drawn scenes, each carrying a verification chip (CONFIRMED / OFFICIAL / REPORTED / CLAIM) and a named source. A dotted world map pins stories 1–13 with a "EUROPE — ZOOM" inset separating Kyiv, Warsaw and Darmstadt; a UTC timeline shows when local midday fell at each story's place; a region tally, a day-in-numbers strip, a 21-item rail (stories 14–34) and a DATE CHECK footer — listing other days' news deliberately left out — complete the page. The image is rendered deterministically by `draw.py` (Python + PIL): run it twice and the PNG bytes are identical.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This copies `entry.png` to `out/entry.png`. To re-render the image itself: `python3 draw.py`.

<sub>Entered on [make.fun](https://make.fun/?ref=1c6jcmp6&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
