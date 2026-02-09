# ImageRescaler

Multi-monitor wallpaper generator. Composes multiple images into centered, horizontally-laid-out wallpapers — one per monitor.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

**Load an image into the library:**
```bash
python -m src.cli load /path/to/image.jpg
```

**Generate wallpapers for all detected monitors:**
```bash
python -m src.cli generate
```

**Apply wallpapers to your desktop:**
```bash
python -m src.cli apply
```

## How It Works

Images are stored in `images/`. When you run `generate`, the app detects your monitors, randomly selects images using a hero + greedy fill algorithm, composes them onto a centered canvas, and saves to `output/<width>x<height>_<monitor>/`. Each run produces a unique wallpaper. Run `apply` to set them on your desktop via macOS AppleScript.
