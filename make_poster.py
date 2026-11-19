#!/usr/bin/env python3
"""One-image world-news poster for Thursday 19 November 2026.

Builds a 1024x1024 PNG with Pillow only: a masthead, then six
story tiles in a 2x3 grid. Every tile carries a tag, a headline,
one factual line and a small hand-drawn geometric glyph.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
PLAIN = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

PAPER = (247, 242, 233)
INK = (28, 40, 48)
MUTED = (96, 104, 102)
BAND = (16, 58, 52)
BAND_INK = (247, 242, 233)
GOLD = (198, 142, 38)


def load_fonts():
    """Return (bold, regular) font factories sized on demand."""
    def bold(px):
        try:
            return ImageFont.truetype(BOLD, px)
        except OSError:
            return ImageFont.load_default()

    def regular(px):
        try:
            return ImageFont.truetype(PLAIN, px)
        except OSError:
            return ImageFont.load_default()

    return bold, regular


def wrap_line(draw, text, font, width):
    """Greedy word wrap returning a list of lines fitting `width`."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_glyph(draw, kind, cx, cy, r, colour):
    """Draw a small geometric icon centred at (cx, cy)."""
    if kind == "games":
        # gamepad: rounded body + d-pad + two buttons
        draw.rounded_rectangle([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
                               radius=r * 0.5, outline=colour, width=4)
        draw.line([cx - r * 0.62, cy, cx - r * 0.28, cy], fill=colour, width=4)
        draw.line([cx - r * 0.45, cy - r * 0.17, cx - r * 0.45, cy + r * 0.17],
                  fill=colour, width=4)
        draw.ellipse([cx + r * 0.30, cy - r * 0.30, cx + r * 0.52, cy - r * 0.08],
                     fill=colour)
        draw.ellipse([cx + r * 0.58, cy + r * 0.08, cx + r * 0.80, cy + r * 0.30],
                     fill=colour)
    elif kind == "summit":
        # three peaks meeting: triangles of different heights
        for i, h in enumerate((0.9, 1.25, 0.75)):
            x0 = cx - r + i * r * 0.66
            draw.polygon([(x0, cy + r * 0.5), (x0 + r * 0.33, cy - r * h * 0.5),
                          (x0 + r * 0.66, cy + r * 0.5)], outline=colour, width=4)
        draw.line([cx - r, cy + r * 0.62, cx + r, cy + r * 0.62], fill=colour, width=4)
    elif kind == "hormuz":
        # flame above two wave strokes
        draw.polygon([(cx, cy - r), (cx + r * 0.55, cy + r * 0.1),
                      (cx + r * 0.15, cy + r * 0.45), (cx - r * 0.15, cy + r * 0.45),
                      (cx - r * 0.55, cy + r * 0.1)], outline=colour, width=4)
        for dy in (0.62, 0.85):
            draw.arc([cx - r, cy + r * dy - 8, cx + r, cy + r * dy + 8],
                     start=200, end=340, fill=colour, width=4)
    elif kind == "space":
        # four-point star inside a tilted orbit ring
        draw.polygon([(cx, cy - r), (cx + r * 0.22, cy - r * 0.22),
                      (cx + r, cy), (cx + r * 0.22, cy + r * 0.22),
                      (cx, cy + r), (cx - r * 0.22, cy + r * 0.22),
                      (cx - r, cy), (cx - r * 0.22, cy - r * 0.22)], fill=colour)
        draw.ellipse([cx - r * 1.15, cy - r * 0.45, cx + r * 1.15, cy + r * 0.45],
                     outline=colour, width=3)
    elif kind == "europe":
        # ring of small stars around a coin disc
        draw.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45],
                     outline=colour, width=4)
        for k in range(8):
            ang = math.pi * 2 * k / 8 - math.pi / 2
            sx = cx + r * 0.85 * math.cos(ang)
            sy = cy + r * 0.85 * math.sin(ang)
            draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=colour)
    elif kind == "culture":
        # sunflower: centre disc plus eight petal spokes
        for k in range(8):
            ang = math.pi * 2 * k / 8
            x1 = cx + r * 0.45 * math.cos(ang)
            y1 = cy + r * 0.45 * math.sin(ang)
            x2 = cx + r * 0.95 * math.cos(ang)
            y2 = cy + r * 0.95 * math.sin(ang)
            draw.line([x1, y1, x2, y2], fill=colour, width=6)
        draw.ellipse([cx - r * 0.32, cy - r * 0.32, cx + r * 0.32, cy + r * 0.32],
                     fill=colour)


STORIES = [
    ("games", "GAMES", "Grand Theft Auto VI launches worldwide",
     "Near-perfect reviews after a 13-year wait.",
     (176, 62, 48)),
    ("summit", "SUMMIT", "Trump lands in China to rare Xi welcome",
     "Xi greets him on the tarmac; summit with Putin in Shenzhen today.",
     (14, 124, 107)),
    ("hormuz", "HORMUZ", "Tankers burn on mines off Hormuz",
     "US strikes Iran's Qeshm Island; fires spread east of the strait.",
     (178, 96, 24)),
    ("space", "SPACE", "Voyager 1 reaches one light-day away",
     "The first human-made object to travel that far from home.",
     (52, 84, 150)),
    ("europe", "EUROPE", "EU proposes €45–49bn loan for Ukraine",
     "To be repaid after Russia pays reparations, under the new plan.",
     (112, 74, 158)),
    ("culture", "CULTURE", "Van Gogh sells for a record $190.4M",
     "The auction price sets a new high for the artist's work.",
     (198, 142, 38)),
]


def build_poster(path):
    bold, regular = load_fonts()
    canvas = Image.new("RGB", (SIDE, SIDE), PAPER)
    draw = ImageDraw.Draw(canvas)

    # --- masthead band ---
    draw.rectangle([0, 0, SIDE, 148], fill=BAND)
    draw.rectangle([0, 148, SIDE, 154], fill=GOLD)
    title_font = bold(52)
    draw.text((28, 22), "THE WORLD ON THURSDAY", font=title_font, fill=BAND_INK)
    date_font = bold(30)
    date_text = "NOV 19, 2026"
    draw.text((SIDE - 28 - draw.textlength(date_text, font=date_font), 30),
              date_text, font=date_font, fill=GOLD)
    sub_font = regular(26)
    draw.text((28, 96),
              "Six stories that defined the day — in one picture.",
              font=sub_font, fill=(214, 224, 220))

    # --- six tiles, 2 columns x 3 rows ---
    margin, gap = 28, 20
    top, bottom = 176, 996
    tile_w = (SIDE - margin * 2 - gap) // 2
    tile_h = (bottom - top - gap * 2) // 3
    tag_font = bold(21)
    head_font = bold(32)
    body_font = regular(24)

    for idx, (kind, tag, headline, fact, accent) in enumerate(STORIES):
        col, row = idx % 2, idx // 2
        x0 = margin + col * (tile_w + gap)
        y0 = top + row * (tile_h + gap)
        x1, y1 = x0 + tile_w, y0 + tile_h

        draw.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=(255, 255, 255))
        draw.rounded_rectangle([x0, y0, x1, y1], radius=18, outline=(214, 206, 192), width=2)
        draw.rectangle([x0 + 18, y0, x0 + 26, y0 + 52], fill=accent)

        # tag + glyph share the top row
        draw.text((x0 + 44, y0 + 20), tag, font=tag_font, fill=accent)
        draw_glyph(draw, kind, x1 - 52, y0 + 52, 30, accent)

        # headline, wrapped to at most two lines
        head_lines = wrap_line(draw, headline, head_font, tile_w - 56)[:2]
        hy = y0 + 62
        for line in head_lines:
            draw.text((x0 + 28, hy), line, font=head_font, fill=INK)
            hy += 38

        # factual line, wrapped to at most three lines
        fact_lines = wrap_line(draw, fact, body_font, tile_w - 56)[:3]
        fy = y0 + tile_h - 28 - len(fact_lines) * 30
        for line in fact_lines:
            draw.text((x0 + 28, fy), line, font=body_font, fill=MUTED)
            fy += 30

    canvas.save(path, format="PNG", optimize=True)


if __name__ == "__main__":
    target = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build_poster(target)
    print(f"wrote {target}")
