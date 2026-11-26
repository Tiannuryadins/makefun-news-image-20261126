#!/usr/bin/env python3
"""Render the 26 November 2026 world-news poster (1024x1024).

Original build for make.fun bounty news-image-20261126.
Every story was verified against live sources on 26 Nov 2026 before
rendering (see SOURCES in the story table below). No network at render
time; all facts are baked in as constants. Pure PIL + stdlib.

Layout (per the news-image playbook): big serif date masthead, red deck
naming the 3 top stories, a 7-stat number strip, 7 region tabs,
3 large illustrated leads, 2 rows of 4 illustrated cards, world map
with story dots + a 16-row illustrated index. Every card carries a
PIL-drawn illustration made fresh for this edition: no text-only
cards, no illustration recycled from an earlier edition.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poster.png")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF_R = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

# ---------------------------------------------------------------- palette
PAPER = (250, 247, 238)      # newsprint cream
INK = (22, 22, 22)
MUTED = (90, 86, 78)
RULE = (160, 152, 132)
RED = (178, 34, 34)          # headline accent / kicker
NAVY = (24, 48, 88)
SKY = (146, 190, 220)
SEA = (64, 120, 168)
SAND = (232, 214, 176)
GREEN = (34, 139, 64)
ORANGE = (232, 116, 24)
GOLD = (214, 164, 32)
TEAL = (18, 130, 120)
PURPLE = (96, 60, 140)

# ---------------------------------------------------------------- stories
# (kicker, headline, body, art, map lon/lat)
LEADS = [
    ("GULF  \u2022  STRAIT OF HORMUZ",
     "Mines in the Strait: two tankers ablaze",
     "Two tankers hit mines and catch fire, the IRGC Navy says. "
     "Washington tells US citizens to leave Iran.",
     "mines", (57, 26)),
    ("USA  \u2022  THANKSGIVING",
     "Thanksgiving storm grounds the parade",
     "Macy's parade is postponed to Saturday \u2014 a first in its "
     "history \u2014 as a storm targets 250m people.",
     "parade", (-74, 40.7)),
    ("UKRAINE  \u2022  DEEP STRIKES",
     "Kyiv hits air base, refineries in Russia",
     "Ukraine hits Savasleyka air base, knocking out 5 jets, and "
     "strikes two refineries 800 km inside Russia.",
     "airfield", (43.5, 55.5)),
]

CARDS = [
    ("MARKETS",
     "Nvidia gives back 8% after record rally",
     "Shares fall 8.2% to $151.60 a day after the +31% rebound on "
     "Huang's return.",
     "nvdadip", (-122, 37)),
    ("CLIMATE  \u2022  ANTALYA",
     "Pope Leo laments COP31 collapse",
     "Pope Leo laments the failed talks; OPEC blames the EU for the "
     "Antalya collapse.",
     "cop31", (30.7, 36.9)),
    ("GULF  \u2022  RIYADH",
     "Houthi drone hits Riyadh tower again",
     "A Houthi drone hits Riyadh's tallest tower again; 11 wounded.",
     "tower", (46.7, 24.6)),
    ("SPORT  \u2022  BRUGES",
     "Isak brace as Liverpool cruise 3-0",
     "Isak scores twice in Liverpool's 3-0 win at Club Brugge; Roma "
     "hold PSG 2-2.",
     "football", (3.2, 51.2)),
    ("SPACE  \u2022  JIUQUAN",
     "Shenzhou-24 carries first Pakistani to orbit",
     "Shenzhou-24 carries Muhammad Zeeshan Ali, the first Pakistani "
     "in orbit.",
     "rocket", (100.3, 40.9)),
    ("TECH  \u2022  NEW YORK",
     "Huawei convicted on 10 of 12 counts",
     "A Brooklyn jury convicts Huawei on 10 of 12 counts of tech "
     "theft and fraud.",
     "gavel", (-73, 41.5)),
    ("TRADE  \u2022  WASHINGTON",
     "Trump plans new wave of global tariffs",
     "Trump plans new global tariffs, reviving trade-war fears in "
     "the EU and China.",
     "tariffs", (-77, 38.9)),
    ("ASIA  \u2022  JAKARTA",
     "Indonesia\u2013Norway sign 12Mt carbon deal",
     "Indonesia signs a 12-million-ton carbon deal with Norway to "
     "boost solar power.",
     "carbon", (106.8, -6.2)),
]

# (text, mini-icon kind)
INDEX = [
    ("Vance blames Iran war for GOP losing both chambers in the midterms.",
     "flag"),
    ("Trump \u2018inclined\u2019 to renew Iran strikes after New Year if talks fail.",
     "flag"),
    ("US tells citizens to leave Iran immediately as tensions rise.",
     "plane"),
    ("EU to invest $55bn in AI and quantum computing.", "chart"),
    ("Meta rethinks 2030 net-zero goal as AI emissions climb 45%.", "globe"),
    ("Tesla wins key FSD approval in Italy, expanding across Europe.",
     "bolt"),
    ("Sarkozy and Bruni to face trial in France on conspiracy charges.",
     "gavel"),
    ("Six dead after Cessna crashes in Gulf of Mexico near Mississippi.",
     "plane"),
    ("Roma end PSG's perfect Champions League record in 2-2 Paris draw.",
     "ball"),
    ("Bayern beaten 2-1 at Lille; Man Utd draw 2-2 in chaotic Lisbon night.",
     "ball"),
    ("Real Madrid 5-1 PSV: Bellingham wondergoal keeps 100% record.",
     "ball"),
    ("New Jersey declares emergency; St. Louis braced for 8 in of snow.",
     "storm"),
    ("Poland plans no-fly zone along its eastern border from late Dec.",
     "plane"),
    ("Ukraine's Blysk laser downs a Geran drone in first combat use.",
     "bolt"),
    ("EU adds 15 Russian defence-linked entities to export list.", "flag"),
    ("Black Friday: some brands opt out as war reignites inflation.",
     "chart"),
]

NUMBERS = [
    ("$91.40", "BRENT, +$2 ON DAY"),
    ("10", "TANKER STRIKES IN A WEEK"),
    ("\u221242%", "HORMUZ TRAFFIC VS PREWAR"),
    ("\u22128.2%", "NVIDIA, DAY AFTER +31%"),
    ("4,500+", "US FLIGHTS DELAYED WED"),
    ("250M+", "PEOPLE IN STORM'S PATH"),
    ("2,091", "RUSSIAN LOSSES IN A DAY"),
]

REGIONS = [
    ("GULF", RED), ("EUROPE", NAVY), ("AMERICAS", GREEN),
    ("ASIA", ORANGE), ("CLIMATE", TEAL), ("SPORT", PURPLE),
    ("TECH", (60, 60, 60)),
]

DECK = ("Mines in the Strait, a storm over Thanksgiving, and Kyiv's "
        "deep strikes into Russia.")

SOURCES = ("Sources: Reuters, CNN, AP, UEFA, Fox Weather, ME Forum, "
           "Hudson Institute, Carbon Credits \u2014 26 Nov 2026")

# ---------------------------------------------------------------- fonts
def F(path, size):
    return ImageFont.truetype(path, size)

# ---------------------------------------------------------------- text utils
def wrap(draw, text, font, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def text_block(draw, x, y, text, font, max_w, leading, fill=INK, max_lines=None):
    lines = wrap(draw, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y

# ---------------------------------------------------------------- flags
def stripe_flag(d, x, y, w, h, bands, vertical=False):
    """bands: list of colours, drawn as equal horizontal (default) or
    vertical stripes inside the given box."""
    n = len(bands)
    for i, colour in enumerate(bands):
        if vertical:
            d.rectangle([x + w * i / n, y, x + w * (i + 1) / n, y + h], fill=colour)
        else:
            d.rectangle([x, y + h * i / n, x + w, y + h * (i + 1) / n], fill=colour)
    d.rectangle([x, y, x + w, y + h], outline=(40, 40, 40), width=1)

def star(d, cx, cy, r, colour):
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=colour)

# ---------------------------------------------------------------- art
def art_mines(d, x, y, w, h):
    """Hormuz at dusk: spiked naval mines, a tanker ablaze, smoke."""
    d.rectangle([x, y, x + w, y + h * 0.45], fill=(250, 150, 80))
    d.ellipse([x + w - 64, y + 8, x + w - 16, y + 56], fill=(255, 210, 110))
    d.rectangle([x, y + h * 0.45, x + w, y + h], fill=(22, 58, 92))
    for wy in range(3):
        yy = y + h * 0.52 + wy * 14
        d.line([(x + 6, yy), (x + w - 6, yy)], fill=(64, 110, 150), width=2)
    # tanker mid-frame, burning
    tx, ty = x + w * 0.10, y + h * 0.52
    d.polygon([(tx, ty), (tx + w * 0.80, ty), (tx + w * 0.74, ty + 20),
               (tx + 6, ty + 20)], fill=(38, 40, 46))
    d.rectangle([tx + 12, ty - 24, tx + 40, ty], fill=(200, 60, 50))
    d.rectangle([tx + w * 0.62, ty - 30, tx + w * 0.72, ty], fill=(220, 220, 220))
    fx = tx + w * 0.42
    d.polygon([(fx - 30, ty - 2), (fx - 18, ty - 46), (fx - 4, ty - 16),
               (fx + 10, ty - 52), (fx + 24, ty - 18), (fx + 34, ty - 38),
               (fx + 38, ty - 2)], fill=ORANGE)
    d.polygon([(fx - 14, ty - 2), (fx - 5, ty - 30), (fx + 7, ty - 10),
               (fx + 16, ty - 32), (fx + 20, ty - 2)], fill=GOLD)
    for sx, sy, sr in ((fx - 26, ty - 52, 9), (fx - 4, ty - 62, 11),
                       (fx + 18, ty - 54, 9)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(90, 90, 94))
    # spiked mines in the foreground water
    for mx, my, mr in ((x + w * 0.16, y + h - 18, 11),
                       (x + w * 0.82, y + h - 14, 9)):
        for k in range(8):
            ang = k * math.pi / 4
            d.line([(mx, my), (mx + (mr + 7) * math.cos(ang),
                                my + (mr + 7) * math.sin(ang))],
                   fill=(20, 20, 20), width=3)
        d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(25, 25, 28),
                  outline=(120, 120, 120), width=1)
    d.text((x + 10, y + 8), "HORMUZ", font=F(SANS_B, 13), fill=(90, 40, 20))

def art_parade(d, x, y, w, h):
    """Storm over Manhattan: a giant balloon buffeted by wind and rain."""
    d.rectangle([x, y, x + w, y + h], fill=(58, 74, 96))
    # rain streaks
    for i in range(26):
        rx = x + (i * 37) % w
        ry = y + (i * 53) % h
        d.line([(rx, ry), (rx - 6, ry + 16)], fill=(140, 160, 185), width=2)
    # skyline silhouette
    for i, bh in enumerate((46, 66, 38, 78, 52, 60, 44)):
        bx = x + 8 + i * (w - 16) // 7
        d.rectangle([bx, y + h - bh, bx + (w - 16) // 7 - 4, y + h],
                    fill=(30, 38, 54))
        for wy in range(2):
            d.rectangle([bx + 5, y + h - bh + 8 + wy * 16, bx + 12,
                         y + h - bh + 14 + wy * 16], fill=(255, 210, 110))
    # giant balloon, tilted by the wind, with ropes and basket
    cx, cy = x + w * 0.52, y + h * 0.38
    d.ellipse([cx - 52, cy - 40, cx + 52, cy + 40], fill=(178, 34, 34))
    d.ellipse([cx - 52, cy - 40, cx - 18, cy + 40], fill=(220, 90, 60))
    d.ellipse([cx + 18, cy - 40, cx + 52, cy + 40], fill=(220, 90, 60))
    d.ellipse([cx - 12, cy - 40, cx + 12, cy + 40], fill=(255, 255, 255))
    d.line([(cx - 30, cy + 34), (cx - 12, cy + 62)], fill=(220, 220, 220), width=2)
    d.line([(cx + 30, cy + 34), (cx + 12, cy + 62)], fill=(220, 220, 220), width=2)
    d.rectangle([cx - 14, cy + 62, cx + 14, cy + 76], fill=(120, 84, 40))
    # wind gusts
    for wy in (y + 18, y + 34):
        d.arc([x + 10, wy, x + 90, wy + 22], 200, 340, fill=(200, 215, 230),
              width=3)
    d.text((x + 10, y + h - 20), "PARADE POSTPONED", font=F(SANS_B, 12),
           fill=(255, 255, 255))

def art_airfield(d, x, y, w, h):
    """Savasleyka air base: jets on the apron, a fireball over a hangar."""
    d.rectangle([x, y, x + w, y + h * 0.42], fill=(176, 200, 222))
    d.ellipse([x + 14, y + 10, x + 52, y + 48], fill=(255, 240, 180))
    d.rectangle([x, y + h * 0.42, x + w, y + h], fill=(96, 98, 92))
    # runway
    d.polygon([(x + w * 0.30, y + h), (x + w * 0.46, y + h * 0.46),
               (x + w * 0.54, y + h * 0.46), (x + w * 0.70, y + h)],
              fill=(60, 62, 66))
    for i in range(4):
        yy = y + h * (0.52 + i * 0.11)
        ww = 4 + i * 5
        d.line([(x + w // 2 - ww, yy), (x + w // 2 + ww, yy)],
               fill=(240, 240, 240), width=3)
    # hangar, burning
    hx, hy = x + w * 0.62, y + h * 0.50
    d.rectangle([hx, hy, hx + w * 0.30, hy + h * 0.30], fill=(120, 118, 112))
    d.polygon([(hx, hy), (hx + w * 0.15, hy - 22), (hx + w * 0.30, hy)],
              fill=(90, 88, 84))
    fx = hx + w * 0.15
    d.polygon([(fx - 26, hy - 4), (fx - 14, hy - 40), (fx - 2, hy - 14),
               (fx + 10, hy - 44), (fx + 22, hy - 12), (fx + 28, hy - 4)],
              fill=ORANGE)
    d.polygon([(fx - 10, hy - 4), (fx, hy - 26), (fx + 12, hy - 6)],
              fill=GOLD)
    d.ellipse([fx - 14, hy - 52, fx + 12, hy - 30], fill=(80, 80, 86))
    # two jets parked on the apron (delta-wing silhouettes)
    for jx, jy, js in ((x + w * 0.10, y + h * 0.66, 1.0),
                       (x + w * 0.30, y + h * 0.80, 0.8)):
        d.polygon([(jx, jy - 26 * js), (jx + 10 * js, jy - 6 * js),
                   (jx + 44 * js, jy + 2 * js), (jx + 10 * js, jy + 8 * js),
                   (jx, jy + 12 * js), (jx - 10 * js, jy + 8 * js),
                   (jx - 44 * js, jy + 2 * js), (jx - 10 * js, jy - 6 * js)],
                  fill=(52, 58, 66))
        d.ellipse([jx - 4, jy - 4, jx + 4, jy + 4], fill=(200, 200, 200))
    d.text((x + 10, y + 8), "SAVASLEYKA", font=F(SANS_B, 13), fill=(40, 50, 70))

def art_nvdadip(d, x, y, w, h):
    """Falling chart on a dark board: the day after the +31% rebound."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 26, 44))
    for gy in range(1, 4):
        yy = y + h * gy / 4
        d.line([(x + 8, yy), (x + w - 8, yy)], fill=(52, 72, 104), width=1)
    pts = [(x + 12, y + 14), (x + w * 0.28, y + 18),
           (x + w * 0.45, y + h * 0.30), (x + w * 0.62, y + h * 0.55),
           (x + w * 0.80, y + h * 0.72), (x + w - 12, y + h - 14)]
    d.line(pts, fill=(232, 80, 80), width=4, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex - 16, ey - 2), (ex - 2, ey + 12), (ex + 2, ey - 14)],
              fill=(232, 80, 80))
    d.text((x + 10, y + 6), "\u22128.2%", font=F(SANS_B, 26), fill=(232, 80, 80))
    d.text((x + 10, y + h - 20), "NVDA  \u2022  $151.60", font=F(SANS_B, 11),
           fill=(170, 195, 220))

def art_cop31(d, x, y, w, h):
    """A cracked globe: the climate talks end with no deal."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 240))
    cx, cy, r = x + w // 2, y + h // 2 + 4, 26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 120, 168))
    d.ellipse([cx - r * 0.55, cy - r * 0.75, cx + r * 0.15, cy - r * 0.25],
              fill=GREEN)
    d.ellipse([cx - r * 0.10, cy + r * 0.10, cx + r * 0.60, cy + r * 0.65],
              fill=GREEN)
    d.ellipse([cx - r * 0.85, cy + r * 0.30, cx - r * 0.35, cy + r * 0.70],
              fill=(120, 170, 110))
    # red crack zigzag across the globe
    d.line([(cx - r * 0.55, cy - r * 0.85), (cx - r * 0.15, cy - r * 0.35),
            (cx - r * 0.45, cy), (cx + r * 0.05, cy + r * 0.35),
            (cx - r * 0.20, cy + r * 0.70), (cx + r * 0.30, cy + r * 0.95)],
           fill=RED, width=4, joint="curve")
    d.text((x + 8, y + 6), "NO DEAL", font=F(SANS_B, 13), fill=RED)

def art_tower(d, x, y, w, h):
    """Riyadh's tallest tower at dusk, a drone above, smoke at the top."""
    d.rectangle([x, y, x + w, y + h], fill=(250, 190, 120))
    d.ellipse([x + w - 56, y + 8, x + w - 14, y + 50], fill=(255, 226, 140))
    # tower: twin pillars joined by an inverted arch near the top
    tx = x + w // 2
    d.rectangle([tx - 34, y + 26, tx - 14, y + h], fill=(70, 78, 92))
    d.rectangle([tx + 14, y + 26, tx + 34, y + h], fill=(70, 78, 92))
    d.polygon([(tx - 34, y + 26), (tx - 34, y + 46), (tx, y + 62),
               (tx + 34, y + 46), (tx + 34, y + 26)], fill=(70, 78, 92))
    for wy in range(5):
        yy = y + 76 + wy * 12
        d.rectangle([tx - 30, yy, tx - 18, yy + 5], fill=(255, 220, 130))
        d.rectangle([tx + 18, yy, tx + 30, yy + 5], fill=(255, 220, 130))
    # ground + city base
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(52, 48, 44))
    d.rectangle([x + 10, y + h - 34, x + 52, y + h - 16], fill=(80, 76, 70))
    d.rectangle([x + w - 52, y + h - 28, x + w - 10, y + h - 16],
                fill=(80, 76, 70))
    # smoke from the arch + quadcopter drone
    for sx, sy, sr in ((tx - 8, y + 14, 7), (tx + 6, y + 6, 8),
                       (tx + 16, y + 16, 6)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(96, 96, 100))
    dx, dy = x + w - 40, y + 22
    d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(30, 30, 30))
    for ox, oy in ((-11, -7), (11, -7), (-11, 7), (11, 7)):
        d.line([(dx, dy), (dx + ox, dy + oy)], fill=(30, 30, 30), width=2)
        d.ellipse([dx + ox - 5, dy + oy - 2, dx + ox + 5, dy + oy + 2],
                  fill=(60, 60, 60))

def art_football(d, x, y, w, h):
    """Night match: green pitch, goal, ball and a 0-3 scoreboard."""
    d.rectangle([x, y, x + w, y + h], fill=(38, 110, 58))
    for i in range(4):
        d.rectangle([x + i * w // 4, y, x + (i + 1) * w // 4, y + h],
                    fill=(46, 124, 66) if i % 2 == 0 else (38, 110, 58))
    d.ellipse([x + w // 2 - 34, y + h // 2 - 20, x + w // 2 + 34,
               y + h // 2 + 20], outline=(255, 255, 255), width=2)
    d.line([(x + w // 2, y), (x + w // 2, y + h)], fill=(255, 255, 255),
           width=2)
    # goal, right side
    gx, gy = x + w - 58, y + h // 2 - 24
    d.rectangle([gx, gy, gx + 44, gy + 48], outline=(255, 255, 255), width=3)
    for lx in range(gx + 8, gx + 44, 8):
        d.line([(lx, gy), (lx, gy + 48)], fill=(230, 230, 230), width=1)
    # ball + motion trail
    bx, by = x + 44, y + h // 2 + 6
    d.line([(bx + 44, by - 4), (bx + 74, by - 12)], fill=(255, 255, 255),
           width=2)
    d.ellipse([bx - 13, by - 13, bx + 13, by + 13], fill=(255, 255, 255),
              outline=(40, 40, 40), width=2)
    d.polygon([(bx, by - 5), (bx + 5, by), (bx, by + 5), (bx - 5, by)],
              fill=(30, 30, 30))
    d.rectangle([x + 8, y + 6, x + 96, y + 26], fill=(22, 22, 22))
    d.text((x + 13, y + 9), "BRU 0\u20133 LIV", font=F(SANS_B, 12),
           fill=(255, 255, 255))

def art_rocket(d, x, y, w, h):
    """Night launch: rocket climbing past stars, Earth curve below."""
    d.rectangle([x, y, x + w, y + h], fill=(14, 20, 44))
    for sx, sy, sr in ((x + 20, y + 16, 2), (x + 60, y + 34, 1),
                       (x + w - 30, y + 14, 2), (x + w - 70, y + 40, 1),
                       (x + 40, y + 58, 1), (x + w - 110, y + 66, 2),
                       (x + w // 2, y + 12, 1)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 255, 255))
    # Earth curve at the bottom
    d.pieslice([x - w // 2, y + h - 26, x + w * 3 // 2, y + h + 90], 180, 360,
               fill=(64, 120, 168))
    d.pieslice([x - w // 2, y + h - 26, x + w * 3 // 2, y + h + 90], 180, 360,
               fill=None, outline=(120, 180, 220), width=2)
    # rocket, centre, nose up
    rx, ry = x + w // 2, y + 12
    d.polygon([(rx, ry), (rx - 12, ry + 22), (rx + 12, ry + 22)],
              fill=RED)
    d.rectangle([rx - 12, ry + 22, rx + 12, ry + 52], fill=(235, 235, 235))
    d.rectangle([rx - 12, ry + 40, rx + 12, ry + 48], fill=(24, 88, 160))
    d.polygon([(rx - 12, ry + 44), (rx - 24, ry + 56), (rx - 12, ry + 52)],
              fill=RED)
    d.polygon([(rx + 12, ry + 44), (rx + 24, ry + 56), (rx + 12, ry + 52)],
              fill=RED)
    d.polygon([(rx - 7, ry + 56), (rx, ry + 78), (rx + 7, ry + 56)],
              fill=ORANGE)
    d.polygon([(rx - 4, ry + 56), (rx, ry + 68), (rx + 4, ry + 56)],
              fill=GOLD)
    d.ellipse([rx - 5, ry + 26, rx + 5, ry + 36], fill=(146, 190, 220),
              outline=(40, 40, 40), width=1)
    d.text((x + 8, y + h - 18), "SHENZHOU-24", font=F(SANS_B, 11),
           fill=(255, 255, 255))

def art_gavel(d, x, y, w, h):
    """Courthouse columns and a judge's gavel."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 200))
    # pediment + columns
    d.polygon([(x + 12, y + 8), (x + w // 2, y + 26), (x + w - 12, y + 8)],
              fill=(150, 140, 120))
    for i in range(3):
        cx = x + 34 + i * (w - 68) // 2
        d.rectangle([cx - 9, y + 28, cx + 9, y + h - 30], fill=(245, 240, 228),
                    outline=(120, 110, 90), width=1)
        d.rectangle([cx - 13, y + 24, cx + 13, y + 30], fill=(200, 190, 168))
        d.rectangle([cx - 13, y + h - 34, cx + 13, y + h - 28],
                    fill=(200, 190, 168))
    d.rectangle([x + 12, y + h - 28, x + w - 12, y + h - 20],
                fill=(150, 140, 120))
    # gavel resting on its block, foreground right
    gx, gy = x + w - 62, y + h - 52
    d.rectangle([gx - 6, gy + 14, gx + 34, gy + 22], fill=(120, 84, 40))
    d.line([(gx, gy + 6), (gx + 30, gy - 12)], fill=(120, 84, 40), width=5)
    d.rectangle([gx + 24, gy - 20, gx + 40, gy - 2], fill=(90, 60, 30))
    d.text((x + 10, y + h - 18), "10 OF 12 COUNTS", font=F(SANS_B, 11),
           fill=RED)

def art_tariffs(d, x, y, w, h):
    """Stacked shipping containers under a giant % sign."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 236))
    # ship hull at the bottom
    d.polygon([(x + 8, y + h - 22), (x + w - 8, y + h - 22),
               (x + w - 30, y + h - 6), (x + 30, y + h - 6)],
              fill=(38, 44, 52))
    # container stacks
    cols = [(178, 34, 34), (24, 88, 160), (214, 164, 32), (34, 139, 64)]
    for row in range(2):
        for i in range(3):
            cx = x + 14 + i * 56
            cy = y + h - 66 + row * 0 if row == 0 else y + h - 44
            d.rectangle([cx, cy, cx + 52, cy + 20], fill=cols[(i + row) % 4],
                        outline=(40, 40, 40), width=1)
            for vx in range(1, 5):
                d.line([(cx + vx * 10, cy), (cx + vx * 10, cy + 20)],
                       fill=(0, 0, 0), width=1)
    # big % sign, top right
    d.text((x + w - 74, y + 2), "%", font=F(SANS_B, 44), fill=RED)
    d.text((x + 10, y + 8), "NEW TARIFFS", font=F(SANS_B, 12), fill=NAVY)

def art_carbon(d, x, y, w, h):
    """Solar panels under palms: Indonesia's 12Mt carbon deal."""
    d.rectangle([x, y, x + w, y + h], fill=(200, 228, 240))
    d.ellipse([x + w - 52, y + 8, x + w - 12, y + 48], fill=GOLD)
    # palm trees, left and right
    for px, flip in ((x + 26, 1), (x + w - 26, -1)):
        d.line([(px, y + h - 30), (px, y + 26)], fill=(120, 84, 40), width=5)
        for k in range(4):
            ang = (-30 - k * 30) if flip == 1 else (210 + k * 30)
            ex = px + 26 * flip * math.cos(math.radians(ang + 90))
            ey = y + 30 + 14 * math.sin(math.radians(ang + 90))
            d.line([(px, y + 28), (ex, ey)], fill=GREEN, width=4)
    # solar panel rows, centre bottom
    for i in range(2):
        px = x + w // 2 - 52 + i * 56
        d.polygon([(px, y + h - 34), (px + 46, y + h - 34),
                   (px + 40, y + h - 14), (px - 6, y + h - 14)],
                  fill=(24, 48, 88), outline=(150, 180, 210), width=2)
        d.line([(px + 23, y + h - 34), (px + 17, y + h - 14)],
               fill=(150, 180, 210), width=1)
    d.text((x + 8, y + 6), "12 Mt CO\u2082", font=F(SANS_B, 13), fill=TEAL)

ART = {"mines": art_mines, "parade": art_parade, "airfield": art_airfield,
       "nvdadip": art_nvdadip, "cop31": art_cop31, "tower": art_tower,
       "football": art_football, "rocket": art_rocket, "gavel": art_gavel,
       "tariffs": art_tariffs, "carbon": art_carbon}

# ---------------------------------------------------------------- mini icons
def mini_icon(d, x, y, kind):
    """14x14 topic icon drawn at the head of an index row."""
    s = 14
    if kind == "flag":
        for i, c in enumerate([(178, 34, 34), (255, 255, 255), (24, 48, 88)]):
            d.rectangle([x, y + i * s // 3, x + s, y + (i + 1) * s // 3],
                        fill=c)
        d.rectangle([x, y, x + s, y + s], outline=(40, 40, 40), width=1)
    elif kind == "ball":
        d.ellipse([x, y, x + s, y + s], fill=(255, 255, 255),
                  outline=(40, 40, 40), width=1)
        d.polygon([(x + 7, y + 4), (x + 10, y + 7), (x + 7, y + 10),
                   (x + 4, y + 7)], fill=(30, 30, 30))
    elif kind == "rocket":
        d.polygon([(x + 7, y), (x + 11, y + 9), (x + 3, y + 9)], fill=RED)
        d.polygon([(x + 5, y + 9), (x + 7, y + 14), (x + 9, y + 9)],
                  fill=ORANGE)
    elif kind == "gavel":
        d.line([(x + 2, y + 11), (x + 11, y + 3)], fill=(120, 84, 40), width=3)
        d.rectangle([x + 8, y, x + 13, y + 5], fill=(90, 60, 30))
    elif kind == "chart":
        for i, bh in enumerate((5, 9, 13)):
            d.rectangle([x + 1 + i * 5, y + s - bh, x + 4 + i * 5, y + s],
                        fill=(24, 88, 160))
    elif kind == "globe":
        d.ellipse([x, y, x + s, y + s], fill=(64, 120, 168))
        d.ellipse([x + 2, y + 3, x + 7, y + 7], fill=GREEN)
        d.ellipse([x + 8, y + 8, x + 12, y + 12], fill=GREEN)
    elif kind == "plane":
        d.polygon([(x + 1, y + 7), (x + 13, y + 7), (x + 7, y + 3),
                   (x + 7, y + 11)], fill=(60, 60, 60))
        d.polygon([(x + 5, y + 7), (x + 9, y + 7), (x + 7, y + 12)],
                  fill=(90, 90, 90))
    elif kind == "bolt":
        d.polygon([(x + 9, y), (x + 4, y + 8), (x + 7, y + 8),
                   (x + 5, y + 14), (x + 11, y + 6), (x + 8, y + 6)],
                  fill=GOLD)
    elif kind == "storm":
        d.ellipse([x + 1, y + 2, x + 9, y + 8], fill=(120, 130, 145))
        d.ellipse([x + 6, y + 1, x + 13, y + 8], fill=(150, 160, 175))
        for lx in (x + 3, x + 7, x + 11):
            d.line([(lx, y + 9), (lx - 1, y + 13)], fill=(64, 120, 168),
                   width=2)

# ---------------------------------------------------------------- world map
CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80),
           (-85, 80), (-75, 72), (-60, 60), (-55, 47), (-70, 42),
           (-75, 35), (-80, 26), (-85, 20), (-90, 15), (-95, 17),
           (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60),
           (-155, 58), (-165, 60)],
    "SA": [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-35, -8),
           (-40, -20), (-48, -28), (-58, -35), (-65, -45), (-70, -52),
           (-73, -40), (-75, -25), (-80, -15), (-80, 0)],
    "AF": [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31),
           (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20),
           (30, -30), (20, -35), (15, -30), (12, -18), (9, -1), (9, 4),
           (-8, 4), (-17, 15)],
    "EU": [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57),
           (10, 59), (18, 56), (21, 55), (24, 59), (30, 60), (30, 70),
           (40, 68), (45, 66), (40, 60), (35, 55), (30, 50), (28, 45),
           (23, 40), (19, 42), (12, 44), (3, 42), (-2, 37), (-9, 37)],
    "AS": [(30, 70), (45, 68), (60, 69), (70, 72), (90, 75), (110, 76),
           (130, 72), (150, 70), (170, 67), (178, 65), (170, 60),
           (160, 55), (150, 60), (140, 50), (135, 43), (127, 40),
           (122, 38), (120, 30), (110, 20), (105, 10), (100, 8),
           (95, 15), (90, 22), (85, 20), (80, 13), (77, 8), (72, 20),
           (66, 25), (60, 25), (55, 26), (50, 29), (48, 30), (43, 28),
           (40, 35), (35, 36), (30, 36)],
    "OC": [(113, -22), (114, -30), (115, -35), (120, -34), (130, -32),
           (137, -35), (140, -38), (145, -38), (150, -37), (153, -27),
           (150, -22), (146, -19), (142, -11), (136, -12), (130, -13),
           (126, -14), (122, -17), (118, -20)],
}

def draw_map(d, x, y, w, h, dots):
    d.rectangle([x, y, x + w, y + h], fill=(196, 220, 232))
    def proj(lon, lat):
        px = x + (lon + 180) / 360 * w
        py = y + (85 - lat) / 140 * h
        return (px, py)
    for pts in CONTINENTS.values():
        d.polygon([proj(lon, lat) for lon, lat in pts], fill=(214, 196, 150),
                  outline=(150, 132, 96))
    for lon, lat in dots:
        px, py = proj(lon, lat)
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED,
                  outline=(255, 255, 255), width=2)

# ---------------------------------------------------------------- render
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.text((W // 2, 8), "THE WORLD IN ONE IMAGE",
           font=F(SERIF, 22), fill=INK, anchor="ma")
    d.line([(24, 40), (W - 24, 40)], fill=RULE, width=2)
    d.text((W // 2, 46), "THURSDAY, 26 NOVEMBER 2026",
           font=F(SERIF, 34), fill=INK, anchor="ma")
    d.line([(24, 88), (W - 24, 88)], fill=INK, width=3)

    # ---- red deck (serif; no serif-italic font on this box, so regular)
    d.text((W // 2, 94), DECK, font=F(SERIF_R, 15), fill=RED, anchor="ma")

    # ---- number strip: 7 mini stats
    ny, nh = 116, 38
    gap = 8
    bw = (W - 48 - 6 * gap) // 7
    for i, (num, label) in enumerate(NUMBERS):
        bx = 24 + i * (bw + gap)
        d.rectangle([bx, ny, bx + bw, ny + nh], fill=(238, 232, 218),
                    outline=RULE, width=1)
        d.text((bx + bw // 2, ny + 3), num, font=F(SANS_B, 16), fill=RED,
               anchor="ma")
        d.text((bx + bw // 2, ny + 23), label, font=F(SANS_B, 8),
               fill=MUTED, anchor="ma")

    # ---- region tabs
    ty = 162
    tx = 24
    tab_font = F(SANS_B, 11)
    for name, colour in REGIONS:
        tw = d.textlength(name, font=tab_font) + 20
        d.rounded_rectangle([tx, ty, tx + tw, ty + 20], radius=4, fill=colour)
        d.text((tx + tw // 2, ty + 4), name, font=tab_font,
               fill=(255, 255, 255), anchor="ma")
        tx += tw + 8

    # ---- 3 large leads
    col_w = (W - 48 - 2 * 14) // 3   # 316
    xs = [24, 24 + col_w + 14, 24 + 2 * (col_w + 14)]
    ly = 192
    img_h = 106
    for i, (kicker, head, body, art, _ll) in enumerate(LEADS):
        x = xs[i]
        ART[art](d, x, ly, col_w, img_h)
        yy = ly + img_h + 8
        d.text((x, yy), kicker, font=F(SANS_B, 12), fill=RED)
        yy += 19
        yy = text_block(d, x, yy, head, F(SERIF, 20), col_w, 23,
                        max_lines=2)
        text_block(d, x, yy + 3, body, F(SANS, 12), col_w, 14, max_lines=2)
        d.line([(x, ly - 6), (x + col_w, ly - 6)], fill=RULE, width=1)

    # ---- 2 rows of 4 cards
    ccol = (W - 48 - 3 * 12) // 4    # 235
    cxs = [24 + i * (ccol + 12) for i in range(4)]
    row_ys = [404, 562]
    card_img_h = 62
    for r in range(2):
        cy = row_ys[r]
        for i in range(4):
            kicker, head, body, art, _ll = CARDS[r * 4 + i]
            x = cxs[i]
            ART[art](d, x, cy, ccol, card_img_h)
            yy = cy + card_img_h + 6
            d.text((x, yy), kicker, font=F(SANS_B, 10), fill=RED)
            yy += 16
            yy = text_block(d, x, yy, head, F(SERIF, 15), ccol, 18,
                            max_lines=2)
            text_block(d, x, yy + 2, body, F(SANS, 11), ccol, 14,
                       max_lines=2)

    # ---- bottom: world map + 2-column index
    by = 724
    d.line([(24, by - 8), (W - 24, by - 8)], fill=INK, width=2)
    map_w, map_h = 330, 272
    dots = [ll for _k, _h, _b, _a, ll in LEADS + CARDS]
    draw_map(d, 24, by, map_w, map_h, dots)
    d.text((34, by + 6), "WHERE IT HAPPENED", font=F(SANS_B, 11),
           fill=(255, 255, 255), stroke_width=2, stroke_fill=(40, 60, 80))
    ix = 370
    d.text((ix, by), "ALSO TODAY  \u2014  16 MORE STORIES",
           font=F(SANS_B, 14), fill=RED)
    col2_x = ix + 320
    col_w2 = 300
    yy = by + 26
    for n, (item, kind) in enumerate(INDEX):
        col_x = ix if n < 8 else col2_x
        row = n % 8
        ry = by + 26 + row * 30
        mini_icon(d, col_x, ry + 1, kind)
        text_block(d, col_x + 20, ry, item, F(SANS, 11), col_w2 - 20, 13,
                   max_lines=2)

    # ---- footer
    d.text((W // 2, H - 16), SOURCES, font=F(SANS, 9), fill=MUTED,
           anchor="ma")

    img.save(OUT, "PNG")
    print("wrote", OUT, img.size)

if __name__ == "__main__":
    render()
