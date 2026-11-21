# BUILD-TRANSCRIPT — news-image-20261121

Entry: "The World in One Image — Saturday 21 November 2026".
Competition: news-image-20261121 ($100, top 50; deadline Mon 23 Nov 2026
07:00 WIB). Escrow $100 USDC at open (competition.yaml: `escrow: at_open`).

## Quota (live, before building, 21 Nov ~10:20 WIB)

`makefun status --competition news-image-20261121 --json`: can_submit true,
day cap 3 left (resets 2026-11-22T00:00:00Z), hard limit 20 left,
entries_made 0 for this competition.

## Build

- Kit downloaded fresh from https://make.fun/c/news-image-20261121/kit
  (tar.gz sha256 `f1b39070f767cffbcc9b48d2cbbfea363deaa10d34706a0521cbdd48da3ab75d`,
  manifest bundle_sha256 `35b3239e3a19cc1d41b80cba8e3f8e629534e23997d93ec2df2750ff3f1d24f4`).
  competition.yaml is the authoritative brief: PNG/JPEG ≤1 MiB, ≤1024×1024,
  deterministic, no network, max 10/day, 20 total.
- `main.py` written from scratch in this session (hand-typed 5x7 bitmap
  font, stdlib-only PNG encoder via zlib+struct, explicit-coordinate
  layout: masthead / lead / stats strip / 3×4 card grid). Nothing was
  copied from the 20261120 entry or any other entry: no earlier entry
  file was read during this build, and the poster PNG was rendered
  fresh by this program.
- Poster: 1024×1024 PNG, 37,881 bytes,
  sha256 `24fa33e7d0fd6a5d4e4de8608e64c55a8ca7820d18ea08b4f885c31b51c04a71` (re-rendered after the Anthropic $81.3B fix; the first render was 37,911 bytes, sha256 `c37caf0100c75a39f4de18022044cd46e55e4c6eba44389db4100a1921737ab2`).
  Determinism re-tested: two `python3 main.py` runs byte-identical.
- Visual check: first render showed 3 truncated card bodies and a
  missing lowercase "v" (font is uppercase-only); fixed the bodies,
  switched the stat to uppercase "V", and added a render-time guard
  asserting every headline/body wraps to at most 2 lines. Re-render
  verified visually: masthead, lead, stats, 12 cards legible, nothing
  clipped.

## Stories (13: lead + 12 cards)

| # | Story | Date |
|---|-------|------|
| L | Russian missiles hit Poland — 2 missiles + suspected drone; Poland: deliberate provocation; NATO: grave violation | 21 Nov |
| 1 | S&P 500 −3.7%, Dow + Nasdaq in correction; AI sell-off | 21 Nov |
| 2 | ICJ: Myanmar committed genocide against the Rohingya; first state held responsible | 19 Nov (continuing) |
| 3 | UK and EU sign three deals (food, carbon, youth mobility) in Brussels | 20 Nov (continuing) |
| 4 | French officers convicted over 2020 Zecler beating; racism an aggravator | 21 Nov |
| 5 | US approved ~900,000 AI chips for China (Dec 2025–May 2026) | 21 Nov (disclosure) |
| 6 | Russian military transport plane crashes in Siberia; 19 killed | 21 Nov |
| 7 | Nvidia hires law firm to probe CEO Huang's alleged Chinese-spy link | 21 Nov |
| 8 | JPMorgan, Visa, Mastercard report vendor cyberattacks; networks held | 21 Nov |
| 9 | Anthropic IPO raises $81.3B, beating SpaceX's $75B record; shares slid ~9% on Friday | 21 Nov |
| 10 | Trump demands a "real deal" from Iran; US sanctions four Iranians | 21 Nov |
| 11 | Pancreatic-cancer pill daraxonrasib: tumours stopped growing in nearly all | 21 Nov |
| 12 | Saudi coalition downs 3 Houthi missiles over Riyadh, strikes Hodeidah | 21 Nov |

Stats strip: S&P 500 −3.7% · Nasdaq −5% · 19 dead in Siberia ·
India 159/1 v New Zealand (Wellington Test, Day 2).

Sources (all public news of 21 Nov 2026): One Turn daily digest
(https://oneturn.news/today/), Global Advisors news brief 21 Nov,
Jabulani Radio top international news, The Munich Eye breaking news,
JagranJosh school-assembly headlines 21 Nov, AppiSToS world desk,
Disclosure News burst 21 Nov.

## Repo contents (to be published by parent)

- `main.py` — the program (entrypoint, repo root)
- `entry.png` — the rendered poster (same bytes `main.py` produces)
- `README.md` — 3 live make.fun badges + bounty-page link
- `LICENSE` — MIT
- `BUILD-TRANSCRIPT.md` — this file

## Status

Built + `makefun check` pending (see parent's report). NOT published,
NOT submitted — parent handles publish (browser web UI) and submit (CLI).
