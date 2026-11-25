#!/usr/bin/env python3
"""Render the front page of THE WORLD for Tuesday 24 November 2026.

Deterministic: fixed fonts, fixed layout, no randomness, no network.
Run: python3 render.py  -> writes entry.png (1024x1024) next to this file.
"""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 36
COL_GAP = 24

PAPER = (247, 243, 232)   # off-white newsprint
INK = (18, 18, 18)
RED = (158, 22, 22)
NAVY = (16, 32, 56)
GREY = (90, 90, 90)
RULE = (120, 110, 95)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 92)
F_DATE = font("DejaVuSans-Bold.ttf", 21)
F_KICK = font("DejaVuSans-Bold.ttf", 15)
F_HEAD = font("DejaVuSerif-Bold.ttf", 40)
F_DECK = font("DejaVuSerif.ttf", 20)
F_BODY = font("DejaVuSerif.ttf", 16)
F_SECT = font("DejaVuSans-Bold.ttf", 17)
F_ITEM_HEAD = font("DejaVuSans-Bold.ttf", 15)
F_ITEM_BODY = font("DejaVuSerif.ttf", 14)
F_SPORT = font("DejaVuSans-Bold.ttf", 18)
F_FOOT = font("DejaVuSans.ttf", 13)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by measured pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, y, text, fnt, fill, tracking=0):
    if tracking:
        spaced = (" " * tracking).join(list(text.replace(" ", "   ")))
        # simple letterspacing: draw with spaces between chars
        text = spaced
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 4


def rule(draw, y, x0, x1, width=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)
    return y + 6


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    y = 30
    # ---- Masthead ----
    y = draw_centered(d, y, "THE WORLD", F_MAST, INK)
    y += 2
    y = draw_centered(d, y, "TUESDAY,  24  NOVEMBER  2026", F_DATE, INK)
    y += 6
    y = rule(d, y, MARGIN, W - MARGIN, 3)
    y = rule(d, y, MARGIN, W - MARGIN, 1)
    y += 8

    # ---- Lead story ----
    d.text((MARGIN, y), "UNITED STATES  •  TRADE & TECHNOLOGY", font=F_KICK, fill=RED)
    y += 24
    lead_head = "Huawei found guilty of trade-secret conspiracy and bank fraud"
    for line in wrap(d, lead_head, F_HEAD, W - 2 * MARGIN):
        d.text((MARGIN, y), line, font=F_HEAD, fill=INK)
        y += 48
    y += 2
    deck = "US jury acquits Chinese telecoms giant of racketeering in landmark trial"
    for line in wrap(d, deck, F_DECK, W - 2 * MARGIN):
        d.text((MARGIN, y), line, font=F_DECK, fill=INK)
        y += 26
    y += 6
    lead_body = (
        "A federal jury in New York found the Chinese telecoms giant guilty of "
        "conspiring to steal trade secrets and of bank fraud on Tuesday. The jury "
        "cleared Huawei of racketeering, the most serious charge it faced."
    )
    for line in wrap(d, lead_body, F_BODY, W - 2 * MARGIN):
        d.text((MARGIN, y), line, font=F_BODY, fill=INK)
        y += 21
    y += 10
    y = rule(d, y, MARGIN, W - MARGIN, 2)
    y += 6

    # ---- The day in brief ----
    d.text((MARGIN, y), "THE DAY IN BRIEF", font=F_SECT, fill=NAVY)
    y += 26
    y = rule(d, y, MARGIN, W - MARGIN, 1)
    y += 10

    items = [
        ("RIYADH", "Houthi missile hits Saudi PIF tower",
         "At least 11 wounded in the financial district; second strike in under "
         "a week. Coalition answers with strikes on Hodeidah port."),
        ("STRAIT OF HORMUZ", "Iran says it hit a container ship",
         "IRGC navy claims the attack; Iran reports four tankers hit by mines "
         "in the strait."),
        ("CARTAGENA", "25 hostages held at supermarket",
         "Armed men seize shoppers in Colombia's port city; police surround "
         "the store."),
        ("TURKEY", "Air Force helicopter crashes, 5 killed",
         "AS-532 comes down after takeoff from Eskisehir on a training flight."),
        ("BLACK SEA", "Ukraine drones hit Russian ships",
         "Cargo ship Sparta II struck in the Gulf of Finland and off Libya; "
         "Libya condemns the attack."),
        ("GAZA", "Israeli strike kills Hamas security chief",
         "Brig-Gen Naeem Abu Mohammed Nahel killed in Gaza, officials say."),
        ("KYIV", "Germany first into Ukraine's Delta system",
         "Berlin gains access to the battlefield management network; deal on "
         "interceptor missiles."),
        ("BRUSSELS", "NATO vows to defend space",
         "Chief Mark Rutte warns the alliance will respond to threats in orbit "
         "after reports of a Russian nuclear-armed satellite."),
        ("KATHMANDU", "5.6 quake shakes Nepal",
         "Magnitude 5.6 tremor strikes near the Chinese border."),
        ("BEIJING", "Shenzhou-24 carries Pakistan's first astronaut",
         "Zeeshan Ali flies aboard China's latest crewed mission."),
        ("THE HAGUE", "14 nations back Rohingya ruling",
         "Countries recognise the ICJ decision that Myanmar committed genocide."),
        ("DAKAR", "Senegal regain Africa Cup title",
         "Champions again after a sports court appeal overturns the result."),
    ]

    col_w = (W - 2 * MARGIN - COL_GAP) // 2
    row_h = 78  # kicker 20 + headline 19 + 2 body lines at 18 = 75, plus slack
    grid_top = y
    for i, (kicker, head, body) in enumerate(items):
        r, c = divmod(i, 2)
        x = MARGIN + c * (col_w + COL_GAP)
        yy = grid_top + r * row_h
        d.text((x, yy), kicker, font=F_KICK, fill=RED)
        yy += 20
        head_lines = wrap(d, head, F_ITEM_HEAD, col_w)
        for line in head_lines[:1]:
            d.text((x, yy), line, font=F_ITEM_HEAD, fill=INK)
            yy += 19
        for line in wrap(d, body, F_ITEM_BODY, col_w)[:2]:
            d.text((x, yy), line, font=F_ITEM_BODY, fill=INK)
            yy += 18
    y = grid_top + 6 * row_h + 4

    # ---- Sports strip ----
    band_top = y
    band_h = 62
    assert band_top + band_h + 40 <= H, "layout overflow: sports band too low"
    d.rectangle([MARGIN, band_top, W - MARGIN, band_top + band_h], fill=NAVY)
    sport = ("SPORT   •   REAL MADRID 5-1 PSV   •   MAN CITY 2-2 NAPOLI   •   "
             "ARSENAL 2-2 DORTMUND   •   SENEGAL WIN AFCON TITLE")
    lines = wrap(d, sport, F_SPORT, W - 2 * MARGIN - 24)
    sy = band_top + (band_h - len(lines) * 22) // 2
    for line in lines:
        lw = d.textlength(line, font=F_SPORT)
        d.text(((W - lw) / 2, sy), line, font=F_SPORT, fill=(255, 255, 255))
        sy += 22
    y = band_top + band_h + 12

    # ---- Footer ----
    y = draw_centered(d, y, "THE WORLD  —  Tuesday 24 November 2026  •  One day's news in full",
                      F_FOOT, GREY)
    assert y < H - 8, "layout overflow: footer too low"

    img.save(OUT, format="PNG")
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
