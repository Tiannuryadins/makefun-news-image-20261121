# The World in One Image — 21 November 2026

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/tiannuryadins/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/tiannuryadins/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

Entry for [news-image-20261121](https://make.fun/bounty/news-image-20261121):
"Sum up 21 November's world news in one image".

`main.py` (Python 3.13, standard library only) draws a 1024×1024
newspaper front page — masthead, lead story, stats strip and 12 story
cards — and writes it deterministically to `/output/entry.png`
(two runs produce identical bytes; no network at runtime).

Lead story: Russian missiles hit Poland — two missiles and a
suspected drone came down; Warsaw calls it a deliberate provocation,
NATO calls it a grave violation of its airspace.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
