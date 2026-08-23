from __future__ import annotations

import base64
import re
from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def save_webp(source: Path, target: Path, *, max_size: tuple[int, int] | None, quality: int) -> None:
    with Image.open(source) as opened:
        image = opened.convert("RGBA" if "A" in opened.getbands() else "RGB")
        if max_size is not None:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        target.parent.mkdir(parents=True, exist_ok=True)
        image.save(
            target,
            format="WEBP",
            quality=quality,
            method=6,
            alpha_quality=100,
            exact=True,
        )
        print(f"{source.relative_to(ROOT)} -> {target.relative_to(ROOT)} {image.width}x{image.height}")


def save_circle_background_with_ninth_frame(source: Path, target: Path) -> None:
    """Repeat only the gold eighth-card ornament in the empty ninth-card slot."""
    with Image.open(source) as opened:
        background = opened.convert("RGBA")
    source_box = (54, 1706, 690, 1833)
    frame = background.crop(source_box)
    mask = Image.new("L", frame.size)
    frame_pixels = frame.load()
    mask_pixels = mask.load()
    for y in range(frame.height):
        for x in range(frame.width):
            red, green, blue, _ = frame_pixels[x, y]
            warm = (red + green) / 2 - blue
            brightness = (red + green + blue) / 3
            alpha = max(0, min(255, int((warm - 5) * 18)))
            if brightness < 24:
                alpha = 0
            mask_pixels[x, y] = alpha
    frame.putalpha(mask)
    background.alpha_composite(frame, (source_box[0], source_box[1] + 125))
    target.parent.mkdir(parents=True, exist_ok=True)
    background.save(target, format="WEBP", quality=90, method=6, alpha_quality=100, exact=True)
    print(f"{source.relative_to(ROOT)} -> {target.relative_to(ROOT)} {background.width}x{background.height}")


def extract_inline_story_images() -> None:
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    block = re.search(r"const STORY_IMAGES=\[(.*?)\];", html, re.DOTALL)
    if not block:
        return
    encoded_images = re.findall(r"data:image/webp;base64,([^']+)", block.group(1))
    for index, encoded in enumerate(encoded_images, start=1):
        target = ROOT / "assets" / "story" / f"intro-{index:02d}.webp"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(base64.b64decode(encoded))
        print(f"inline story image -> {target.relative_to(ROOT)}")


def main() -> None:
    extract_inline_story_images()
    for wave in range(1, 10):
        source = next(ROOT.glob(f"{wave:02d}_*_4k.png"))
        target = ROOT / "assets" / "game" / "backgrounds" / source.name.replace("_4k.png", ".webp")
        save_webp(source, target, max_size=(1080, 1920), quality=86)

    for source in sorted(ROOT.glob("pause_*.png")):
        target = ROOT / "assets" / "game" / "interwave" / f"{source.stem}.webp"
        save_webp(source, target, max_size=(1080, 1920), quality=87)

    ui_jobs = (
        ("main-menu-background-v1-1440x2560.png", "main-menu-background-v2-1080x1920.webp", (1080, 1920), 88),
        ("records-background-v1-841x1870.png", "records-background-v2-841x1870.webp", None, 90),
        ("perk-upgrade-background-v1-841x1870.png", "perk-upgrade-background-v2-841x1870.webp", None, 90),
        ("story-dialog-frame-v1.png", "story-dialog-frame-v2.webp", None, 92),
    )
    for source_name, target_name, max_size, quality in ui_jobs:
        save_webp(
            ROOT / "assets" / "ui" / source_name,
            ROOT / "assets" / "ui" / target_name,
            max_size=max_size,
            quality=quality,
        )
    save_circle_background_with_ninth_frame(
        ROOT / "assets" / "ui" / "circle-select-background-v1-744x2114.png",
        ROOT / "assets" / "ui" / "circle-select-background-v3-744x2114.webp",
    )


if __name__ == "__main__":
    main()
