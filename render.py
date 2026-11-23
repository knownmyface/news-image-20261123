#!/usr/bin/env python3
"""news-image-20261123: front page for Monday 23 November 2026.

Sixty stories, every one checked against a report published on 23 Nov 2026
(or first reported that day). Named source per story; [CLAIM] marks an
unverified claim, [FORECAST] marks something not yet happened. All art is
drawn in code with PIL -- no photographs. Renders are byte-identical.
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os
import sys

PAGE_W, PAGE_H = 1024, 1024
PAPER = (248, 244, 233)
INK = (26, 26, 26)
RED = (176, 30, 40)
NAVY = (31, 78, 121)
TEAL = (14, 107, 107)
MUTE = (110, 108, 100)
PALE = (232, 226, 210)
NIGHT = (16, 28, 54)
GOLD = (184, 134, 11)
MARGIN = 16

FONT_DIR = "/usr/share/fonts/truetype"


def load_font(fname, size):
    for sub in ("dejavu", "noto", "liberation"):
        path = os.path.join(FONT_DIR, sub, fname)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def serif_b(size):
    return load_font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return load_font("DejaVuSerif.ttf", size)


def serif_i(size):
    return load_font("NotoSerif-Italic.ttf", size)


def sans(size):
    return load_font("DejaVuSans.ttf", size)


def sans_b(size):
    return load_font("DejaVuSans-Bold.ttf", size)


def fit_text(text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if fnt.getlength(trial) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def put_lines(draw, x, y, lines, fnt, fill=INK, leading=None, centre=None):
    """Draw lines top to bottom; returns the y just below the last line."""
    if leading is None:
        leading = fnt.size + 3
    for i, line in enumerate(lines):
        xx = x
        if centre is not None:
            xx = x + (centre - fnt.getlength(line)) // 2
        draw.text((xx, y + i * leading), line, font=fnt, fill=fill)
    return y + len(lines) * leading


# ------------------------------------------------------------------ stories
# Three big leads. `pin` is (latitude, longitude, map label).
BIG_THREE = [
    {
        "n": 1,
        "kicker": "CLIMATE  |  ANTALYA, TURKEY",
        "head": "COP31 fallout: 1.5°C now 'inevitable'",
        "body": (
            "UN chief Guterres calls the collapse 'deeply disappointing' and "
            "warns overshoot of 1.5°C is now inevitable. 90+ nations salvage "
            "an electrification pledge; the rest carries to COP32 in 2027."
        ),
        "src": "UN / Reuters / CNN",
        "region": "Europe",
        "pin": (36.9, 30.7, "Antalya"),
    },
    {
        "n": 2,
        "kicker": "WAR  |  UKRAINE",
        "head": "153 drones in one night",
        "body": (
            "Russia launches 153 drones from 18:00 Sun; Ukraine's Air Force "
            "says 134 are downed or jammed by 08:00. A block falls in Dymer, "
            "north of Kyiv: 11 killed — a boy, 7, is pulled alive after 14 hours."
        ),
        "src": "Ukrainian Air Force / BBC",
        "region": "Europe",
        "pin": (50.5, 30.3, "Kyiv"),
    },
    {
        "n": 3,
        "kicker": "MARKETS  |  NEW YORK",
        "head": "Wall Street bounces back",
        "body": (
            "Futures jump after the worst week since 2020: Nasdaq +3%, S&P "
            "+2.7%. Nvidia gains 9.4% pre-market after Friday's 14% plunge; "
            "Bitcoin climbs back above $61,000 from a $55,000 low."
        ),
        "src": "Reuters / CoinDesk",
        "region": "Markets & Tech",
        "pin": (40.7, -74.0, "New York"),
    },
]

# Ten more, in brief. `icon` picks a small flat pictogram.
BRIEFS = [
    {
        "n": 4, "icon": "ballot", "head": "Democrats take 258 House seats",
        "body": "Largest House majority this century.",
        "src": "AP", "region": "Americas",
        "pin": (38.5, -77.5, "Washington"),
    },
    {
        "n": 5, "icon": "flame", "head": "Java factory fire: 24 dead",
        "body": "Search resumes Mon; ~30 still missing.",
        "src": "Reuters", "region": "Asia-Pacific",
        "pin": (-6.2, 106.2, "Java"),
    },
    {
        "n": 6, "icon": "cricket", "head": "NZ draw Wellington Test",
        "body": "239/5; Mitchell 49*, Phillips 26*.",
        "src": "AP", "region": "Sport",
        "pin": (-41.3, 174.8, "Wellington"),
    },
    {
        "n": 7, "icon": "dove", "head": "Ukraine ready for 4-way talks",
        "body": "Zelenskyy: meet before Christmas.",
        "src": "h.ua", "region": "Europe",
        "pin": (50.8, 4.4, "Brussels"),
    },
    {
        "n": 8, "icon": "toxic", "head": "Gaza 'toxic wasteland': Oxfam",
        "body": "Contamination across 99% of Gaza.",
        "src": "Guardian", "region": "Middle East",
        "pin": (31.5, 34.5, "Gaza"),
    },
    {
        "n": 9, "icon": "castle", "head": "Shuri Castle reopens Monday",
        "body": "Seven years after the 2019 fire.",
        "src": "AP", "region": "Asia-Pacific",
        "pin": (26.2, 127.7, "Okinawa"),
    },
    {
        "n": 10, "icon": "heart", "head": "Pig kidney: one year on",
        "body": "NH woman, 58, sets survival record.",
        "src": "NYT", "region": "Americas",
        "pin": (43.8, -71.0, "New Hampshire"),
    },
    {
        "n": 11, "icon": "oil", "head": "Nigeria–China $23bn refineries",
        "body": "Three plants: Bayelsa, Kogi, Lagos.",
        "src": "BBC", "region": "Africa",
        "pin": (6.5, 3.4, "Lagos"),
    },
    {
        "n": 12, "icon": "chip", "head": "California AG sues OpenAI",
        "body": "Nvidia faces SEC + state probes.",
        "src": "XTB", "region": "Markets & Tech",
        "pin": (37.8, -122.4, "San Francisco"),
    },
    {
        "n": 13, "icon": "alert", "head": "35 killed in Nigeria reprisals",
        "body": "Retaliatory attacks in central-west.",
        "src": "Wire reports", "region": "Africa",
        "pin": (10.5, 10.5, "Nigeria"),
    },
]

# The other 47 stories: (headline, source, region). Keep each line short.
REST = [
    ("Zelenskyy: 2,700 drones hit Ukraine in a week", "Zelenskyy", "Europe"),
    ("Russia says it downed 192 Ukrainian drones", "Interfax", "Europe"),
    ("Novoshakhtinsk refinery fire after strike [CLAIM]", "Media reports", "Europe"),
    ("Ukraine drone units hit record 2,552 targets", "UNITED24", "Europe"),
    ("Dymer: woman, 79, pulled alive from rubble", "BBC", "Europe"),
    ("COP31 leftovers carry to COP32, Addis 2027", "UNFCCC", "Europe"),
    ("UNEP: adaptation needs $305bn a year by 2035", "RMetS", "Europe"),
    ("UNEP: current pledges point to 2.6°C warming", "RMetS", "Europe"),
    ("German PMI 55.0, highest since March 2022", "Reuters", "Europe"),
    ("UK PMI 52.3; Q4 growth seen at 0.6% [FORECAST]", "Reuters", "Europe"),
    ("UK chancellor: benefits bill must fall", "BBC", "Europe"),
    ("Lib Dems elect Josh Babarinde president", "PAN", "Europe"),
    ("France: students call fresh blockades Monday", "GazetAI", "Europe"),
    ("Paris protest turns violent; tear gas fired", "Wire reports", "Europe"),
    ("Choose France summit: nearly €15bn pledged", "sumi.news", "Europe"),
    ("Portugal joins Europe's tech-investment top 10", "sumi.news", "Europe"),
    ("Gaza death toll reaches 74,742", "Health ministry", "Middle East"),
    ("Two killed in strike on al-Mawasi at dawn", "ABNA", "Middle East"),
    ("Turkey: Israel blocks Gaza housing units", "ABNA", "Middle East"),
    ("Meningitis cases rise in Gaza, water ruined", "ABNA", "Middle East"),
    ("Houthis claim Saudi refinery hit; Riyadh hits back", "OneTurn", "Middle East"),
    ("Iran: US blockade must end before Hormuz talks", "GazetAI", "Middle East"),
    ("Iran brands UK Navy and RAF terrorist groups", "GazetAI", "Middle East"),
    ("IDF warns Netanyahu on multifront Iran war", "Times Union", "Middle East"),
    ("Lebanon army seizes trio with 264kg explosives", "Wire reports", "Middle East"),
    ("Lula seeks dialogue among Russia, US, China", "Times Union", "Americas"),
    ("Congress leaves; funding deadline Dec 11", "WYO News", "Americas"),
    ("Khartoum drone strikes kill five children", "OneTurn", "Africa"),
    ("Libya: forces 'repelled threats' to Benghazi", "Libyan command", "Africa"),
    ("Dr Phumzile Mlambo-Ngcuka dies", "AllAfrica", "Africa"),
    ("China sets 2030 eldercare, childcare goals", "Standard Topic", "Asia-Pacific"),
    ("Xi: China will work with Arabs on Mideast peace", "GazetAI", "Asia-Pacific"),
    ("Kim receives envoys in person, first time", "Insight", "Asia-Pacific"),
    ("South Korea names new foreign ministers", "sumi.news", "Asia-Pacific"),
    ("Vietnam picks French-Korean rail group", "sumi.news", "Asia-Pacific"),
    ("Thai court halves royal-insult jail term", "sumi.news", "Asia-Pacific"),
    ("Taiwan warns Canada over China trade ties", "sumi.news", "Asia-Pacific"),
    ("India pledges $1.6bn to rebuild Nepal", "Insight", "Asia-Pacific"),
    ("Pakistan chairs SCO bank group 2026-27", "GazetAI", "Asia-Pacific"),
    ("Japan shut for holiday as Asia slides", "Reuters", "Asia-Pacific"),
    ("Seoul minister reiterates market support plans", "Reuters", "Asia-Pacific"),
    ("Taiwan shares fell 17% last week, worst since 1990", "political.org", "Markets & Tech"),
    ("Bitcoin: 7th straight weekly loss; ETFs -$669m Fri", "CoinDesk", "Markets & Tech"),
    ("Citi cuts Bitcoin 12-month view to $99,532", "Morningstar", "Markets & Tech"),
    ("Nvidia down 47.5% since Oct 6; $2.7tn gone", "Reuters", "Markets & Tech"),
    ("Skubal agrees record $450m Mets deal", "AP", "Sport"),
    ("Prabowo to name two VP candidates Monday", "Reuters", "Asia-Pacific"),
]

BIG_NUMBERS = [
    ("153", "drones overnight, 134 downed"),
    ("11", "killed in Dymer; boy, 7, alive"),
    ("0", "COP31 deal: none since 2000"),
    ("258", "House seats: Dems' biggest haul"),
    ("24", "dead in Java fire, ~30 missing"),
    ("$61,846", "Bitcoin Mon high, off $55k low"),
]

DAY_CLOCK = [
    ("00:00", "Cikande search resumes"),
    ("03:10", "Bitcoin $60,851"),
    ("05:15", "Nigeria: 35 killed"),
    ("06:00", "134 of 153 drones downed"),
    ("07:30", "German PMI hits 55.0"),
    ("10:17", "Gaza toll 74,742"),
    ("11:20", "Oxfam: Gaza toxic, 99%"),
    ("11:31", "Zelenskyy: 4-way talks"),
    ("13:13", "Bitcoin $61,286"),
]

WRONG_DAY = [
    "ICJ: Myanmar genocide ruling — Thu 19",
    "Shenzhen: Trump–Xi–Putin summit — Thu 19",
    "UN killer-robot talks end, no rules — Sat 21",
    "BepiColombo enters Mercury orbit — Sat 21",
    "El Chapo Isidro captured — Fri 21",
    "Bahrain radar claim, Houthi missiles — Sat 22",
]

STILL_OPEN = [
    "COP31: no resumed session; items go to COP32, Nov 2027.",
    "Cikande: ~30 still missing; DNA IDs take weeks.",
    "Four-way Ukraine talks: no date or venue set.",
]

WATCH_TUESDAY = [
    "Dell earnings Tue; US core PCE Wed [FORECAST].",
    "India v NZ, 2nd Test starts Fri, Christchurch.",
    "Black Friday: will 182.7m shoppers show up? [FORECAST]",
    "US funding deadline: Dec 11, no bills passed.",
]

# Drones launched at Ukraine per night (Ukrainian Air Force / Zelenskyy).
DRONE_BARS = [
    ("19–20", 400, "400+"),
    ("20–21", 148, "148"),
    ("21–22", 186, "186"),
    ("22–23", 153, "153"),
]

REGION_ORDER = [
    "Europe", "Middle East", "Asia-Pacific", "Africa",
    "Americas", "Sport", "Markets & Tech",
]

SHORT_LINES = []  # index lines shortened with an ellipsis


def region_tally():
    from collections import Counter
    seen = Counter()
    for story in BIG_THREE:
        seen[story["region"]] += 1
    for card in BRIEFS:
        seen[card["region"]] += 1
    for _, _, region in REST:
        seen[region] += 1
    return [(name, seen.get(name, 0)) for name in REGION_ORDER]


if __name__ == "__main__" and "--selftest" in sys.argv:
    assert len(BIG_THREE) == 3 and len(BRIEFS) == 10 and len(REST) == 47
    total = 3 + 10 + 47
    assert total == 60, total
    tally = region_tally()
    assert sum(v for _, v in tally) == 60, tally
    print("counts OK: 13 featured + 47 index = 60; regions:", tally)


# ------------------------------------------------------------------ pictures
def draw_pictogram(draw, kind, x, y, size=34):
    """One small flat pictogram, drawn in code."""
    if kind == "ballot":
        draw.rectangle([x + 2, y + 12, x + size - 2, y + size - 2],
                       outline=NAVY, width=2)
        draw.rectangle([x + 8, y + 2, x + size - 8, y + 12], fill=RED)
        draw.line([x + 6, y + 18, x + size - 6, y + 18], fill=NAVY, width=2)
        draw.line([x + 6, y + 24, x + size - 10, y + 24], fill=NAVY, width=2)
    elif kind == "cricket":
        draw.ellipse([x + 20, y + 4, x + 30, y + 14], fill=RED)
        draw.line([x + 6, y + 30, x + 22, y + 12], fill=(139, 90, 43), width=5)
    elif kind == "flame":
        draw.polygon(
            [(x + 17, y + 2), (x + 26, y + 14), (x + 30, y + 22),
             (x + 24, y + 30), (x + 10, y + 30), (x + 4, y + 22),
             (x + 8, y + 14)],
            fill=(230, 90, 20),
        )
        draw.polygon(
            [(x + 17, y + 12), (x + 23, y + 20), (x + 21, y + 28),
             (x + 13, y + 28), (x + 11, y + 20)],
            fill=(255, 200, 40),
        )
    elif kind == "dove":
        draw.ellipse([x + 4, y + 14, x + 26, y + 28], fill=(255, 255, 255),
                      outline=NAVY, width=2)
        draw.ellipse([x + 22, y + 6, x + 31, y + 15], fill=(255, 255, 255),
                      outline=NAVY, width=2)
        draw.polygon([(x + 30, y + 10), (x + 34, y + 12), (x + 30, y + 14)],
                     fill=GOLD)
        draw.arc([x + 8, y + 10, x + 24, y + 24], 200, 340, fill=NAVY, width=2)
        draw.line([x + 2, y + 30, x + 12, y + 30], fill=(90, 170, 90), width=2)
        draw.ellipse([x + 12, y + 27, x + 16, y + 31], fill=(90, 170, 90))
    elif kind == "toxic":
        draw.polygon([(x + 17, y + 2), (x + 32, y + 30), (x + 2, y + 30)],
                     fill=(255, 200, 40), outline=INK)
        draw.text((x + 14, y + 14), "!", font=sans_b(14), fill=INK)
    elif kind == "castle":
        draw.rectangle([x + 4, y + 14, x + 30, y + 32], fill=(150, 150, 150))
        draw.rectangle([x + 4, y + 8, x + 10, y + 14], fill=(150, 150, 150))
        draw.rectangle([x + 14, y + 8, x + 20, y + 14], fill=(150, 150, 150))
        draw.rectangle([x + 24, y + 8, x + 30, y + 14], fill=(150, 150, 150))
        draw.rectangle([x + 14, y + 20, x + 20, y + 32], fill=(60, 60, 60))
        draw.line([x + 17, y + 8, x + 17, y + 2], fill=INK, width=2)
        draw.polygon([(x + 17, y + 2), (x + 26, y + 5), (x + 17, y + 8)],
                     fill=RED)
    elif kind == "heart":
        draw.ellipse([x + 4, y + 6, x + 18, y + 20], fill=RED)
        draw.ellipse([x + 16, y + 6, x + 30, y + 20], fill=RED)
        draw.polygon([(x + 5, y + 14), (x + 29, y + 14), (x + 17, y + 31)],
                     fill=RED)
        draw.line([x + 10, y + 10, x + 14, y + 14], fill=(255, 255, 255),
                  width=2)
    elif kind == "oil":
        draw.polygon([(x + 6, y + 30), (x + 14, y + 4), (x + 20, y + 4),
                      (x + 28, y + 30)], outline=INK, width=2)
        draw.line([x + 10, y + 22, x + 24, y + 22], fill=INK, width=2)
        draw.line([x + 12, y + 14, x + 22, y + 14], fill=INK, width=2)
        draw.rectangle([x + 4, y + 30, x + 30, y + 32], fill=INK)
        draw.ellipse([x + 26, y + 8, x + 32, y + 14], fill=(60, 60, 60))
    elif kind == "chip":
        draw.rectangle([x + 8, y + 8, x + 26, y + 26], fill=NAVY)
        draw.rectangle([x + 13, y + 13, x + 21, y + 21], fill=(255, 255, 255))
        for px in (12, 17, 22):
            draw.line([x + px, y + 2, x + px, y + 8], fill=INK, width=2)
            draw.line([x + px, y + 26, x + px, y + 32], fill=INK, width=2)
            draw.line([x + 2, y + px, x + 8, y + px], fill=INK, width=2)
            draw.line([x + 26, y + px, x + 32, y + px], fill=INK, width=2)
    elif kind == "alert":
        draw.polygon([(x + 17, y + 2), (x + 32, y + 30), (x + 2, y + 30)],
                     fill=RED)
        draw.text((x + 14, y + 12), "!", font=sans_b(16), fill=(255, 255, 255))


def draw_lead_picture(draw, which, x, y, w, h):
    """Illustrated header for one big lead, drawn in code."""
    if which == 0:  # COP31: globe, thermometer, NO DEAL stamp
        draw.rectangle([x, y, x + w, y + h], fill=(214, 232, 240))
        cx, cy, r = x + 62, y + h // 2 + 4, 40
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=(70, 130, 180), outline=NAVY, width=2)
        draw.ellipse([cx - 28, cy - 24, cx - 6, cy - 6], fill=(90, 170, 90))
        draw.ellipse([cx + 2, cy + 8, cx + 26, cy + 30], fill=(90, 170, 90))
        draw.ellipse([cx + 8, cy - 30, cx + 24, cy - 14], fill=(90, 170, 90))
        tx = x + w - 78
        draw.rectangle([tx, y + 14, tx + 10, y + h - 24], outline=RED,
                       width=2, fill=(255, 255, 255))
        draw.rectangle([tx + 2, y + h - 44, tx + 8, y + h - 26], fill=RED)
        draw.ellipse([tx - 3, y + h - 26, tx + 13, y + h - 10], fill=RED)
        draw.text((tx + 15, y + 56), "1.5°C", font=sans_b(9), fill=RED)
        draw.text((x + 118, y + 8), "ANTALYA", font=sans_b(10), fill=NAVY)
        draw.text((x + 118, y + 22), "no cover decision", font=sans(10),
                  fill=INK)
        draw.text((x + 118, y + 36), "first since 2000", font=sans(10),
                  fill=INK)
        draw.text((x + 118, y + 52), "NO DEAL", font=sans_b(12), fill=RED)
    elif which == 1:  # Ukraine: night sky, drones, block, blast
        draw.rectangle([x, y, x + w, y + h], fill=NIGHT)
        for sx, sy in [(20, 10), (60, 22), (110, 8), (170, 16), (230, 10),
                       (290, 20), (90, 30), (200, 28)]:
            draw.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2],
                         fill=(255, 255, 255))
        for dx, dy in [(40, 26), (150, 18), (250, 30)]:
            draw.rectangle([x + dx, y + dy, x + dx + 16, y + dy + 5],
                           fill=(200, 200, 200))
            draw.line([x + dx - 4, y + dy - 3, x + dx + 4, y + dy - 3],
                      fill=(200, 200, 200), width=2)
            draw.line([x + dx + 12, y + dy - 3, x + dx + 20, y + dy - 3],
                      fill=(200, 200, 200), width=2)
        bx, by = x + 120, y + h - 42
        draw.rectangle([bx, by, bx + 90, y + h], fill=(120, 120, 120))
        for wy in range(by + 6, y + h - 4, 10):
            for wx in range(bx + 6, bx + 86, 14):
                draw.rectangle([wx, wy, wx + 8, wy + 6],
                               fill=(255, 220, 120))
        ex, ey = bx + 45, by - 6
        for ang in range(0, 360, 30):
            ex2 = ex + 16 * math.cos(math.radians(ang))
            ey2 = ey + 16 * math.sin(math.radians(ang))
            draw.line([ex, ey, ex2, ey2], fill=(255, 160, 30), width=3)
        draw.ellipse([ex - 10, ey - 10, ex + 10, ey + 10],
                     fill=(255, 200, 60))
        draw.text((x + 8, y + h - 16), "153 DRONES · 134 DOWNED",
                  font=sans_b(9), fill=(255, 220, 120))
    else:  # Markets: a V-shaped rebound on a dark board
        draw.rectangle([x, y, x + w, y + h], fill=NIGHT)
        draw.line([x + 14, y + 10, x + 14, y + h - 14], fill=MUTE, width=1)
        draw.line([x + 14, y + h - 14, x + w - 10, y + h - 14], fill=MUTE,
                  width=1)
        pts = [(20, 18), (70, 26), (120, 22), (170, 44), (210, 58),
               (250, 34), (290, 16)]
        for i in range(len(pts) - 1):
            ax, ay = x + pts[i][0], y + pts[i][1]
            bx, by = x + pts[i + 1][0], y + pts[i + 1][1]
            colour = RED if by > ay else (60, 200, 90)
            draw.line([ax, ay, bx, by], fill=colour, width=3)
        draw.polygon([(x + 290, y + 16), (x + 282, y + 20), (x + 290, y + 24)],
                     fill=(60, 200, 90))
        draw.text((x + 20, y + h - 30), "NASDAQ FUTURES +3%",
                  font=sans_b(10), fill=(60, 200, 90))
        draw.text((x + 20, y + h - 16), "NVIDIA +9.4% PRE-MARKET",
                  font=sans_b(9), fill=(255, 255, 255))


def draw_world_map(draw, x0, y0, mw, mh):
    """Dotted world map with numbered pins; returns the pin list."""
    blobs = [(-100, 50, 28, 18), (-152, 64, 10, 5), (-88, 15, 8, 4),
             (-42, 73, 8, 4), (-60, -15, 12, 20), (15, 52, 14, 9),
             (-2, 54, 3, 4), (18, 2, 16, 22), (95, 50, 45, 17),
             (78, 21, 7, 9), (102, 12, 8, 6), (115, -3, 12, 3),
             (138, 38, 4, 6), (134, -25, 14, 7), (172, -41, 3, 4)]

    def on_land(lon, lat):
        for cl, ca, rx, ry in blobs:
            if ((lon - cl) / rx) ** 2 + ((lat - ca) / ry) ** 2 <= 1:
                return True
        return False

    px = x0
    while px < x0 + mw:
        py = y0
        while py < y0 + mh:
            lo = (px - x0) / mw * 360 - 180
            la = 82 - (py - y0) / mh * 140
            if on_land(lo, la):
                draw.ellipse([px - 1.5, py - 1.5, px + 1.5, py + 1.5],
                             fill=(140, 150, 165))
            py += 5
        px += 5

    def to_px(la, lo):
        return (x0 + (lo + 180) / 360 * mw, y0 + (82 - la) / 140 * mh)

    pins = []
    for story in BIG_THREE + BRIEFS:
        la, lo, lab = story["pin"]
        px, py = to_px(la, lo)
        pins.append((story["n"], px, py, lab))
    for n, px, py, lab in pins:
        draw.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                     outline=(255, 255, 255), width=1)
        f = sans_b(8)
        tw = f.getlength(str(n))
        draw.text((px - tw / 2, py - 6), str(n), font=f,
                  fill=(255, 255, 255))
    return pins


# ------------------------------------------------------------------ the page
def render():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(img)
    m = MARGIN
    d.rectangle([0, 0, PAGE_W, 5], fill=RED)

    # ---- masthead
    y = 12
    f = serif_b(19)
    title = "THE WORLD IN ONE DAY"
    d.text(((PAGE_W - f.getlength(title)) // 2, y), title, font=f, fill=INK)
    y += 26
    d.line([m, y, PAGE_W - m, y], fill=INK, width=2)
    y += 6
    f = serif_b(44)
    dateline = "Monday 23 November 2026"
    d.text(((PAGE_W - f.getlength(dateline)) // 2, y), dateline, font=f,
           fill=INK)
    y += 54
    f = serif_i(15)
    deck = ("COP31 fallout: 1.5°C overshoot 'now inevitable'  ·  "
            "153 drones over Ukraine  ·  Wall Street bounces back")
    d.text(((PAGE_W - f.getlength(deck)) // 2, y), deck, font=f, fill=RED)
    y += 24
    d.line([m, y, PAGE_W - m, y], fill=INK, width=1)

    # ---- six-number band
    y += 5
    box_w = (PAGE_W - 2 * m - 5 * 6) // 6
    for i, (num, lab) in enumerate(BIG_NUMBERS):
        bx = m + i * (box_w + 6)
        d.rectangle([bx, y, bx + box_w, y + 42], outline=INK, width=1)
        d.text((bx + 6, y + 2), num, font=sans_b(20),
               fill=RED if i in (0, 1, 2) else INK)
        d.text((bx + 6, y + 25), lab, font=sans(9), fill=INK)
    y += 48

    # ---- region band
    tally = region_tally()
    d.text((m, y), "60 STORIES  ·  7 REGIONS:", font=sans_b(10), fill=INK)
    xx = m + sans_b(10).getlength("60 STORIES  ·  7 REGIONS:  ")
    d.text((xx, y), "   ".join(f"{r} {v}" for r, v in tally),
           font=sans(10), fill=NAVY)
    y += 17
    d.line([m, y, PAGE_W - m, y], fill=INK, width=1)

    # ---- day-by-the-clock strip (UTC)
    y += 5
    d.text((m, y), "DAY BY THE CLOCK — ALL TIMES UTC", font=sans_b(10),
           fill=RED)
    y += 15
    d.line([m, y + 8, PAGE_W - m, y + 8], fill=MUTE, width=1)
    span = PAGE_W - 2 * m
    for i, (tm, ev) in enumerate(DAY_CLOCK):
        px = m + int((i + 0.5) * span / len(DAY_CLOCK))
        d.ellipse([px - 3, y + 5, px + 3, y + 11], fill=RED)
        tw = sans_b(9).getlength(tm)
        d.text((px - tw / 2, y - 2), tm, font=sans_b(9), fill=INK)
        ly = y + 14
        for ln in fit_text(ev, sans(8), 96)[:2]:
            tw2 = sans(8).getlength(ln)
            d.text((px - tw2 / 2, ly), ln, font=sans(8), fill=INK)
            ly += 9
    y += 36

    # ---- the three big stories
    d.text((m, y), "THE THREE BIG STORIES", font=sans_b(11), fill=RED)
    y += 16
    lead_w = (PAGE_W - 2 * m - 2 * 10) // 3
    top_y = y
    for i, story in enumerate(BIG_THREE):
        bx = m + i * (lead_w + 10)
        draw_lead_picture(d, i, bx, y, lead_w, 70)
        yy = y + 74
        d.text((bx, yy), story["kicker"], font=sans_b(9), fill=RED)
        yy += 12
        for ln in fit_text(story["head"], serif_b(15), lead_w):
            d.text((bx, yy), ln, font=serif_b(15), fill=INK)
            yy += 17
        for ln in fit_text(story["body"], sans(10), lead_w):
            d.text((bx, yy), ln, font=sans(10), fill=INK)
            yy += 12
        d.text((bx, yy + 1), "Source: " + story["src"], font=sans(8),
               fill=MUTE)
    y = top_y + 70 + 12 + 34 + 48 + 13
    d.line([m, y, PAGE_W - m, y], fill=INK, width=1)

    # ---- ten more, in brief (5 x 2 grid)
    y += 5
    d.text((m, y), "TEN MORE, IN BRIEF", font=sans_b(11), fill=RED)
    y += 15
    card_w = (PAGE_W - 2 * m - 4 * 8) // 5
    card_h = 56
    for i, card in enumerate(BRIEFS):
        row, col = divmod(i, 5)
        bx = m + col * (card_w + 8)
        by = y + row * (card_h + 6)
        d.rectangle([bx, by, bx + card_w, by + card_h], outline=MUTE,
                    width=1)
        draw_pictogram(d, card["icon"], bx + 5, by + 5, 26)
        tx = bx + 40
        yy = by + 4
        for ln in fit_text(card["head"], sans_b(10), card_w - 46):
            d.text((tx, yy), ln, font=sans_b(10), fill=INK)
            yy += 12
            if yy > by + 28:
                break
        yy = by + 37
        for ln in fit_text(card["body"], sans(9), card_w - 10):
            d.text((bx + 5, yy), ln, font=sans(9), fill=INK)
            yy += 11
            if yy > by + card_h - 13:
                break
        d.text((bx + 5, by + card_h - 9), "Source: " + card["src"],
               font=sans(8), fill=MUTE)
    y += 2 * card_h + 6 + 4

    # ---- world map + legend underneath
    d.line([m, y, PAGE_W - m, y], fill=INK, width=1)
    y += 4
    d.text((m, y), "WHERE IT HAPPENED — the 13 featured stories, numbered",
           font=sans_b(11), fill=RED)
    y += 13
    pins = draw_world_map(d, m, y, PAGE_W - 2 * m, 104)
    y += 106
    legend = [f"{n}. {lab}" for n, _, _, lab in pins]
    d.text((m, y), "   ·   ".join(legend[:7]), font=sans(9), fill=INK)
    y += 10
    d.text((m, y), "   ·   ".join(legend[7:]), font=sans(9), fill=INK)
    y += 11

    # ---- bottom row: chart | date check | not yet | watch Tuesday
    d.line([m, y, PAGE_W - m, y], fill=INK, width=1)
    y += 4
    box_w2 = (PAGE_W - 2 * m - 3 * 8) // 4
    boxes_y = y
    bx = m
    d.rectangle([bx, y, bx + box_w2, y + 84], outline=INK, width=1)
    d.text((bx + 6, y + 4), "DRONES AT UKRAINE / NIGHT", font=sans_b(9),
           fill=RED)
    top_v = max(v for _, v, _ in DRONE_BARS)
    base = y + 76
    for i, (lab, v, txt) in enumerate(DRONE_BARS):
        cx0 = bx + 12 + i * 56
        bh = int(v / top_v * 42)
        d.rectangle([cx0, base - bh, cx0 + 30, base],
                    fill=NAVY if i == 3 else (150, 160, 175))
        d.text((cx0 + 2, base - bh - 11), txt, font=sans_b(9), fill=INK)
        d.text((cx0 - 2, base + 2), lab, font=sans(8), fill=INK)
    bx = m + (box_w2 + 8)
    d.rectangle([bx, y, bx + box_w2, y + 84], outline=RED, width=2)
    d.text((bx + 6, y + 4), "DATE CHECK — NOT MONDAY", font=sans_b(9),
           fill=RED)
    yy = y + 16
    for ln in WRONG_DAY:
        d.text((bx + 6, yy), "✕ " + ln, font=sans(8), fill=INK)
        yy += 11
    bx = m + 2 * (box_w2 + 8)
    d.rectangle([bx, y, bx + box_w2, y + 84], outline=INK, width=1)
    d.text((bx + 6, y + 4), "NOT YET HAPPENED", font=sans_b(9), fill=RED)
    yy = y + 16
    for ln in STILL_OPEN:
        for wln in fit_text(ln, sans(8), box_w2 - 12):
            d.text((bx + 6, yy), "• " + wln, font=sans(8), fill=INK)
            yy += 11
        yy += 2
    bx = m + 3 * (box_w2 + 8)
    d.rectangle([bx, y, bx + box_w2, y + 84], outline=INK, width=1)
    d.text((bx + 6, y + 4), "WHAT TO WATCH ON TUESDAY", font=sans_b(9),
           fill=RED)
    yy = y + 16
    for ln in WATCH_TUESDAY:
        for wln in fit_text(ln, sans(8), box_w2 - 12):
            d.text((bx + 6, yy), "• " + wln, font=sans(8), fill=INK)
            yy += 11
        yy += 2
    d.text((m, boxes_y + 88),
           "Chart source: Ukrainian Air Force (nightly totals) / Zelenskyy (400+ figure).",
           font=sans(8), fill=MUTE)
    y = boxes_y + 100

    # ---- index: 47 more stories, 3 columns
    d.line([m, y, PAGE_W - m, y], fill=INK, width=1)
    y += 4
    d.text((m, y), "ALSO ON MONDAY 23 NOVEMBER — 47 MORE STORIES",
           font=sans_b(11), fill=RED)
    y += 15
    col_w = (PAGE_W - 2 * m - 2 * 10) // 3
    per_col = 16
    fidx = sans(9)
    for ci in range(3):
        cx = m + ci * (col_w + 10)
        yy = y
        for j in range(per_col):
            k = ci * per_col + j
            if k >= len(REST):
                break
            txt, src, _ = REST[k]
            line = f"{14 + k}. {txt} — {src}"
            while fidx.getlength(line) > col_w and len(txt) > 20:
                txt = txt[:-4].rstrip()
                line = f"{14 + k}. {txt}… — {src}"
                SHORT_LINES.append(line)
            d.text((cx, yy), line, font=fidx, fill=INK)
            yy += 11
    y += per_col * 11 + 4

    # ---- footer
    d.line([m, y, PAGE_W - m, y], fill=INK, width=1)
    y += 4
    d.text((m, y),
           "60 stories, each checked against a report of Monday 23 November 2026. "
           "[CLAIM] = unverified claim. [FORECAST] = not yet happened. Drawn in code — no photos.",
           font=sans(8), fill=MUTE)
    return img


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    render().save(out, optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")
    if SHORT_LINES:
        print("SHORTENED index lines:")
        for t in SHORT_LINES:
            print("  ", t)
