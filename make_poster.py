#!/usr/bin/env python3
"""Draw the news poster for Thursday, November 19, 2026.

A one-image summary of the day: a dated masthead and six panels, each
with a category tag, a small drawn icon, a bold headline and one short
factual line.  Drawn entirely with Pillow so every word stays crisp.
Running this file writes entry.png next to it.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (24, 28, 38)
MUTED = (96, 102, 112)
NAVY = (16, 34, 64)
RED = (178, 34, 44)

BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_KICKER = font(BOLD, 25)
F_TITLE = font(BOLD, 52)
F_SUB = font(REG, 24)
F_TAG = font(BOLD, 19)
F_HEAD = font(BOLD, 29)
F_DESC = font(REG, 21)
F_FOOT = font(REG, 19)


def wrap(draw, text, fnt, max_width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- icons
def icon_missile(d, x, y, s, color):
    d.polygon([(x + s * 0.5, y), (x + s * 0.72, y + s * 0.34),
               (x + s * 0.62, y + s * 0.78), (x + s * 0.38, y + s * 0.78),
               (x + s * 0.28, y + s * 0.34)], fill=color)
    d.polygon([(x + s * 0.38, y + s * 0.78), (x + s * 0.62, y + s * 0.78),
               (x + s * 0.5, y + s)], fill=(240, 140, 40))
    d.ellipse([x + s * 0.42, y + s * 0.3, x + s * 0.58, y + s * 0.46],
              fill=(255, 255, 255))


def icon_globe(d, x, y, s, color):
    d.ellipse([x + s * 0.08, y + s * 0.08, x + s * 0.92, y + s * 0.92],
              outline=color, width=6)
    d.ellipse([x + s * 0.34, y + s * 0.08, x + s * 0.66, y + s * 0.92],
              outline=color, width=4)
    d.line([x + s * 0.1, y + s * 0.38, x + s * 0.9, y + s * 0.38],
           fill=color, width=4)
    d.line([x + s * 0.1, y + s * 0.64, x + s * 0.9, y + s * 0.64],
           fill=color, width=4)


def icon_gamepad(d, x, y, s, color):
    dark = (16, 34, 64)
    d.rounded_rectangle([x + s * 0.06, y + s * 0.28, x + s * 0.94, y + s * 0.8],
                        radius=12, fill=color)
    d.rectangle([x + s * 0.2, y + s * 0.47, x + s * 0.36, y + s * 0.57],
                fill=dark)
    d.rectangle([x + s * 0.26, y + s * 0.42, x + s * 0.3, y + s * 0.62],
                fill=dark)
    d.ellipse([x + s * 0.62, y + s * 0.4, x + s * 0.7, y + s * 0.48],
              fill=dark)
    d.ellipse([x + s * 0.74, y + s * 0.4, x + s * 0.82, y + s * 0.48],
              fill=dark)
    d.ellipse([x + s * 0.68, y + s * 0.54, x + s * 0.76, y + s * 0.62],
              fill=dark)
    d.line([x + s * 0.1, y + s * 0.82, x + s * 0.28, y + s * 0.94],
           fill=color, width=6)
    d.line([x + s * 0.9, y + s * 0.82, x + s * 0.72, y + s * 0.94],
           fill=color, width=6)


def icon_rocket(d, x, y, s, color):
    d.polygon([(x + s * 0.5, y + s * 0.04), (x + s * 0.68, y + s * 0.36),
               (x + s * 0.62, y + s * 0.66), (x + s * 0.38, y + s * 0.66),
               (x + s * 0.32, y + s * 0.36)], fill=color)
    d.ellipse([x + s * 0.42, y + s * 0.26, x + s * 0.58, y + s * 0.42],
              fill=(255, 255, 255))
    d.polygon([(x + s * 0.38, y + s * 0.6), (x + s * 0.2, y + s * 0.86),
               (x + s * 0.38, y + s * 0.74)], fill=color)
    d.polygon([(x + s * 0.62, y + s * 0.6), (x + s * 0.8, y + s * 0.86),
               (x + s * 0.62, y + s * 0.74)], fill=color)
    d.polygon([(x + s * 0.42, y + s * 0.68), (x + s * 0.58, y + s * 0.68),
               (x + s * 0.5, y + s * 0.94)], fill=(240, 140, 40))


def icon_bridge(d, x, y, s, color):
    d.arc([x, y + s * 0.05, x + s, y + s * 0.85], 180, 360, fill=color, width=6)
    for fx in (0.18, 0.38, 0.62, 0.82):
        d.line([x + s * fx, y + s * 0.28, x + s * fx, y + s * 0.62],
               fill=color, width=4)
    d.line([x, y + s * 0.62, x + s, y + s * 0.62], fill=color, width=7)
    d.line([x, y + s * 0.8, x + s, y + s * 0.8], fill=(70, 130, 200), width=5)
    d.line([x, y + s * 0.92, x + s, y + s * 0.92], fill=(70, 130, 200), width=5)


def icon_palette(d, x, y, s, color):
    d.ellipse([x + s * 0.08, y + s * 0.08, x + s * 0.92, y + s * 0.92],
              fill=color)
    for (cx, cy), dot in (((0.3, 0.32), (178, 34, 44)),
                          ((0.58, 0.24), (38, 84, 160)),
                          ((0.74, 0.46), (24, 120, 74))):
        d.ellipse([x + s * cx - 7, y + s * cy - 7,
                   x + s * cx + 7, y + s * cy + 7], fill=dot)
    d.ellipse([x + s * 0.6, y + s * 0.58, x + s * 0.8, y + s * 0.78],
              fill=PAPER)


ICONS = {
    "missile": icon_missile,
    "globe": icon_globe,
    "gamepad": icon_gamepad,
    "rocket": icon_rocket,
    "bridge": icon_bridge,
    "palette": icon_palette,
}

PANELS = [
    {
        "tag": "GAMES", "color": (112, 62, 168), "icon": "gamepad",
        "headline": "GTA VI LAUNCHES WORLDWIDE",
        "desc": "Grand Theft Auto VI launched worldwide to near-perfect "
                "reviews after a 13-year wait.",
    },
    {
        "tag": "SUMMIT", "color": (38, 84, 160), "icon": "globe",
        "headline": "TRUMP LANDS IN CHINA",
        "desc": "Trump landed in China to a rare airport welcome from Xi, "
                "ahead of a trilateral summit with Putin in Shenzhen.",
    },
    {
        "tag": "HORMUZ", "color": (178, 34, 44), "icon": "missile",
        "headline": "TANKERS BURN OFF HORMUZ",
        "desc": "Oil tankers caught fire after hitting mines east of the "
                "Strait of Hormuz; the U.S. struck Iran's Qeshm Island.",
    },
    {
        "tag": "SPACE", "color": (24, 120, 74), "icon": "rocket",
        "headline": "VOYAGER 1 REACHES ONE LIGHT-DAY",
        "desc": "NASA's Voyager 1 became the first human-made object to "
                "reach one light-day from Earth.",
    },
    {
        "tag": "EUROPE", "color": (70, 96, 140), "icon": "bridge",
        "headline": "EU PROPOSES \u20ac45\u201349BN UKRAINE LOAN",
        "desc": "The EU proposed a \u20ac45\u201349 billion loan for Ukraine, "
                "to be repaid after Russia pays reparations.",
    },
    {
        "tag": "CULTURE", "color": (206, 110, 24), "icon": "palette",
        "headline": "VAN GOGH SELLS FOR RECORD $190.4M",
        "desc": "A Van Gogh painting sold for a record $190.4 million "
                "at auction.",
    },
]


def draw_panel(d, x, y, w, h, panel):
    color = panel["color"]
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=(255, 255, 255),
                        outline=(210, 204, 190), width=2)
    d.rounded_rectangle([x, y, x + w, y + 40], radius=14, fill=color)
    d.rectangle([x, y + 26, x + w, y + 40], fill=color)
    d.text((x + 16, y + 8), panel["tag"], font=F_TAG, fill=(255, 255, 255))
    bx, by, bs = x + 16, y + 56, 84
    d.rounded_rectangle([bx, by, bx + bs, by + bs], radius=12, fill=color)
    inner = Image.new("RGBA", (bs, bs), (0, 0, 0, 0))
    idraw = ImageDraw.Draw(inner)
    ICONS[panel["icon"]](idraw, 10, 10, bs - 20, (255, 255, 255))
    tx = x + 116
    head_lines = wrap(d, panel["headline"], F_HEAD, x + w - tx - 14)
    hy = y + 54
    for line in head_lines[:2]:
        d.text((tx, hy), line, font=F_HEAD, fill=INK)
        hy += 36
    desc_lines = wrap(d, panel["desc"], F_DESC, w - 32)
    dy = y + 152
    for line in desc_lines[:3]:
        d.text((x + 16, dy), line, font=F_DESC, fill=MUTED)
        dy += 28
    return inner, (bx, by)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 156], fill=RED)
    d.text((36, 18), "THE WORLD IN ONE PICTURE  \u00b7  DAILY NEWS POSTER",
           font=F_KICKER, fill=(250, 205, 90))
    d.text((36, 50), "THURSDAY, NOVEMBER 19, 2026", font=F_TITLE,
           fill=(255, 255, 255))
    d.text((36, 116), "The six stories that defined the day, at a glance",
           font=F_SUB, fill=(190, 202, 224))

    margin, gap = 28, 16
    pw = (W - margin * 2 - gap) // 2
    ph = 258
    top = 172
    overlays = []
    for i, panel in enumerate(PANELS):
        col, row = i % 2, i // 2
        x = margin + col * (pw + gap)
        y = top + row * (ph + gap)
        inner, pos = draw_panel(d, x, y, pw, ph, panel)
        overlays.append((inner, pos))
    for inner, pos in overlays:
        img.paste(inner, pos, inner)

    d.text((36, H - 34),
           "Compiled from Reuters, AP and AFP reporting.",
           font=F_FOOT, fill=MUTED)

    out = HERE / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, out.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
