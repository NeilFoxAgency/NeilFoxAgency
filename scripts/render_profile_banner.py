#!/usr/bin/env python3
"""Render the animated, brand-matched GitHub profile banner."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONT_DIR = ASSETS / "fonts"
LOGO_PATH = ASSETS / "neil-fox-logo.webp"
GIF_PATH = ASSETS / "profile-banner.gif"
PREVIEW_PATH = ASSETS / "profile-banner-preview.png"

WIDTH = 1600
HEIGHT = 650
FRAME_COUNT = 16
FRAME_DURATION_MS = 210

INK = (3, 16, 34)
INK_2 = (7, 23, 44)
PANEL = (11, 27, 49)
CHROME = (32, 43, 58)
ORANGE = (255, 77, 18)
ORANGE_2 = (255, 106, 36)
BLUE = (71, 168, 255)
MINT = (49, 214, 160)
WHITE = (255, 254, 250)
BODY = (199, 207, 219)
MUTED = (139, 154, 174)
LINE = (39, 63, 91)

SERIF_PATH = FONT_DIR / "DM-Serif-Display-Regular.ttf"
SANS_PATH = FONT_DIR / "DM-Sans-Regular.ttf"
SANS_BOLD_PATH = FONT_DIR / "DM-Sans-Bold.ttf"


def load_font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


def rounded_box(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill: tuple[int, ...],
    outline: tuple[int, ...] | None = None,
    width: int = 1,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_soft_shadow(
    image: Image.Image,
    box: tuple[int, int, int, int],
    radius: int,
    alpha: int = 96,
    blur: int = 22,
) -> None:
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        box, radius=radius, fill=(0, 0, 0, alpha)
    )
    image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(blur)))


def make_background() -> Image.Image:
    image = Image.new("RGBA", (WIDTH, HEIGHT), INK + (255,))
    draw = ImageDraw.Draw(image, "RGBA")

    # A slow navy gradient keeps the artwork close to the agency's site hero.
    for y in range(HEIGHT):
        t = y / max(1, HEIGHT - 1)
        color = tuple(
            round(INK[i] * (1 - t) + INK_2[i] * t) for i in range(3)
        )
        draw.line((0, y, WIDTH, y), fill=color + (255,))

    glows = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glows)
    glow_draw.ellipse((-350, 190, 720, 1020), fill=BLUE + (29,))
    glow_draw.ellipse((270, 405, 1170, 1000), fill=ORANGE + (19,))
    glow_draw.ellipse((1030, 40, 1810, 780), fill=BLUE + (21,))
    image.alpha_composite(glows.filter(ImageFilter.GaussianBlur(112)))

    grid = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    grid_draw = ImageDraw.Draw(grid)
    for x in range(0, WIDTH, 54):
        grid_draw.line((x, 88, x, HEIGHT), fill=(255, 255, 255, 8), width=1)
    for y in range(108, HEIGHT, 54):
        grid_draw.line((0, y, WIDTH, y), fill=(255, 255, 255, 8), width=1)
    image.alpha_composite(grid)
    return image


def add_brand_header(image: Image.Image) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    draw.rectangle((0, 0, WIDTH, 88), fill=CHROME + (246,))
    draw.rectangle((0, 0, WIDTH, 4), fill=ORANGE + (255,))
    draw.line((0, 87, WIDTH, 87), fill=(104, 122, 143, 100), width=1)

    logo = Image.open(LOGO_PATH).convert("RGBA")
    alpha = logo.getchannel("A")
    bounds = alpha.getbbox()
    if bounds:
        logo = logo.crop(bounds)
    logo.thumbnail((64, 68), Image.Resampling.LANCZOS)
    image.alpha_composite(logo, (50, 10))

    draw = ImageDraw.Draw(image, "RGBA")
    draw.text(
        (128, 25),
        "Neil Fox Agency",
        font=load_font(SERIF_PATH, 35),
        fill=WHITE,
    )
    draw.text(
        (795, 34),
        "CREATOR PARTNERSHIPS  /  DEVELOPER YOUTUBE",
        font=load_font(SANS_BOLD_PATH, 15),
        fill=(224, 231, 240),
    )
    rounded_box(draw, (1300, 24, 1540, 62), 19, (3, 16, 34, 170), (91, 111, 135, 120), 1)
    draw.ellipse((1316, 38, 1328, 50), fill=MINT + (255,))
    draw.text(
        (1340, 32),
        "FOUNDER · BUILDER",
        font=load_font(SANS_BOLD_PATH, 13),
        fill=(225, 235, 245),
    )


def add_left_column(image: Image.Image) -> None:
    draw = ImageDraw.Draw(image, "RGBA")

    rounded_box(draw, (56, 126, 506, 168), 11, (5, 30, 57, 210), (71, 168, 255, 155), 2)
    rounded_box(draw, (70, 136, 99, 158), 6, ORANGE + (255,))
    draw.polygon([(82, 140), (82, 154), (92, 147)], fill=WHITE + (255,))
    draw.text(
        (114, 137),
        "CREATOR PARTNERSHIPS  ·  BUILDER FIRST",
        font=load_font(SANS_BOLD_PATH, 13),
        fill=(232, 239, 248),
    )

    serif = load_font(SERIF_PATH, 68)
    draw.text((56, 191), "Creator partnerships", font=serif, fill=WHITE)
    first = "that put "
    orange = "fit first."
    first_width = draw.textlength(first, font=serif)
    draw.text((56, 264), first, font=serif, fill=WHITE)
    draw.text((56 + first_width, 264), orange, font=serif, fill=ORANGE)

    body = load_font(SANS_PATH, 21)
    draw.text(
        (59, 354),
        "Connecting developer YouTubers with dev-tool and SaaS sponsors.",
        font=body,
        fill=BODY,
    )
    draw.text(
        (59, 386),
        "Building research and campaign systems in Python + TypeScript.",
        font=body,
        fill=BODY,
    )

    cards = [
        ((56, 454, 247, 555), "70K+", "SUBSCRIBERS", "educational channel", BLUE),
        ((259, 454, 450, 555), "17M+", "VIEWS", "educational channel", ORANGE),
        ((462, 454, 690, 555), "$1M+", "LIFETIME REVENUE", "ArtworkTee", MINT),
    ]
    for box, value, label, caption, accent in cards:
        x1, y1, x2, y2 = box
        draw_soft_shadow(image, box, 14, alpha=56, blur=14)
        draw = ImageDraw.Draw(image, "RGBA")
        rounded_box(draw, box, 14, (8, 26, 47, 222), (69, 97, 130, 94), 1)
        rounded_box(draw, (x1 + 15, y1 + 15, x1 + 19, y2 - 15), 2, accent + (255,))
        draw.text((x1 + 31, y1 + 10), value, font=load_font(SERIF_PATH, 36), fill=WHITE)
        draw.text(
            (x1 + 31, y1 + 57),
            label,
            font=load_font(SANS_BOLD_PATH, 11),
            fill=accent,
        )
        draw.text(
            (x1 + 31, y1 + 76),
            caption,
            font=load_font(SANS_PATH, 11),
            fill=MUTED,
        )


def add_workflow_panel(image: Image.Image, frame_index: int) -> None:
    progress = frame_index / FRAME_COUNT
    active_step = min(2, int(progress * 3))
    draw_soft_shadow(image, (731, 116, 1545, 558), 25, alpha=116, blur=24)
    draw = ImageDraw.Draw(image, "RGBA")

    rounded_box(draw, (731, 116, 1545, 558), 25, (8, 25, 46, 246), (73, 150, 218, 190), 2)
    draw.line((756, 117, 1305, 117), fill=(111, 192, 255, 180), width=2)

    draw.text(
        (771, 145),
        "ILLUSTRATIVE WORKFLOW",
        font=load_font(SANS_BOLD_PATH, 13),
        fill=ORANGE,
    )
    rounded_box(draw, (1284, 138, 1505, 169), 15, (7, 35, 50, 205), (49, 214, 160, 90), 1)
    draw.text(
        (1300, 146),
        "CREATOR-FIRST · DATA-HONEST",
        font=load_font(SANS_BOLD_PATH, 10),
        fill=(168, 238, 218),
    )
    draw.text(
        (771, 178),
        "From better fit to clear recap",
        font=load_font(SANS_BOLD_PATH, 31),
        fill=WHITE,
    )
    draw.text(
        (772, 222),
        "Respect the creator. Make the terms clear. Report what the data supports.",
        font=load_font(SANS_PATH, 15),
        fill=MUTED,
    )

    stages = [
        (772, "01", "Find the fit", "Audience before reach"),
        (1021, "02", "Coordinate", "Clear terms. Your call."),
        (1270, "03", "Measure", "Track what is available"),
    ]
    centers = [x + 110 for x, _, _, _ in stages]
    connector_y = 277
    for start, end in zip(centers, centers[1:]):
        draw.line((start + 17, connector_y, end - 17, connector_y), fill=(55, 114, 160, 180), width=3)

    pulse = (math.sin(progress * math.tau) + 1) / 2
    for index, (x, number, title, caption) in enumerate(stages):
        box = (x, 295, x + 229, 401)
        is_active = index == active_step
        border = (255, 105, 50, 218) if is_active else (64, 96, 130, 130)
        fill = (13, 37, 63, 242) if is_active else (6, 22, 41, 232)
        rounded_box(draw, box, 15, fill, border, 2 if is_active else 1)

        node_x = centers[index]
        node_color = ORANGE if is_active else BLUE
        if is_active:
            ring_alpha = int(38 + pulse * 60)
            draw.ellipse(
                (node_x - 17, connector_y - 17, node_x + 17, connector_y + 17),
                outline=node_color + (ring_alpha,),
                width=5,
            )
        draw.ellipse(
            (node_x - 8, connector_y - 8, node_x + 8, connector_y + 8),
            fill=node_color + (255,),
        )

        rounded_box(draw, (x + 16, 313, x + 47, 344), 9, (30, 46, 66, 255), (74, 116, 154, 120), 1)
        draw.text(
            (x + 21, 320),
            number,
            font=load_font(SANS_BOLD_PATH, 12),
            fill=ORANGE if is_active else BLUE,
        )
        draw.text(
            (x + 57, 314),
            title,
            font=load_font(SANS_BOLD_PATH, 18),
            fill=WHITE,
        )
        draw.text(
            (x + 17, 364),
            caption,
            font=load_font(SANS_PATH, 13),
            fill=BODY,
        )

    # This moving pulse suggests a connected process, not campaign performance data.
    travel_x = centers[0] + progress * (centers[-1] - centers[0])
    halo_alpha = int(36 + 54 * pulse)
    draw.ellipse(
        (travel_x - 12, connector_y - 12, travel_x + 12, connector_y + 12),
        fill=ORANGE + (halo_alpha,),
    )
    draw.ellipse(
        (travel_x - 5, connector_y - 5, travel_x + 5, connector_y + 5),
        fill=WHITE + (255,),
    )

    rounded_box(draw, (772, 423, 1503, 528), 15, (5, 18, 35, 225), (53, 85, 120, 110), 1)
    draw.text(
        (794, 439),
        "TRACKING WITHOUT THEATER",
        font=load_font(SANS_BOLD_PATH, 12),
        fill=ORANGE_2,
    )
    draw.text(
        (794, 461),
        "Links + codes",
        font=load_font(SANS_BOLD_PATH, 15),
        fill=WHITE,
    )
    draw.text(
        (794, 485),
        "Deliverables",
        font=load_font(SANS_BOLD_PATH, 15),
        fill=WHITE,
    )
    draw.text(
        (1044, 461),
        "Available results",
        font=load_font(SANS_BOLD_PATH, 15),
        fill=WHITE,
    )
    draw.text(
        (1044, 485),
        "Clear next steps",
        font=load_font(SANS_BOLD_PATH, 15),
        fill=WHITE,
    )

    # Small path accent animates through the recap band without implying live metrics.
    path_points = [(1286, 493), (1334, 486), (1372, 492), (1411, 469), (1469, 475)]
    draw.line(path_points, fill=(71, 168, 255, 165), width=3, joint="curve")
    spark_index = int(progress * (len(path_points) - 1))
    t = (progress * (len(path_points) - 1)) % 1
    xa, ya = path_points[spark_index]
    xb, yb = path_points[min(spark_index + 1, len(path_points) - 1)]
    spark_x = xa + (xb - xa) * t
    spark_y = ya + (yb - ya) * t
    draw.ellipse((spark_x - 9, spark_y - 9, spark_x + 9, spark_y + 9), fill=ORANGE + (75,))
    draw.ellipse((spark_x - 4, spark_y - 4, spark_x + 4, spark_y + 4), fill=ORANGE + (255,))

    draw.text(
        (1248, 439),
        "PRACTICAL RECAP",
        font=load_font(SANS_BOLD_PATH, 10),
        fill=MUTED,
    )


def render_frame(background: Image.Image, frame_index: int) -> Image.Image:
    image = background.copy()
    add_brand_header(image)
    add_left_column(image)
    add_workflow_panel(image, frame_index)
    return image.convert("RGB")


def main() -> None:
    for required in (LOGO_PATH, SERIF_PATH, SANS_PATH, SANS_BOLD_PATH):
        if not required.exists():
            raise SystemExit(f"Missing required asset: {required}")

    background = make_background()
    frames = [render_frame(background, i) for i in range(FRAME_COUNT)]
    frames[0].save(PREVIEW_PATH, format="PNG", optimize=True)

    # Derive one shared palette to avoid a color shift between animation frames.
    palette_source = Image.new("RGB", (WIDTH, HEIGHT * len(frames)))
    for index, frame in enumerate(frames):
        palette_source.paste(frame, (0, index * HEIGHT))
    palette = palette_source.quantize(colors=192, method=Image.Quantize.MEDIANCUT)
    palette_frames = [
        frame.quantize(palette=palette, dither=Image.Dither.FLOYDSTEINBERG)
        for frame in frames
    ]
    palette_frames[0].save(
        GIF_PATH,
        format="GIF",
        save_all=True,
        append_images=palette_frames[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        optimize=True,
        disposal=1,
    )
    print(f"Wrote {GIF_PATH} ({GIF_PATH.stat().st_size:,} bytes)")
    print(f"Wrote {PREVIEW_PATH} ({PREVIEW_PATH.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
