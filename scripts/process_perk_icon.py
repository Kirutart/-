from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


PALETTE = (
    (5, 8, 6),
    (16, 21, 19),
    (17, 25, 18),
    (39, 51, 38),
    (128, 111, 70),
    (185, 154, 83),
    (228, 202, 125),
    (221, 211, 176),
    (149, 155, 141),
    (111, 40, 36),
    (23, 40, 45),
)


def nearest_palette_color(red: int, green: int, blue: int) -> tuple[int, int, int]:
    return min(
        PALETTE,
        key=lambda color: (
            (red - color[0]) ** 2
            + (green - color[1]) ** 2
            + (blue - color[2]) ** 2
        ),
    )


def process(source: Path, destination: Path) -> None:
    image = Image.open(source).convert("RGBA")
    alpha_box = image.getchannel("A").getbbox()
    if alpha_box is None:
        raise ValueError(f"No visible pixels in {source}")

    image = image.crop(alpha_box)
    scale = min(76 / image.width, 76 / image.height)
    resized_size = (
        max(1, round(image.width * scale)),
        max(1, round(image.height * scale)),
    )
    image = image.resize(resized_size, Image.Resampling.LANCZOS)

    working = Image.new("RGBA", (96, 96), (5, 8, 6, 0))
    working.alpha_composite(
        image,
        ((96 - resized_size[0]) // 2, (96 - resized_size[1]) // 2),
    )

    quantized = []
    for red, green, blue, alpha in working.getdata():
        if alpha == 0:
            quantized.append((5, 8, 6, 0))
            continue
        quantized.append((*nearest_palette_color(red, green, blue), alpha))
    working.putdata(quantized)

    final = working.resize((192, 192), Image.Resampling.NEAREST)
    destination.parent.mkdir(parents=True, exist_ok=True)
    final.save(destination, "WEBP", lossless=True, method=6, exact=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    process(args.source, args.destination)


if __name__ == "__main__":
    main()
