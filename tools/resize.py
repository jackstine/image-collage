#!/usr/bin/env python3
"""Resize an image to a percentage of its original size, preserving aspect ratio."""

import argparse
import sys
from pathlib import Path
from PIL import Image


def resize_image(input_path: Path, percent: float, output_path: Path | None = None) -> Path:
    if not (1 <= percent <= 100):
        raise ValueError(f"Percent must be between 1 and 100, got {percent}")

    with Image.open(input_path) as img:
        orig_w, orig_h = img.size
        new_w = max(1, round(orig_w * percent / 100))
        new_h = max(1, round(orig_h * percent / 100))
        resized = img.resize((new_w, new_h), Image.LANCZOS)

        if output_path is None:
            stem = input_path.stem
            suffix = input_path.suffix
            output_path = input_path.parent / f"{stem}_{int(percent)}pct{suffix}"

        resized.save(output_path)
        print(f"{orig_w}x{orig_h} → {new_w}x{new_h}  saved to {output_path}")
        return output_path


def main():
    parser = argparse.ArgumentParser(description="Resize an image to a percentage of its original size.")
    parser.add_argument("image", type=Path, help="Path to the input image")
    parser.add_argument("percent", type=float, help="Resize percentage (1–100)")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Output file path (optional)")
    args = parser.parse_args()

    if not args.image.exists():
        print(f"Error: file not found: {args.image}", file=sys.stderr)
        sys.exit(1)

    resize_image(args.image, args.percent, args.output)


if __name__ == "__main__":
    main()
