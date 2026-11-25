#!/usr/bin/env python3
"""Sum up 25 November's world news in one image — make.fun entry.

Draws a 1024x1024 newspaper front page with six stories from
Wednesday 25 November 2026 and writes it to /output/entry.png.
The image itself carries the news: headlines plus one-line summaries,
so it reads on its own with no news feed attached. Six stories, one page.
"""

import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
MARGIN = 48
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RULE = (185, 28, 28)
MUTED = (90, 86, 78)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

STORIES = [
    ("UKRAINE", (30, 90, 168),
     "Ukraine hit a Russian ship in the Gulf of Finland",
     "Zelenskiy confirms the drone strike; Norway urges caution."),
    ("MIDDLE EAST", (176, 62, 34),
     "Houthis hit Riyadh's tallest tower; 11 wounded",
     "Saudi civil defence reports the strike on the tower."),
    ("SPACE", (88, 60, 140),
     "NATO vows space defence over Russian nuclear satellite",
     "The alliance warns it will defend against threats in orbit."),
    ("CHINA", (14, 122, 102),
     "Shenzhou-24 launches successfully from Jiuquan",
     "China's crewed mission lifts off on a Long March 2F."),
    ("TECH", (150, 90, 10),
     "Huawei convicted in US trial over Iran business",
     "Guilty verdict for trade-secret theft and sanctions evasion."),
    ("USA", (120, 40, 40),
     "Trump pardons turkeys Freedom and Feathers",
     "The White House spares the birds for Thanksgiving."),
]


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, font, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=font) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def main():
    image = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(image)
    f_mast = load_font(BOLD, 58)
    f_date = load_font(BOLD, 26)
    f_chip = load_font(BOLD, 20)
    f_head = load_font(BOLD, 30)
    f_body = load_font(REGULAR, 22)
    f_foot = load_font(REGULAR, 20)

    y = MARGIN
    draw.text((MARGIN, y), "THE WORLD IN ONE PAGE", font=f_mast, fill=INK)
    y += 72
    draw.text((MARGIN, y), "WEDNESDAY  ·  25 NOVEMBER 2026", font=f_date, fill=RULE)
    y += 42
    draw.rectangle([MARGIN, y, SIZE - MARGIN, y + 5], fill=RULE)
    y += 26

    for tag, colour, headline, summary in STORIES:
        chip_w = int(draw.textlength(tag, font=f_chip)) + 28
        draw.rounded_rectangle([MARGIN, y, MARGIN + chip_w, y + 32],
                               radius=8, fill=colour)
        draw.text((MARGIN + 14, y + 4), tag, font=f_chip, fill=(255, 255, 255))
        y += 40
        for line in wrap(draw, headline, f_head, SIZE - 2 * MARGIN):
            draw.text((MARGIN, y), line, font=f_head, fill=INK)
            y += 36
        for line in wrap(draw, summary, f_body, SIZE - 2 * MARGIN):
            draw.text((MARGIN, y), line, font=f_body, fill=MUTED)
            y += 28
        y += 8
        draw.line([MARGIN, y, SIZE - MARGIN, y], fill=(200, 192, 178), width=2)
        y += 8

    draw.text((MARGIN, SIZE - 36),
              "Six stories that shaped 25 November 2026  ·  Sources: Reuters, AP",
              font=f_foot, fill=MUTED)

    os.makedirs("/output", exist_ok=True)
    image.save("/output/entry.png", format="PNG")
    size = os.path.getsize("/output/entry.png")
    if size == 0 or size > 1_048_576:
        raise ValueError(f"entry image must be a non-empty PNG under 1 MiB, got {size}")
    if image.size != (1024, 1024):
        raise ValueError(f"entry image must be 1024x1024, got {image.size}")


if __name__ == "__main__":
    main()
