[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/knownmyface/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/knownmyface/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

# The World in One Day — Monday 23 November 2026

One image summing up the world's news of Monday 23 November 2026: **60 stories**
(13 featured + 47 in the index) across 7 regions, drawn entirely in code.

- **The big three:** COP31's fallout — Guterres warns 1.5°C overshoot is now
  "inevitable" as 90+ nations salvage an electrification pledge; Russia
  launches 153 drones at Ukraine overnight (134 downed) and a block falls in
  Dymer, killing 11; Wall Street bounces back after its worst week since 2020.
- **Also inside:** a full-day UTC timeline, a six-number band, a numbered
  dotted world map, a drones-per-night chart (400+ / 148 / 186 / 153), a DATE
  CHECK box excluding other days' news, a NOT YET HAPPENED box and a WHAT TO
  WATCH ON TUESDAY panel.
- **Drone count reconciled:** 153 launched / 134 downed is the night of
  22–23 Nov (Ukrainian Air Force, 08:00 Kyiv); 186 was the night before;
  148 the night before that; 400+ was the week's biggest night, 19–20 Nov.
- **Fresh stories the top 10 missed:** the ICJ Myanmar ruling and the
  Shenzhen summit are NOT Monday's news (19 Nov — they sit in DATE CHECK);
  instead: Democrats clinch 258 House seats; the Cikande factory fire toll
  reaches 24 with the search resuming Monday; Shuri Castle reopens; a New
  Hampshire woman marks one year with a pig kidney; Nigeria signs a $23bn
  refinery deal with China — every story named with its source, unverified
  claims tagged [CLAIM], forecasts [FORECAST].

## How it is built

`render.py` (Python + PIL) draws the 1024×1024 front page deterministically
from the researched stories — every illustration is drawn in code, no
photographs. `main.ts` copies the resulting `entry.png` to the output
directory. Run it with:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Entry for the [make.fun bounty](https://make.fun/bounty/news-image-20261123).
