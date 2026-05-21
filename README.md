# ImageCollage

Multi-monitor wallpaper generator for macOS. Composes multiple images into centered, horizontally-laid-out collages — one per monitor.

## Requirements

- macOS (uses AppleScript to apply wallpapers)
- Python 3.x

## Setup

```bash
pip install -r requirements.txt
```

Or with `uv`:

```bash
uv sync
```

## Usage

**Load an image into the library:**
```bash
python -m src.cli load /path/to/image.jpg
```

Supported formats: JPG, PNG, TIFF, BMP, WebP

**Generate wallpapers for all detected monitors:**
```bash
python -m src.cli generate          # one wallpaper per monitor
python -m src.cli generate 5        # five wallpapers per monitor
```

**Apply a wallpaper to your desktop:**
```bash
python -m src.cli apply
```

Picks a random wallpaper from each monitor's output folder and sets it via AppleScript.

## How It Works

Images are stored in `images/`. When you run `generate`, the app:

1. Detects all connected monitors via `screeninfo`
2. For each monitor, maintains an independent image pool that persists across cycles — images used in one cycle are removed so subsequent cycles get different images, resetting only when the pool is exhausted
3. Selects images using a **hero + greedy fill** algorithm (see below)
4. Composes selected images onto a black canvas, scaled to fit monitor resolution, centered both horizontally and vertically, with 20px gaps between images
5. Saves output to `output/<width>x<height>_<monitor>/` as a JPEG

### Selection Algorithm

For each monitor canvas:

1. Randomly samples ~20% of the available image pool
2. Picks a random **hero** image; if it fills less than 50% of the canvas width, picks a second hero from the remaining space
3. **Greedily fills** remaining space with the narrowest images first
4. Repeats until the canvas is at least 90% filled

This produces varied, non-repeating collages across multiple `generate` runs.
