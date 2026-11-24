#!/usr/bin/env python3
"""News-24: sum up 24 November 2026 world news in one 1024x1024 image.

Fresh rewrite, authored in-session 24 Nov 2026 for make.fun bounty
news-image-20261124 ($100). Python + Pillow only, no network.
Run: python3 main.py  ->  writes entry.png (1024x1024, RGB).
All figures verified against sources on 24 Nov 2026; every story is
dated by the day the event happened, not the day it was reported.
"""
import math
from PIL import Image, ImageDraw, ImageFont

OUT = "entry.png"
SIZE = 1024
MARGIN = 26
WIDTH = SIZE - 2 * MARGIN

INK = (17, 24, 39)
MUTED = (107, 114, 128)
FAINT = (156, 163, 175)
PAPER = (255, 255, 255)
DARK = (17, 24, 39)
GOLD = (250, 204, 21)
LINE = (209, 213, 219)
SEA = (220, 233, 245)
LAND = (100, 116, 139)
RED = (220, 38, 38)

REGIONS = [
    ("NORTH AMERICA", (37, 99, 235)),
    ("EUROPE", (124, 58, 237)),
    ("MIDDLE EAST", (234, 88, 12)),
    ("ASIA", (22, 163, 74)),
    ("CULTURE", (219, 39, 119)),
    ("SPORT", (13, 148, 136)),
]

NUMBERS = [
    ("+6.51%", "Nasdaq jump, best day since April"),
    ("+31.5%", "Nvidia in one day, to $165.05"),
    ("$225m", "Hunger Games global opening"),
    ("$1.62bn", "India's package for Nepal"),
    ("397", "UNRWA staff killed since war began"),
    ("2,700", "Russian drones at Ukraine in a week"),
    ("$43.9bn", "CrowdStrike deal for Zscaler"),
    ("92,000", "People at COP31, ended with no deal"),
]

HEROES = [
    {
        "num": 1, "color": (37, 99, 235), "art": "markets",
        "kicker": "MARKETS  ·  NEW YORK  ·  MON 23 NOV",
        "head": "Wall Street roars back",
        "deck": "Nvidia brings back Jensen Huang — and the market posts its best day since April.",
        "body": "S&P 500 +4.73% to 7,237.17; Nasdaq +6.51% to 24,089.56; Dow +3.01% to "
                "49,595.31. Nvidia +31.5% to $165.05, the largest one-day market-value gain "
                "ever, after its board reinstated Huang as CEO. Gold +3.3% to $3,632; oil -4% to ~$80.",
        "src": "Sources: Yahoo Finance / Nasdaq / AP / Reuters",
    },
    {
        "num": 2, "color": (124, 58, 237), "art": "estonia",
        "kicker": "EUROPE  ·  TALLINN–MOSCOW  ·  MON 23 NOV",
        "head": "Russia warns Estonia of \u201copen war\u201d",
        "deck": "",
        "body": "Moscow accused Estonia of actions \u201con the verge of triggering open war\u201d "
                "after Tallinn said it will shut all land border crossings with Russia from "
                "1 December for at least six months. Estonia blames Russian security services "
                "for a staged arson attempt on a defence firm.",
        "src": "Source: Reuters",
    },
    {
        "num": 3, "color": (22, 163, 74), "art": "cop31",
        "kicker": "CLIMATE  ·  ANTALYA, T\u00dcRKIYE  ·  SUN 22 NOV",
        "head": "COP31 ends with no deal",
        "deck": "",
        "body": "The UN climate summit collapsed after running two days over — the longest COP "
                "on record. The final text named no fossil fuels, so the EU and island states "
                "refused it. 90 countries signed an electrification pledge; 47 backed a methane goal.",
        "src": "Sources: Reuters / NPR / Bloomberg",
    },
]

MEDIUM = [
    {
        "num": 4, "color": (234, 88, 12), "art": "gaza",
        "kicker": "MIDDLE EAST · JABALIA",
        "head": "Strike kills UN worker in Gaza",
        "body": "An Israeli airstrike killed UNRWA worker Adel Al-Helo in Jabalia; "
                "three others were wounded.",
        "src": "Reuters / UNRWA",
    },
    {
        "num": 5, "color": (37, 99, 235), "art": "drone",
        "kicker": "AMERICAS · SINALOA",
        "head": "US drone helped catch \u201cEl Chapo Isidro\u201d",
        "body": "A US drone helped track FBI fugitive Fausto Isidro Meza Flores, "
                "captured in Guasave. At least 20 killed.",
        "src": "AP / Reuters / NPR",
    },
    {
        "num": 6, "color": (22, 163, 74), "art": "nepal",
        "kicker": "ASIA · NEW DELHI",
        "head": "India gives Nepal $1.62bn",
        "body": "India pledged $1.62bn — a $377m grant plus a $1.24bn energy credit line — to rebuild "
                "Nepal after August floods killed ~1,500 people.",
        "src": "Reuters / AP / Al Jazeera",
    },
    {
        "num": 7, "color": (124, 58, 237), "art": "ukraine",
        "kicker": "EUROPE · KYIV–BRUSSELS",
        "head": "New strikes feared as EU unveils 22nd sanctions",
        "body": "Zelenskyy warned of new Russian strikes after ~2,700 drones, 1,460 bombs "
                "and 165 missiles in a week.",
        "src": "Reuters / Euronews",
    },
    {
        "num": 8, "color": (219, 39, 119), "art": "hunger",
        "kicker": "CULTURE · WORLDWIDE · 20–22 NOV",
        "head": "Hunger Games reaps $225m",
        "body": "\u201cSunrise on the Reaping\u201d opened to $225m worldwide — $120m in North America, "
                "$105m overseas — one of six $100m+ debuts of 2026.",
        "src": "Screen Daily / Variety",
    },
    {
        "num": 9, "color": (37, 99, 235), "art": "puzzle",
        "kicker": "TECH · USA",
        "head": "CrowdStrike buys Zscaler for $43.9bn",
        "body": "CrowdStrike agreed to buy cloud-security rival Zscaler in an all-stock deal worth "
                "about $43.9bn. Zscaler +17.7%; CrowdStrike -8.9%.",
        "src": "Benzinga / Barron's",
    },
    {
        "num": 10, "color": (13, 148, 136), "art": "football",
        "kicker": "SPORT · LONDON",
        "head": "Brentford 4–0 Everton",
        "body": "Brentford thrashed Everton 4–0 at home in the Premier League — 2–0 by half-time — "
                "on Monday night, Matchday 11.",
        "src": "Sportradar",
    },
    {
        "num": 11, "color": (37, 99, 235), "art": "spacex",
        "kicker": "TECH · USA · PRICED FRI 20 NOV",
        "head": "SpaceX prices record $44bn GPU debt",
        "body": "Apollo and Goldman Sachs priced about $44bn in notes to fund Nvidia Vera Rubin chips "
                "for SpaceX — the largest AI chip financing ever.",
        "src": "Apollo / Goldman Sachs",
    },
    {
        "num": 12, "color": (220, 38, 38), "art": "carriers",
        "kicker": "USA · WASHINGTON · SUN 22 NOV",
        "head": "Trump \u201cinclined\u201d to strike Iran after New Year",
        "body": "Trump told Fox News he is inclined to resume major strikes on Iran after the New Year "
                "if indirect nuclear talks fail. Two US carrier groups are in the Arabian Sea.",
        "src": "Fox News / AP",
    },
    {
        "num": 13, "color": (124, 58, 237), "art": "schools",
        "kicker": "EUROPE · GERMANY & DENMARK",
        "head": "Bomb threats hit hundreds of schools",
        "body": "Hundreds of schools in Germany and Denmark received emailed bomb threats on Monday. "
                "Police said there was no real danger.",
        "src": "The Insight International",
    },
]

BRIEFS = [
    ("14", "Delta fixes Sunday outage — Delta Air Lines fixed the system outage that disrupted "
           "flights on Sunday; its shares rose about 5.4% on Monday. (FirstFeed)"),
    ("15", "Gaza students start studies in Ireland — Students from Gaza began their studies in "
           "Ireland on Tuesday after winning a visa battle. (Arab News)"),
    ("16", "Trump pauses explosives detonation — President Trump paused a planned detonation of "
           "degraded explosives, officials said. (AFP)"),
]

# lat, lon, label; dx/dy are pin offsets (px) so neighbours never cover each other.
PINS = [
    (40.7, -74.0, "New York", 0, -9),
    (59.4, 24.7, "Tallinn", 0, -9),
    (36.9, 30.7, "Antalya", 0, 10),
    (31.5, 34.5, "Jabalia", 0, 10),
    (25.6, -108.5, "Guasave", -8, 8),
    (28.6, 77.2, "New Delhi", 0, -10),
    (50.5, 30.5, "Kyiv", 10, -8),
    (34.0, -118.2, "Los Angeles", -10, -8),
    (30.3, -97.7, "Austin", 0, 10),
    (51.5, -0.3, "London", 10, -9),
    (33.9, -118.3, "Hawthorne", 8, 9),
    (24.0, 62.0, "Arabian Sea", 0, 10),
    (52.5, 13.4, "Berlin", -10, 8),
    (33.7, -84.4, "Atlanta", -13, 10),
    (53.3, -6.3, "Dublin", -12, 8),
    (38.9, -77.0, "Washington", 12, -10),
]

KEPT = ("COP31 close (~34h, Sun 22 Nov) · Trump Fox interview (~24h) · El Chapo Isidro "
        "capture (disclosed Mon 23 Nov) · Hunger Games weekend (reported Mon) · SpaceX debt "
        "(priced Fri 20 Nov, reported Mon)")
EXCLUDED = ("GTA VI $3.79bn day-one (20 Nov) · Wembanyama 50 pts (21 Nov) · NFL Week 11 "
            "(22 Nov) · Skubal \u2192 Mets $450m (22 Nov) · Tajikistan quits ICC (20 Nov) · "
            "UN Hormuz briefing (13 Nov) · BepiColombo at Mercury (21 Nov) · Claude / Riemann "
            "proof (21 Nov) · Newsom AI powers (18 Nov) · OpenAI model delayed (21 Nov) · "
            "Trump \u201cvery traumatic\u201d warning (Feb) · Danish ghetto-law ruling (date "
            "unverified) · AFCON court ruling (date unverified)")

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_B = FONT_DIR + "/dejavu/DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "/dejavu/DejaVuSerif.ttf"
SERIF_I = FONT_DIR + "/liberation/LiberationSerif-Italic.ttf"
SANS = FONT_DIR + "/dejavu/DejaVuSans.ttf"
SANS_B = FONT_DIR + "/dejavu/DejaVuSans-Bold.ttf"

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def fit_font(path, text, max_w, start, minimum=10):
    size = start
    while size > minimum and font(path, size).getlength(text) > max_w:
        size -= 1
    return font(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill, leading=None, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    step = leading or int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def text_h(draw, text, fnt, max_w, leading=None, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    return len(lines) * (leading or int(fnt.size * 1.28))


def card(draw, x, y, w, h, accent=None):
    draw.rectangle([x, y, x + w, y + h], fill=PAPER, outline=LINE, width=1)
    if accent:
        draw.rectangle([x, y, x + 4, y + h], fill=accent)


def kicker_line(draw, x, y, num, color, text, fnt):
    badge = str(num)
    bw = draw.textlength(badge, font=fnt) + 10
    draw.rounded_rectangle([x, y - 1, x + bw, y + 13], radius=6, fill=color)
    draw.text((x + 5, y), badge, font=fnt, fill=(255, 255, 255))
    draw.text((x + bw + 6, y), text, font=fnt, fill=color)
    return y + 15


# ---------------------------------------------------------------- illustrations
# Flat-vector procedural art, no gradients, no text inside the art.
# Every illustration draws inside box (x, y, w, h) on its own soft background.

def art_bg(draw, x, y, w, h, color):
    draw.rectangle([x, y, x + w, y + h], fill=color)


def art_markets(d, x, y, w, h):
    art_bg(d, x, y, w, h, (219, 234, 254))
    for i in range(5):
        gx = x + 12 + i * (w - 24) // 4
        d.line([gx, y + 6, gx, y + h - 6], fill=(191, 219, 254), width=1)
    pts = [(x + 8, y + h - 14), (x + w * 0.3, y + h * 0.55),
           (x + w * 0.52, y + h * 0.62), (x + w * 0.72, y + h * 0.3),
           (x + w - 10, y + 12)]
    d.line(pts, fill=(22, 163, 74), width=5, joint="curve")
    d.polygon([(pts[-1][0] - 12, pts[-1][1] + 2), (pts[-1][0] + 2, pts[-1][1] - 2),
               (pts[-1][0] - 2, pts[-1][1] + 12)], fill=(22, 163, 74))
    bx, by = x + w * 0.14, y + h * 0.52
    d.ellipse([bx, by, bx + w * 0.42, by + h * 0.3], fill=(17, 24, 39))
    d.polygon([(bx + w * 0.36, by + 2), (bx + w * 0.5, by - h * 0.16),
               (bx + w * 0.44, by + h * 0.1)], fill=(17, 24, 39))
    d.polygon([(bx + w * 0.05, by + 2), (bx - w * 0.04, by - h * 0.14),
               (bx + w * 0.1, by + h * 0.08)], fill=(17, 24, 39))
    for lx in (0.06, 0.2, 0.34):
        d.rectangle([bx + w * lx, by + h * 0.28, bx + w * lx + 5, by + h * 0.42], fill=(17, 24, 39))
    cx, cy = x + w - 34, y + 12
    d.rectangle([cx, cy, cx + 26, cy + 30], fill=(17, 24, 39))
    d.rectangle([cx + 6, cy + 6, cx + 20, cy + 24], fill=(34, 197, 94))
    for px in (cx - 5, cx + 26):
        for py in (cy + 5, cy + 14, cy + 23):
            d.rectangle([px, py, px + 5, py + 3], fill=(17, 24, 39))


def art_estonia(d, x, y, w, h):
    art_bg(d, x, y, w, h, (254, 226, 226))
    d.polygon([(x + 6, y + h * 0.3), (x + w * 0.4, y + 8), (x + w - 8, y + h * 0.42),
               (x + w * 0.7, y + h - 8), (x + 10, y + h * 0.75)], fill=(252, 165, 165))
    d.rectangle([x + 8, y + h * 0.52, x + w - 8, y + h * 0.62], fill=(255, 255, 255))
    for i in range(6):
        fx = x + 14 + i * (w - 28) // 5
        d.line([fx, y + h * 0.3, fx, y + h * 0.82], fill=(220, 38, 38), width=3)
    d.rectangle([x + 8, y + h * 0.42, x + w - 8, y + h * 0.48], fill=(220, 38, 38))
    tx, ty = x + w * 0.68, y + h * 0.12
    d.polygon([(tx, ty), (tx + 34, ty), (tx + 17, ty + 30)], fill=(250, 204, 21),
              outline=(17, 24, 39))
    d.text((tx + 13, ty + 6), "!", font=font(SANS_B, 18), fill=(17, 24, 39))


def art_cop31(d, x, y, w, h):
    art_bg(d, x, y, w, h, (220, 252, 231))
    cx, cy, r = x + w * 0.32, y + h * 0.42, min(w, h) * 0.32
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(59, 130, 246))
    d.ellipse([cx - r * 0.55, cy - r * 0.7, cx + r * 0.1, cy - r * 0.1], fill=(34, 197, 94))
    d.ellipse([cx - r * 0.1, cy + r * 0.15, cx + r * 0.6, cy + r * 0.75], fill=(34, 197, 94))
    d.line([(cx + r * 0.1, cy - r), (cx - r * 0.2, cy - r * 0.2),
            (cx + r * 0.3, cy + r * 0.1), (cx - r * 0.1, cy + r)],
           fill=(120, 53, 15), width=3)
    sx, sy = x + w * 0.78, y + h * 0.16
    d.ellipse([sx - 14, sy - 14, sx + 14, sy + 14], fill=(250, 204, 21))
    for a in range(0, 360, 45):
        rad = math.radians(a)
        d.line([sx + 18 * math.cos(rad), sy + 18 * math.sin(rad),
                sx + 26 * math.cos(rad), sy + 26 * math.sin(rad)],
               fill=(250, 204, 21), width=3)
    d.rectangle([x + w * 0.55, y + h * 0.72, x + w - 8, y + h * 0.8], fill=(120, 113, 108))
    d.rectangle([x + w * 0.6, y + h * 0.8, x + w * 0.63, y + h - 6], fill=(87, 83, 78))
    d.rectangle([x + w - 16, y + h * 0.8, x + w - 13, y + h - 6], fill=(87, 83, 78))


def art_gaza(d, x, y, w, h):
    art_bg(d, x, y, w, h, (219, 234, 254))
    wx, wy = x + w * 0.3, y + h * 0.45
    d.ellipse([wx - 26, wy - 8, wx + 26, wy + 22], outline=(120, 113, 108), width=4)
    d.rectangle([wx - 26, wy - 8, wx + 26, wy + 6], fill=(168, 162, 158))
    d.line([wx - 26, wy - h * 0.32, wx - 26, wy - 8], fill=(120, 113, 108), width=4)
    d.line([wx + 26, wy - h * 0.32, wx + 26, wy - 8], fill=(120, 113, 108), width=4)
    d.polygon([(wx - 32, wy - h * 0.32), (wx + 32, wy - h * 0.32),
               (wx, wy - h * 0.55)], fill=(185, 28, 28))
    px, py = x + w * 0.74, y + h * 0.22
    d.line([px, py, px, py + h * 0.6], fill=(100, 116, 139), width=3)
    d.rectangle([px + 2, py, px + 34, py + h * 0.28], fill=(37, 99, 235))
    d.ellipse([px + 8, py + 4, px + 16, py + 12], outline=(255, 255, 255), width=2)
    d.ellipse([px + 20, py + 7, px + 24, py + 11], fill=(255, 255, 255))


def art_drone(d, x, y, w, h):
    art_bg(d, x, y, w, h, (254, 243, 199))
    d.polygon([(x, y + h), (x + w * 0.35, y + h * 0.55), (x + w * 0.7, y + h * 0.8),
               (x + w, y + h * 0.6), (x + w, y + h), (x, y + h)], fill=(234, 88, 12))
    cx, cy = x + w * 0.5, y + h * 0.34
    d.ellipse([cx - 20, cy - 10, cx + 20, cy + 10], fill=(100, 116, 139))
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(220, 38, 38))
    for sx, sy in ((-30, -14), (30, -14), (-30, 14), (30, 14)):
        d.line([cx + sx, cy + sy, cx + sx * 0.55, cy + sy * 0.55], fill=(71, 85, 105), width=3)
        d.ellipse([cx + sx - 9, cy + sy - 4, cx + sx + 9, cy + sy + 4], fill=(51, 65, 85))
    d.line([cx - 4, cy + 10, cx - 4, cy + h * 0.28], fill=(71, 85, 105), width=2)
    d.ellipse([cx - 12, cy + h * 0.26, cx + 4, cy + h * 0.4], outline=(148, 163, 184), width=3)
    d.ellipse([cx + 4, cy + h * 0.26, cx + 20, cy + h * 0.4], outline=(148, 163, 184), width=3)


def art_nepal(d, x, y, w, h):
    art_bg(d, x, y, w, h, (219, 234, 254))
    d.polygon([(x + 4, y + h), (x + w * 0.3, y + h * 0.25), (x + w * 0.55, y + h)],
              fill=(100, 116, 139))
    d.polygon([(x + w * 0.18, y + h * 0.45), (x + w * 0.3, y + h * 0.25),
               (x + w * 0.42, y + h * 0.45)], fill=(255, 255, 255))
    d.polygon([(x + w * 0.45, y + h), (x + w * 0.68, y + h * 0.35),
               (x + w * 0.92, y + h)], fill=(71, 85, 105))
    d.polygon([(x + w * 0.6, y + h * 0.5), (x + w * 0.68, y + h * 0.35),
               (x + w * 0.77, y + h * 0.5)], fill=(255, 255, 255))
    d.line([x + w * 0.55, y + 8, x + w - 8, y + 8], fill=(250, 204, 21), width=4)
    d.line([x + w - 14, y + 8, x + w - 14, y + h * 0.7], fill=(250, 204, 21), width=4)
    d.line([x + w * 0.55, y + 8, x + w * 0.55, y + 26], fill=(17, 24, 39), width=2)
    d.rectangle([x + w * 0.5, y + h - 14, x + w * 0.58, y + h - 6], fill=(185, 28, 28))
    d.rectangle([x + w * 0.58, y + h - 14, x + w * 0.66, y + h - 6], fill=(220, 38, 38))


def art_ukraine(d, x, y, w, h):
    art_bg(d, x, y, w, h, (254, 243, 199))
    cx, cy = x + w * 0.5, y + h * 0.48
    top, mid, bot = cy - h * 0.32, cy + h * 0.05, cy + h * 0.38
    d.polygon([(cx - 26, top), (cx + 26, top), (cx + 26, mid),
               (cx, bot), (cx - 26, mid)], fill=(37, 99, 235))
    d.polygon([(cx - 26, top), (cx + 26, top), (cx + 26, mid - h * 0.1),
               (cx, mid + h * 0.12), (cx - 26, mid - h * 0.1)], fill=(250, 204, 21))
    for dx, dy in ((-32, -0.30), (30, -0.34), (0, 0.28)):
        dyy = cy + dy * h
        d.ellipse([cx + dx - 7, dyy - 4, cx + dx + 7, dyy + 4], fill=(17, 24, 39))
        d.line([cx + dx - 12, dyy, cx + dx + 12, dyy], fill=(17, 24, 39), width=2)


def art_hunger(d, x, y, w, h):
    art_bg(d, x, y, w, h, (254, 226, 226))
    cx, cy = x + w * 0.5, y + h * 0.5
    br = h * 0.42
    d.arc([cx - br, cy - br, cx + br, cy + br], 300, 60, fill=(185, 28, 28), width=4)
    d.line([cx + br * 0.7, cy - br * 0.85, cx + 30, cy - 34], fill=(185, 28, 28), width=2)
    d.polygon([(cx + 30, cy - 36), (cx + 38, cy - 32), (cx + 30, cy - 28)], fill=(17, 24, 39))
    d.line([cx - 26, cy, cx + 26, cy], fill=(100, 116, 139), width=2)
    fx, fy = x + w * 0.82, y + h * 0.72
    d.polygon([(fx - 10, fy + 8), (fx, fy - 14), (fx + 4, fy + 2), (fx + 12, fy - 8),
               (fx + 10, fy + 8)], fill=(234, 88, 12))
    d.polygon([(fx - 5, fy + 8), (fx, fy - 4), (fx + 6, fy + 8)], fill=(250, 204, 21))


def art_puzzle(d, x, y, w, h):
    art_bg(d, x, y, w, h, (237, 233, 254))
    cx, cy = x + w * 0.5, y + h * 0.5
    d.rounded_rectangle([cx - 34, cy - 18, cx - 2, cy + 14], radius=6, fill=(37, 99, 235))
    d.ellipse([cx - 10, cy - 18, cx + 2, cy - 6], fill=(37, 99, 235))
    d.rounded_rectangle([cx + 2, cy - 14, cx + 34, cy + 18], radius=6, fill=(124, 58, 237))
    d.ellipse([cx + 2, cy + 6, cx + 14, cy + 18], fill=(124, 58, 237))
    d.ellipse([cx - 22, cy - h * 0.42, cx + 10, cy - h * 0.24], outline=(100, 116, 139), width=3)
    d.line([cx - 22, cy - h * 0.33, cx + 10, cy - h * 0.33], fill=(255, 255, 255), width=2)


def art_football(d, x, y, w, h):
    art_bg(d, x, y, w, h, (220, 252, 231))
    gx, gy = x + w * 0.5, y + h * 0.38
    gh = h * 0.30
    d.rectangle([gx - 34, gy - gh, gx + 34, gy + gh], outline=(255, 255, 255), width=3)
    for i in range(-2, 3):
        d.line([gx + i * 13, gy - gh, gx + i * 13, gy + gh], fill=(255, 255, 255), width=1)
    d.line([gx - 34, gy, gx + 34, gy], fill=(255, 255, 255), width=1)
    bx, by = x + w * 0.24, y + h * 0.68
    br = max(7, h * 0.28)
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=(255, 255, 255), outline=(17, 24, 39))
    d.polygon([(bx - 5, by - 5), (bx + 5, by - 5), (bx + 6, by + 4), (bx, by + 8), (bx - 6, by + 4)],
              fill=(17, 24, 39))
    d.rectangle([x + w * 0.62, y + 4, x + w - 6, y + 4 + h * 0.55], fill=(17, 24, 39))
    d.text((x + w * 0.62 + 5, y + 5), "4–0", font=font(SANS_B, max(10, int(h * 0.4))),
           fill=(255, 255, 255))


def art_spacex(d, x, y, w, h):
    art_bg(d, x, y, w, h, (219, 234, 254))
    cx, cy = x + w * 0.32, y + h * 0.52
    d.polygon([(cx, cy - h * 0.42), (cx + 12, cy - 6), (cx + 10, cy + h * 0.3),
               (cx - 10, cy + h * 0.3), (cx - 12, cy - 6)], fill=(255, 255, 255),
              outline=(100, 116, 139))
    d.ellipse([cx - 5, cy - 16, cx + 5, cy - 6], fill=(59, 130, 246))
    d.polygon([(cx - 10, cy + h * 0.3), (cx - 20, cy + h * 0.45), (cx - 6, cy + h * 0.36)],
              fill=(234, 88, 12))
    d.polygon([(cx + 10, cy + h * 0.3), (cx + 20, cy + h * 0.45), (cx + 6, cy + h * 0.36)],
              fill=(234, 88, 12))
    d.polygon([(cx - 6, cy + h * 0.3), (cx, cy + h * 0.48), (cx + 6, cy + h * 0.3)],
              fill=(250, 204, 21))
    for i, (px, py) in enumerate(((0.62, 0.3), (0.72, 0.55), (0.82, 0.3))):
        sx, sy = x + w * px, y + h * py
        d.rectangle([sx - 12, sy - 10, sx + 12, sy + 10], fill=(34, 197, 94))
        d.rectangle([sx - 6, sy - 4, sx + 6, sy + 4], fill=(6, 95, 70))
    d.text((x + w * 0.6, y + h * 0.6), "$", font=font(SANS_B, max(12, int(h * 0.5))),
           fill=(22, 163, 74))


def art_carriers(d, x, y, w, h):
    art_bg(d, x, y, w, h, (219, 234, 254))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(59, 130, 246))
    for i in range(3):
        wx = x + 10 + i * w // 3
        d.arc([wx, y + h * 0.66, wx + 30, y + h * 0.82], 0, 180, fill=(255, 255, 255), width=2)
    for cx, cy in ((0.3, 0.52), (0.72, 0.58)):
        sx, sy = x + w * cx, y + h * cy
        d.polygon([(sx - 30, sy), (sx + 30, sy), (sx + 24, sy + 10), (sx - 24, sy + 10)],
                  fill=(100, 116, 139))
        d.rectangle([sx - 4, sy - 18, sx + 10, sy], fill=(71, 85, 105))
    d.line([x + 8, y + h * 0.3, x + w - 8, y + h * 0.24], fill=(220, 38, 38), width=2)
    for i in range(8):
        lx = x + 12 + i * (w - 24) // 7
        ly = y + h * 0.3 - (lx - x) * 0.06 / w * 100
        d.line([lx, ly, lx + 6, ly], fill=(220, 38, 38), width=2)


def art_schools(d, x, y, w, h):
    art_bg(d, x, y, w, h, (254, 243, 199))
    ex, ey = x + w * 0.3, y + h * 0.45
    eh = h * 0.3
    d.rectangle([ex - 26, ey - eh, ex + 26, ey + eh], fill=(255, 255, 255), outline=(100, 116, 139))
    d.polygon([(ex - 26, ey - eh), (ex, ey + 2), (ex + 26, ey - eh)], outline=(100, 116, 139))
    sx, sy = x + w * 0.72, y + h * 0.55
    sh = h * 0.28
    d.rectangle([sx - 22, sy - sh * 0.4, sx + 22, sy + sh], fill=(185, 28, 28))
    d.polygon([(sx - 22, sy - sh * 0.4), (sx, sy - sh), (sx + 22, sy - sh * 0.4)],
              fill=(220, 38, 38))
    d.line([sx + 16, sy - sh, sx + 16, sy - h * 0.42], fill=(100, 116, 139), width=2)
    d.polygon([(sx + 16, sy - h * 0.42), (sx + 30, sy - h * 0.36), (sx + 16, sy - h * 0.3)],
              fill=(250, 204, 21))
    d.line([x + w * 0.12, y + h * 0.78, x + w * 0.24, y + h * 0.88], fill=(22, 163, 74), width=4)
    d.line([x + w * 0.24, y + h * 0.88, x + w * 0.45, y + h * 0.62], fill=(22, 163, 74), width=4)


ART = {
    "markets": art_markets, "estonia": art_estonia, "cop31": art_cop31,
    "gaza": art_gaza, "drone": art_drone, "nepal": art_nepal,
    "ukraine": art_ukraine, "hunger": art_hunger, "puzzle": art_puzzle,
    "football": art_football, "spacex": art_spacex, "carriers": art_carriers,
    "schools": art_schools,
}


# ---------------------------------------------------------------- layout

def draw_masthead(d, y):
    title = "TUESDAY, 24 NOVEMBER 2026"
    fnt = fit_font(SERIF_B, title, WIDTH, 46)
    d.text((MARGIN, y), title, font=fnt, fill=INK)
    y += fnt.size + 8
    d.line([MARGIN, y, MARGIN + WIDTH, y], fill=INK, width=3)
    d.line([MARGIN, y + 4, MARGIN + WIDTH, y + 4], fill=INK, width=1)
    y += 10
    d.text((MARGIN, y), "THE WORLD IN ONE IMAGE  —  24 NOVEMBER 2026",
           font=font(SANS_B, 12), fill=MUTED)
    return y + 20


def draw_regions(d, y):
    seg_w = WIDTH / len(REGIONS)
    for i, (name, color) in enumerate(REGIONS):
        x = MARGIN + i * seg_w
        d.rectangle([x, y, x + seg_w - 2, y + 20], fill=color)
        fnt = font(SANS_B, 10)
        tw = d.textlength(name, font=fnt)
        if tw <= seg_w - 8:
            d.text((x + (seg_w - 2 - tw) / 2, y + 4), name, font=fnt, fill=(255, 255, 255))
    return y + 26


def draw_numbers(d, y):
    d.text((MARGIN, y), "THE DAY IN NUMBERS", font=font(SANS_B, 14), fill=INK)
    y += 20
    cell_w, cell_h = WIDTH / 4, 30
    for idx, (big, label) in enumerate(NUMBERS):
        row, col = divmod(idx, 4)
        x = MARGIN + col * cell_w
        cy = y + row * cell_h
        d.rectangle([x, cy, x + WIDTH / 4, cy + cell_h], fill=DARK)
        if col:
            d.line([x, cy + 5, x, cy + cell_h - 5], fill=(55, 65, 81), width=1)
        d.text((x + 8, cy + 2), big, font=font(SANS_B, 15), fill=GOLD)
        lab = label if len(label) <= 44 else label[:43] + "…"
        d.text((x + 8, cy + 19), lab, font=font(SANS, 8), fill=(209, 213, 219))
    return y + 2 * cell_h + 6


def draw_hero1(d, y, h):
    s = HEROES[0]
    x = MARGIN
    card(d, x, y, WIDTH, h)
    iw = 168
    ART[s["art"]](d, x + 1, y + 1, iw - 1, h - 2)
    tx = x + iw + 12
    tw = WIDTH - iw - 24
    yy = kicker_line(d, tx, y + 8, s["num"], s["color"], s["kicker"], font(SANS_B, 10))
    head_f = fit_font(SERIF_B, s["head"], tw, 30)
    d.text((tx, yy), s["head"], font=head_f, fill=INK)
    yy += head_f.size + 3
    yy = draw_wrapped(d, tx, yy, s["deck"], font(SERIF_I, 13), tw, MUTED, max_lines=1)
    yy = draw_wrapped(d, tx, yy + 2, s["body"], font(SANS, 12), tw, INK, max_lines=3)
    d.text((tx, y + h - 16), s["src"], font=font(SANS, 9), fill=MUTED)
    return y + h + 6


def draw_hero_side(d, x, y, w, h, s):
    card(d, x, y, w, h)
    iw = 108
    ART[s["art"]](d, x + 1, y + 1, iw - 1, h - 2)
    tx = x + iw + 9
    tw = w - iw - 18
    yy = kicker_line(d, tx, y + 7, s["num"], s["color"], s["kicker"], font(SANS_B, 8))
    head_f = fit_font(SERIF_B, s["head"], tw, 18)
    yy = draw_wrapped(d, tx, yy, s["head"], head_f, tw, INK, max_lines=2)
    yy = draw_wrapped(d, tx, yy + 2, s["body"], font(SANS, 10.5), tw, INK, max_lines=5)
    d.text((tx, y + h - 14), s["src"], font=font(SANS, 8), fill=MUTED)
    return y + h


def draw_medium(d, x, y, w, h, s):
    card(d, x, y, w, h, accent=s["color"])
    ART[s["art"]](d, x + 5, y + 5, w - 10, 30)
    yy = y + 39
    yy = kicker_line(d, x + 8, yy, s["num"], s["color"], s["kicker"], font(SANS_B, 7))
    head_f = fit_font(SANS_B, s["head"], w - 16, 11.5)
    yy = draw_wrapped(d, x + 8, yy, s["head"], head_f, w - 16, INK, max_lines=2)
    yy = draw_wrapped(d, x + 8, yy + 2, s["body"], font(SANS, 9), w - 16, INK, max_lines=3)
    d.text((x + 8, y + h - 12), "Sources: " + s["src"], font=font(SANS, 7.5), fill=MUTED)
    return y + h


def draw_map(d, y, h):
    d.text((MARGIN, y), "WHERE IT HAPPENED — 16 PLACES, NUMBERED AS THE STORIES",
           font=font(SANS_B, 11), fill=INK)
    y += 17
    x0, y0, mw, mh = MARGIN, y, WIDTH, h - 17
    d.rectangle([x0, y0, x0 + mw, y0 + mh], fill=SEA, outline=LINE)
    continents = [
        [(0.06, 0.18), (0.16, 0.10), (0.24, 0.16), (0.27, 0.30), (0.20, 0.48),
         (0.13, 0.44), (0.07, 0.34)],
        [(0.30, 0.42), (0.36, 0.34), (0.44, 0.38), (0.45, 0.52), (0.38, 0.62),
         (0.31, 0.55)],
        [(0.46, 0.12), (0.56, 0.06), (0.68, 0.10), (0.72, 0.22), (0.64, 0.30),
         (0.55, 0.34), (0.48, 0.26)],
        [(0.70, 0.28), (0.78, 0.24), (0.84, 0.32), (0.82, 0.46), (0.74, 0.44)],
        [(0.84, 0.62), (0.92, 0.58), (0.96, 0.70), (0.90, 0.80), (0.84, 0.72)],
    ]
    for poly in continents:
        pts = [(x0 + px * mw, y0 + py * mh) for px, py in poly]
        d.polygon(pts, fill=LAND)
    for i, (lat, lon, _label, dx, dy) in enumerate(PINS, start=1):
        px = x0 + (lon + 180) / 360 * mw
        py = y0 + (90 - lat) / 180 * mh
        qx, qy = px + dx, py + dy
        if dx or dy:
            d.line([px, py, qx, qy], fill=RED, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        r = 8
        d.ellipse([qx - r, qy - r, qx + r, qy + r], fill=RED, outline=(255, 255, 255), width=1)
        num = str(i)
        nw = d.textlength(num, font=font(SANS_B, 9))
        d.text((qx - nw / 2, qy - 6), num, font=font(SANS_B, 9), fill=(255, 255, 255))
    return y0 + mh + 5


def draw_briefs(d, y):
    for num, text in BRIEFS:
        fnt = font(SANS, 11)
        d.text((MARGIN, y), num + ".", font=font(SANS_B, 11), fill=RED)
        draw_wrapped(d, MARGIN + 22, y, text, fnt, WIDTH - 22, INK, max_lines=1)
        y += 15
    return y + 2


def draw_datecheck(d, y):
    box_h = 74
    d.rectangle([MARGIN, y, MARGIN + WIDTH, y + box_h], outline=RED, width=2)
    d.text((MARGIN + 8, y + 5), "DATE CHECK — WHAT WAS LEFT OUT AND WHY",
           font=font(SANS_B, 10), fill=RED)
    yy = y + 20
    yy = draw_wrapped(d, MARGIN + 8, yy, "Kept but borderline (24–36h): " + KEPT,
                      font(SANS, 9), WIDTH - 16, INK, max_lines=2)
    yy = draw_wrapped(d, MARGIN + 8, yy + 1, "Excluded (36h+ or date unverified): " + EXCLUDED,
                      font(SANS, 9), WIDTH - 16, MUTED, max_lines=2)
    return y + box_h + 5


def build():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)
    y = 14
    y = draw_masthead(d, y)
    y = draw_regions(d, y)
    y = draw_numbers(d, y)
    y = draw_hero1(d, y, 128)
    hw = (WIDTH - 8) // 2
    draw_hero_side(d, MARGIN, y, hw, 136, HEROES[1])
    draw_hero_side(d, MARGIN + hw + 8, y, hw, 136, HEROES[2])
    y += 136 + 6
    mw = (WIDTH - 4 * 8) // 5
    mh = 128
    for row in range(2):
        for col in range(5):
            s = MEDIUM[row * 5 + col]
            draw_medium(d, MARGIN + col * (mw + 8), y, mw, mh, s)
        y += mh + 6
    y = draw_map(d, y, 94)
    y = draw_briefs(d, y)
    y = draw_datecheck(d, y)
    d.text((MARGIN, y), "Sources are listed under each story. Figures verified against sources "
           "on 24 Nov 2026. Events are dated by the day they happened, not the day reported.",
           font=font(SANS, 8.5), fill=MUTED)
    d.text((MARGIN, y + 12), "Built with Python + Pillow · News-24",
           font=font(SANS, 8.5), fill=FAINT)
    print("final y =", y + 24, "of", SIZE)
    img.save(OUT, optimize=True)
    print("saved", OUT, img.size)


if __name__ == "__main__":
    build()
