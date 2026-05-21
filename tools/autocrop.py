#!/usr/bin/env python3
"""
autocrop.py — crop solid black borders from an image.

Usage:
    python autocrop.py <image_path> [--threshold N] [--suffix SUFFIX]

Outputs a new file alongside the original with the suffix appended before
the extension (default: _cropped). The original is never modified.
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image


def find_content_bounds(arr: np.ndarray, threshold: int = 10) -> tuple[int, int, int, int]:
    """Return (left, top, right, bottom) pixel bounds of non-black content."""
    # Treat a pixel as non-black if any channel exceeds the threshold
    mask = arr.max(axis=2) > threshold  # shape: (H, W), True = content

    # Collapse along each axis to find where content exists
    col_has_content = mask.any(axis=0)  # shape: (W,)
    row_has_content = mask.any(axis=1)  # shape: (H,)

    if not col_has_content.any() or not row_has_content.any():
        raise ValueError("No non-black content found in image (try lowering --threshold).")

    left = int(col_has_content.argmax())
    right = int(len(col_has_content) - col_has_content[::-1].argmax())
    top = int(row_has_content.argmax())
    bottom = int(len(row_has_content) - row_has_content[::-1].argmax())

    return left, top, right, bottom


def autocrop(image_path: str, threshold: int = 10, suffix: str = "", output_dir: str | None = None) -> Path:
    src = Path(image_path)
    if not src.exists():
        raise FileNotFoundError(f"File not found: {src}")

    img = Image.open(src).convert("RGB")
    arr = np.array(img)

    left, top, right, bottom = find_content_bounds(arr, threshold)

    orig_w, orig_h = img.size
    crop_w = right - left
    crop_h = bottom - top

    print(f"Original size : {orig_w} x {orig_h}")
    print(f"Content bounds: left={left}, top={top}, right={right}, bottom={bottom}")
    print(f"Cropped size  : {crop_w} x {crop_h}")

    cropped = img.crop((left, top, right, bottom))

    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        dst = out_dir / (src.stem + suffix + src.suffix)
    else:
        dst = src.with_stem(src.stem + suffix)

    cropped.save(dst, quality=95)
    print(f"Saved          : {dst}")
    return dst


def main():
    parser = argparse.ArgumentParser(description="Auto-crop black borders from an image.")
    parser.add_argument("image", nargs="+", help="Path(s) to source image(s)")
    parser.add_argument(
        "--threshold", type=int, default=10,
        help="Pixel brightness threshold below which a pixel is considered black (default: 10)"
    )
    parser.add_argument(
        "--suffix", default="",
        help="Suffix appended to the filename before the extension (default: none)"
    )
    parser.add_argument(
        "--output-dir", default=None,
        help="Directory to write cropped images into (created if needed)"
    )
    args = parser.parse_args()

    errors = 0
    for path in args.image:
        try:
            autocrop(path, threshold=args.threshold, suffix=args.suffix, output_dir=args.output_dir)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error ({path}): {e}", file=sys.stderr)
            errors += 1
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
