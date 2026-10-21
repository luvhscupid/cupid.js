"""Generate synthetic scoreboard images and exact OCR ground truth.

Requires Pillow (``python -m pip install Pillow``). The generator is deterministic.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


def _font(size: int) -> ImageFont.ImageFont:
    return ImageFont.load_default(size=size)


def render_scoreboard(home: str, away: str, home_score: int, away_score: int) -> Image.Image:
    image = Image.new("RGB", (960, 360), "#101820")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((24, 24, 936, 336), radius=24, fill="#172b3b", outline="#52d6c7", width=4)
    draw.text((54, 52), "FINAL  ·  SYNTHETIC LEAGUE", font=_font(26), fill="#52d6c7")
    draw.line((54, 104, 906, 104), fill="#496174", width=2)
    draw.text((68, 144), away, font=_font(42), fill="white")
    draw.text((68, 236), home, font=_font(42), fill="white")
    draw.text((778, 132), str(away_score), font=_font(64), fill="#ffca58")
    draw.text((778, 224), str(home_score), font=_font(64), fill="#ffca58")
    return image


def _write_case(out: Path, case_id: str, image: Image.Image, gt: dict, variation: str) -> dict:
    name = f"{case_id}.png"
    image.save(out / name)
    return {"id": case_id, "image": name, "variation": variation, "ground_truth": gt}


def generate(out_dir: Path) -> list[dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    entries = []
    for idx, (away, home, ascore, hscore) in enumerate([
        ("NORTH STARS", "RED COMETS", 3, 12),
        ("BLUE HARBOR", "IRON PEAK", 28, 7),
    ], start=1):
        base = render_scoreboard(home, away, hscore, ascore)
        base_gt = {
            "away_team": away,
            "away_score": ascore,
            "home_team": home,
            "home_score": hscore,
            "winner": home if hscore > ascore else away,
        }
        entries.append(_write_case(out_dir, f"game-{idx}-clean", base, base_gt, "clean"))

        blurry = base.filter(ImageFilter.GaussianBlur(radius=2.2))
        entries.append(_write_case(out_dir, f"game-{idx}-blur", blurry, base_gt, "blurred"))

        small = base.resize((240, 90), Image.Resampling.LANCZOS)
        entries.append(_write_case(out_dir, f"game-{idx}-downscale", small, base_gt, "downscaled"))

        # A deliberate edit changes one displayed digit; the truth follows the pixels.
        edited_gt = dict(base_gt)
        edited_gt["home_score"] = (hscore + 1) % 100
        edited = base.copy()
        ImageDraw.Draw(edited).rectangle((770, 222, 912, 300), fill="#172b3b")
        ImageDraw.Draw(edited).text((778, 224), str(edited_gt["home_score"]), font=_font(64), fill="#ffca58")
        entries.append(_write_case(out_dir, f"game-{idx}-edited", edited, edited_gt, "edited_home_score"))

    payload = {"schema_version": 1, "cases": entries}
    (out_dir / "ground_truth.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return entries


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="directory for PNGs and ground_truth.json")
    args = parser.parse_args()
    cases = generate(args.output)
    print(f"Generated {len(cases)} scoreboard images and ground_truth.json in {args.output}")


if __name__ == "__main__":
    main()
