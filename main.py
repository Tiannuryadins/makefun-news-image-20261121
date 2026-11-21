#!/usr/bin/env python3
"""news-image-20261121: "The World in One Image - Saturday 21 November 2026".

A self-contained, deterministic newspaper front page rendered with the
standard library only (no network, no fonts, no image files). It draws a
1024x1024 PNG: masthead, lead story, stats strip and 12 story cards,
then writes it to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).

Every line of this program was written in the build session for this
competition. The 5x7 bitmap font below was typed out by hand for this
entry; the story texts come from public news reports of 21 Nov 2026
(see BUILD-TRANSCRIPT.md for the story table and sources).
"""

import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (248, 244, 233)
INK = (26, 26, 26)
NAVY = (20, 33, 61)
WHITE = (255, 255, 255)
RED = (185, 28, 28)
GREY = (110, 108, 100)
CARD = (255, 255, 255)
RULE = (180, 175, 160)

# ---------------------------------------------------------------- font
# 5x7 bitmap font, one glyph per character. '#' is a set pixel, '.'
# is empty. Uppercase letters, digits and the punctuation the poster
# uses. Unknown characters render as a blank.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
}

FONT.update({
    "0": (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    "(": ("...##", "..#..", ".#...", ".#...", ".#...", "..#..", "...##"),
    ")": ("##...", "..#..", "...#.", "...#.", "...#.", "..#..", "##..."),
    "/": ("....#", "....#", "...#.", "...#.", "..#..", ".#...", "#...."),
    "%": ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "=": (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    "&": (".##..", "#..#.", "#.#..", ".#...", "#.##.", "#..#.", ".##.#"),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
})

BLANK = (".....",) * 7


# ---------------------------------------------------------------- canvas
class Canvas:
    """An RGB pixel buffer with tiny vector/text drawing helpers."""

    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set_px(self, x, y, rgb):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = rgb

    def fill_rect(self, x, y, w, h, rgb):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        r, g, b = rgb
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = r, g, b

    def border(self, x, y, w, h, rgb, t=1):
        self.fill_rect(x, y, w, t, rgb)
        self.fill_rect(x, y + h - t, w, t, rgb)
        self.fill_rect(x, y, t, h, rgb)
        self.fill_rect(x + w - t, y, t, h, rgb)

    def line(self, x0, y0, x1, y1, rgb):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set_px(x0, y0, rgb)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, rgb):
        for dy in range(-r, r + 1):
            span = int((r * r - dy * dy) ** 0.5)
            self.fill_rect(cx - span, cy + dy, span * 2 + 1, 1, rgb)

    def ring(self, cx, cy, r, rgb):
        steps = max(24, r * 6)
        for k in range(steps):
            import math
            a = 2 * math.pi * k / steps
            self.set_px(int(cx + r * math.cos(a)), int(cy + r * math.sin(a)), rgb)

    # -- text ------------------------------------------------------
    def char_w(self, scale):
        return 5 * scale + scale

    def text_w(self, s, scale):
        return len(s) * self.char_w(scale) - scale

    def draw_char(self, ch, x, y, scale, rgb, bold=False):
        rows = FONT.get(ch, BLANK)
        for ry, row in enumerate(rows):
            for rx, bit in enumerate(row):
                if bit != "#":
                    continue
                for sy in range(scale):
                    for sx in range(scale):
                        self.set_px(x + rx * scale + sx, y + ry * scale + sy, rgb)
                        if bold:
                            self.set_px(x + rx * scale + sx + 1, y + ry * scale + sy, rgb)

    def draw_text(self, s, x, y, scale, rgb, bold=False):
        cx = x
        for ch in s:
            self.draw_char(ch, cx, y, scale, rgb, bold)
            cx += self.char_w(scale)
        return cx - x

    def wrap(self, s, max_chars):
        """Greedy word wrap to at most max_chars per line."""
        words = s.split(" ")
        lines = []
        cur = ""
        for word in words:
            while len(word) > max_chars:
                if cur:
                    lines.append(cur)
                    cur = ""
                lines.append(word[:max_chars])
                word = word[max_chars:]
            trial = (cur + " " + word).strip() if cur else word
            if len(trial) <= max_chars:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines


def encode_png(w, h, px):
    """Deterministic whole PNG: IHDR + one IDAT + IEND, no metadata."""
    raw = bytearray()
    stride = w * 3
    for y in range(h):
        raw.append(0)
        raw += px[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 6)

    def chunk(tag, data):
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", comp)
        + chunk(b"IEND", b"")
    )


# ---------------------------------------------------------------- stories
# Each card: tile letter, tile colour, kicker, headline, body (<=48 chars).
# Lead + 12 cards = 13 stories. 11 of them are events first reported on
# 21 Nov 2026; the ICJ verdict (19 Nov) and the UK-EU signing (20 Nov)
# are continuing stories dominating 21 Nov reporting (see transcript).
LEAD = {
    "kicker": "CONFLICT - POLAND",
    "headline": "RUSSIAN MISSILES HIT POLAND",
    "body": (
        "TWO MISSILES AND A SUSPECTED DRONE CAME DOWN IN POLAND. "
        "WARSAW CALLS IT A DELIBERATE PROVOCATION. NATO CALLS IT "
        "A GRAVE VIOLATION OF ITS AIRSPACE."
    ),
}

CARDS = [
    ("$", (22, 101, 52), "MARKETS - NEW YORK",
     "S&P 500 IN CORRECTION",
     "STOCKS FELL 3.7% AS AI SHARES SOLD OFF."),
    ("J", (30, 58, 95), "JUSTICE - THE HAGUE",
     "MYANMAR GUILTY OF GENOCIDE",
     "FIRST TIME A STATE IS HELD RESPONSIBLE."),
    ("D", (15, 118, 110), "DIPLOMACY - BRUSSELS",
     "UK AND EU SIGN THREE DEALS",
     "PACTS ON FOOD TRADE, CARBON AND YOUTH TRAVEL."),
    ("J", (30, 58, 95), "JUSTICE - PARIS",
     "OFFICERS GUILTY OVER ZECLER BEATING",
     "THREE OFFICERS CONVICTED OVER THE 2020 BEATING."),
    ("T", (107, 33, 168), "TECH - WASHINGTON",
     "900,000 AI CHIPS FOR CHINA",
     "THE US APPROVED EXPORTS OF ALMOST 900,000 CHIPS."),
    ("A", (71, 85, 105), "AVIATION - SIBERIA",
     "19 KILLED IN PLANE CRASH",
     "MILITARY TRANSPORT CRASHED IN SIBERIA."),
    ("T", (107, 33, 168), "TECH - CALIFORNIA",
     "NVIDIA PROBES ITS OWN CHIEF",
     "NVIDIA HIRED A TOP LAW FIRM OVER SPY CLAIMS."),
    ("C", (194, 65, 12), "CYBER - NEW YORK",
     "BANKS HIT BY VENDOR ATTACK",
     "JPMORGAN, VISA AND MASTERCARD HIT."),
    ("B", (146, 64, 14), "BUSINESS - US",
     "ANTHROPIC IPO TOPS $81.3B",
     "RAISED $81.3B, BEATING SPACEX'S RECORD."),
    ("C", (185, 28, 28), "CONFLICT - GULF",
     "TRUMP DEMANDS A REAL DEAL",
     "IRAN WANTS A DEAL BUT NOT ONE HE WILL ACCEPT."),
    ("H", (190, 24, 93), "HEALTH - US",
     "PILL HAILED AS CANCER BREAKTHROUGH",
     "TUMOURS STOPPED GROWING IN NEARLY ALL PATIENTS."),
    ("C", (185, 28, 28), "CONFLICT - RIYADH",
     "HOUTHI MISSILES DOWNED",
     "THREE MISSILES DESTROYED OVER RIYADH. 41 KILLED."),
]

STATS = [
    "S&P 500 -3.7%",
    "NASDAQ -5%",
    "19 DEAD IN SIBERIA",
    "INDIA 159/1 V NZ",
]


# ---------------------------------------------------------------- poster
def draw_lead_art(cv, x, y, w, h):
    """Abstract night-sky panel: two missile streaks over dark ground."""
    cv.fill_rect(x, y, w, h, NAVY)
    # stars
    for sx, sy in ((30, 26), (90, 60), (170, 30), (230, 70), (130, 90),
                   (60, 110), (200, 120), (260, 40), (150, 150)):
        cv.set_px(x + sx, y + sy, WHITE)
        cv.set_px(x + sx + 1, y + sy, WHITE)
    # pale moon
    cv.disc(x + w - 52, y + 44, 22, (232, 226, 205))
    cv.disc(x + w - 58, y + 38, 18, NAVY)
    # ground
    cv.fill_rect(x, y + h - 34, w, 34, (12, 20, 38))
    cv.line(x, y + h - 34, x + 90, y + h - 58, (12, 20, 38))
    cv.line(x + 90, y + h - 58, x + 190, y + h - 34, (12, 20, 38))
    # two missile streaks ending in bursts
    for (x0, y0, x1, y1) in ((18, 18, 120, 128), (96, 10, 210, 138)):
        cv.line(x + x0, y + y0, x + x1, y + y1, (239, 68, 68))
        cv.line(x + x0 + 1, y + y0, x + x1 + 1, y + y1, (239, 68, 68))
        bx, by = x + x1, y + y1
        for dx, dy in ((0, 0), (-6, -3), (6, -3), (-3, 6), (3, 6),
                       (-7, 0), (7, 0), (0, -7), (0, 7)):
            cv.set_px(bx + dx, by + dy, (250, 204, 21))
    cv.draw_text("POLAND", x + 14, y + h - 28, 2, WHITE, bold=True)


def render():
    # Guard: no story text may silently lose words to the 2-line cap.
    _probe = Canvas(1, 1, PAPER)
    for _letter, _colour, _k, headline, body in CARDS:
        assert len(_probe.wrap(headline, 24)) <= 2, headline
        assert len(_probe.wrap(body, 24)) <= 2, body
    cv = Canvas(W, H, PAPER)

    # ---- masthead
    title = "THE WORLD IN ONE IMAGE"
    cv.draw_text(title, (W - cv.text_w(title, 5)) // 2, 34, 5, NAVY, bold=True)
    date = "SATURDAY 21 NOVEMBER 2026"
    cv.draw_text(date, (W - cv.text_w(date, 3)) // 2, 86, 3, INK, bold=True)
    cv.fill_rect(24, 118, W - 48, 3, NAVY)
    cv.fill_rect(24, 125, W - 48, 1, NAVY)

    # ---- lead story
    cv.draw_text(LEAD["kicker"], 24, 142, 2, RED, bold=True)
    lx, lw = 24, 660
    lines = cv.wrap(LEAD["headline"], 27)
    hy = 168
    for ln in lines:
        cv.draw_text(ln, lx, hy, 4, INK, bold=True)
        hy += 34
    by = hy + 10
    for ln in cv.wrap(LEAD["body"], 54):
        cv.draw_text(ln, lx, by, 2, INK)
        by += 18
    draw_lead_art(cv, 716, 140, 284, 200)

    # ---- stats strip
    cv.fill_rect(24, 372, W - 48, 44, NAVY)
    cell = (W - 48) // 4
    for i, stat in enumerate(STATS):
        cx0 = 24 + i * cell
        cv.draw_text(stat, cx0 + (cell - cv.text_w(stat, 2)) // 2, 388, 2, WHITE, bold=True)
        if i:
            cv.fill_rect(cx0, 380, 1, 28, (90, 105, 140))

    # ---- story cards, 3 columns x 4 rows
    gx, gy, cw, ch, gap = 24, 428, 317, 132, 12
    for idx, (letter, colour, kicker, headline, body) in enumerate(CARDS):
        col, row = idx % 3, idx // 3
        x = gx + col * (cw + gap)
        y = gy + row * (ch + gap)
        cv.fill_rect(x, y, cw, ch, CARD)
        cv.border(x, y, cw, ch, RULE)
        cv.fill_rect(x + 10, y + 10, 34, 34, colour)
        cv.draw_text(letter, x + 10 + (34 - cv.text_w(letter, 4)) // 2,
                     y + 10 + 3, 4, WHITE, bold=True)
        cv.draw_text(kicker, x + 52, y + 16, 2, colour, bold=True)
        hlines = cv.wrap(headline, 24)
        hy2 = y + 52
        for ln in hlines[:2]:
            cv.draw_text(ln, x + 10, hy2, 2, INK, bold=True)
            hy2 += 16
        by2 = y + 52 + 2 * 16 + 6
        for ln in cv.wrap(body, 24)[:2]:
            cv.draw_text(ln, x + 10, by2, 2, (60, 58, 52))
            by2 += 16

    # ---- footer
    cv.fill_rect(24, 1000, W - 48, 1, RULE)
    foot = "MAKE.FUN NEWS-IMAGE-20261121 - 13 STORIES FROM SATURDAY 21 NOVEMBER 2026"
    cv.draw_text(foot, (W - cv.text_w(foot, 1)) // 2, 1008, 1, GREY)
    return encode_png(W, H, cv.px)


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    png = render()
    path = os.path.join(outdir, "entry.png")
    with open(path, "wb") as f:
        f.write(png)
    print("wrote %s (%d bytes)" % (path, len(png)))


if __name__ == "__main__":
    main()
