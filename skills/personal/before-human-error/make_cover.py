#!/usr/bin/env python3
"""Build a Before Human Error issue cover to the documented template.

Implements operating_guide id 24 "Issue cover template (visual system)" exactly.
That entry exists because a cover was once rebuilt from guesswork and came back
wrong on typography, so treat the constants below as the spec, not defaults.

  python3 make_cover.py --photo fig.png --issue 8 \
      --title "Nothing Was Marked" \
      --footer "LYONDELLBASELL LA PORTE · 27 JUL 2021 · 2 FATALITIES" \
      --out bheissue08

Writes <out>-1200x675.png (post hero, og:image) and <out>-1000x1000.png (the
beehiiv card, which crops 1:1 and would otherwise cut ~43% off a landscape
cover — see project_state.site_thumbnail_rendering).

Pick the photo from the investigation's OWN report, and crop it clear of any
callout labels: a cover carrying figure annotations reads as a report page.
"""
import argparse
import os

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

W, H = 1200, 675
MARGIN = 64
ACCENT = (192, 57, 43)          # #C0392B, the only colour on the card
GREY = (150, 150, 150)          # #969696
WHITE = (255, 255, 255)

FONTDIR = "/mnt/skills/examples/canvas-design/canvas-fonts"
# Roboto Mono / Inter are not installed here. Geist Mono is the closest mono and
# Instrument Sans the closest neutral grotesque to Inter. If the real faces ever
# land in the container, swap these two lines and nothing else changes.
MONO = os.path.join(FONTDIR, "GeistMono-Regular.ttf")
SANS_BOLD = os.path.join(FONTDIR, "InstrumentSans-Bold.ttf")


def tracked(draw, xy, text, font, fill, tracking):
    """Draw text with letter-spacing. PIL has no tracking, so step per glyph."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x


def tracked_width(draw, text, font, tracking):
    return sum(draw.textlength(c, font=font) + tracking for c in text) - tracking


def build_photo(path, exposure=1.0):
    """Full bleed, monochrome, contrast +15%, brightness -20% (per the spec).

    `exposure` multiplies the spec brightness for source photos that need
    compensation. The template was calibrated on daylight shots; an under-deck
    industrial photo can arrive several stops down and go to mud at -20%.
    Adjust the photo, never the template.
    """
    im = Image.open(path).convert("RGB")
    scale = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left = (im.width - W) // 2
    top = (im.height - H) // 2
    im = im.crop((left, top, left + W, top + H))
    im = ImageEnhance.Color(im).enhance(0.0)
    im = ImageEnhance.Contrast(im).enhance(1.15)
    im = ImageEnhance.Brightness(im).enhance(0.80 * exposure)
    return im


def scrim(im):
    """Dark at the masthead, light through the middle, heavy under the title.

    232 alpha at the top falling to 82 by 22% height, 82 through the middle,
    then ramping to 240 at the bottom so the title always reads.
    """
    layer = Image.new("L", (1, H))
    px = layer.load()
    for y in range(H):
        f = y / H
        if f < 0.22:
            a = 232 + (82 - 232) * (f / 0.22)
        elif f < 0.55:
            a = 82
        else:
            a = 82 + (240 - 82) * ((f - 0.55) / 0.45) ** 1.35
        px[0, y] = int(a)
    mask = layer.resize((W, H))
    return Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, mask)


def draw_card(photo_path, issue, title_lines, footer, exposure=1.0):
    im = scrim(build_photo(photo_path, exposure))
    d = ImageDraw.Draw(im)

    d.rectangle([MARGIN, 58, MARGIN + 34, 58 + 4], fill=ACCENT)

    f_word = ImageFont.truetype(MONO, 17)
    tracked(d, (MARGIN, 80), "BEFORE HUMAN ERROR", f_word, WHITE, 5.2)

    f_issue = ImageFont.truetype(MONO, 12)
    tracked(d, (MARGIN, 112), f"ISSUE {issue} · INCIDENT TEARDOWN", f_issue, GREY, 3.4)

    f_foot = ImageFont.truetype(MONO, 13)
    foot_y = H - 46 - 13
    tracked(d, (MARGIN, foot_y), footer, f_foot, GREY, 2.6)

    # Title sits above the footer and stacks upward, Title Case, no period.
    f_title = ImageFont.truetype(SANS_BOLD, 72)
    line_h = int(72 * 1.06)
    y = foot_y - 34 - line_h * len(title_lines)
    for line in title_lines:
        d.text((MARGIN, y), line, font=f_title, fill=WHITE)
        y += line_h
    return im


def square(card):
    """1000x1000 card: full landscape centred over a blurred, darkened copy."""
    bg = card.resize((1000, 1000), Image.LANCZOS).filter(ImageFilter.GaussianBlur(28))
    bg = ImageEnhance.Brightness(bg).enhance(0.45)
    fg = card.resize((1000, round(1000 * card.height / card.width)), Image.LANCZOS)
    bg.paste(fg, (0, (1000 - fg.height) // 2))
    return bg


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--photo", required=True)
    p.add_argument("--issue", required=True)
    p.add_argument("--title", required=True, help="use | to force a line break")
    p.add_argument("--footer", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--exposure", type=float, default=1.0,
                   help="brightness multiplier for dark source photos, e.g. 1.15")
    a = p.parse_args()

    lines = [s.strip() for s in a.title.split("|")]
    card = draw_card(a.photo, a.issue, lines, a.footer, a.exposure)
    card.save(f"{a.out}-1200x675.png")
    square(card).save(f"{a.out}-1000x1000.png")
    print(f"wrote {a.out}-1200x675.png and {a.out}-1000x1000.png")


if __name__ == "__main__":
    main()
