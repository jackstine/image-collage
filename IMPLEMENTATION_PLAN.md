# Implementation Plan

## Overview
Transform ImageRescaler from a single-file script into a CLI application with three commands (`load`, `generate`, `apply`) that supports multi-monitor wallpaper generation with intelligent image selection.

## Current State
- Single file `image.py` with a basic `rescale_and_center()` function
- Hardcoded image paths and monitor dimensions
- Reversed x/y coordinate naming in layout logic
- No CLI, no monitor detection, no per-monitor output structure
- No `src/` directory structure

---

## Implementation Items (Priority Order)

### 1. Project Structure
- Create module layout:
  ```
  src/
  ├── __init__.py
  ├── cli.py               # CLI entry point (load, generate, apply)
  ├── image_loader.py       # Image ingestion and header-only dimension reading
  ├── monitor.py            # Monitor detection via screeninfo
  ├── selection.py          # Pool generation, hero selection, greedy fill
  ├── composer.py           # Canvas creation, rescaling, layout, centered placement
  └── wallpaper.py          # macOS osascript wallpaper setting
  ```
- Create `requirements.txt` with `Pillow` and `screeninfo`
- **Why**: Every other item depends on having an organized module structure. Without it, the codebase stays monolithic and untestable.

### 2. Image Loader (`image_loader.py`)
- **Spec**: [[specs/image-load-operation|Image Load Operation]]
- Implement `load(source_path)`:
  - Copy file to `images/` directory, preserving original filename
  - Read dimensions from file header using `Image.open(path).size` (lazy, no pixel load)
  - Return `(width, height)` tuple
  - Support JPEG, PNG, TIFF
- Implement `catalog(images_dir)`:
  - Scan all images in a directory
  - Return list of `{path, width, height}` dicts using header-only reads
  - Must handle 1,000+ images efficiently
- **Why**: The selection algorithm and composer both need fast dimension data. This is the data layer everything builds on.
- **Test**: Load 1,000+ images and verify dimensions are read without full pixel loading (measure memory usage stays flat).

### 3. Monitor Detection (`monitor.py`)
- **Spec**: [[specs/wallpaper-generation-algorithm#Monitor Detection]]
- Implement `detect_monitors()`:
  - Use `screeninfo.get_monitors()`
  - Return list of `{name, width, height, x, y}` dicts
- Implement `get_output_dir(monitor)`:
  - Return path `output/<width>x<height>_<name>/`
  - Create directory if it doesn't exist
- **Why**: The generate command needs monitor dimensions to drive the selection algorithm and determine output paths.
- **Test**: Verify output directory naming matches `<width>x<height>_<name>` pattern.

### 4. Selection Algorithm (`selection.py`)
- **Spec**: [[specs/wallpaper-generation-algorithm|Wallpaper Generation Algorithm]]
- Implement `scaled_width(image_width, image_height, monitor_height)`:
  - Returns `image_width * (monitor_height / image_height)`
- Implement `generate_pool(catalog, pool_ratio=0.2)`:
  - Randomly sample ~20% of catalog
  - Sort pool by scaled width ascending
- Implement `select_images(pool, canvas_width, monitor_height, border=20)`:
  - Pick first hero randomly from pool
  - If hero scaled_width < 50% of canvas_width: pick second hero from filtered candidates where `scaled_width <= remaining_width`
  - Greedy fill remaining space from rest of pool (narrowest-first)
  - Return ordered list of selected images
- Implement `select_for_monitors(catalog, monitors, border=20)`:
  - For each monitor, run selection; remove used images from catalog for next monitor
  - Allow repeats only when catalog is exhausted
  - If pool exhausted and space remains, generate new pool and repeat hero selection
- **Why**: This is the core intelligence of the application — it determines which images go where. Getting this right means visually diverse, well-packed wallpapers.
- **Test**: Verify hero count logic (1 vs 2 based on 50% threshold). Verify greedy fill packs narrowest-first. Verify no repeats across monitors until exhausted. Verify new pool generation when current pool is exhausted.

### 5. Composer (`composer.py`)
- **Spec**: [[specs/image-rescaling-and-layout|Image Rescaling and Layout]], [[specs/output-overflow-handling|Output Overflow Handling]]
- Implement `compose(selected_images, output_size, background_color, monitor_name)`:
  - Create RGB canvas of `output_size`, filled with `background_color`
  - Precompute total width of all images (scaled) + borders
  - Compute `start_offset = (canvas_width - total_width) / 2` (centered layout)
  - Rescale each image with `img.thumbnail(output_size, Image.LANCZOS)`, preserving aspect ratio
  - Place images left-to-right from `start_offset` with 20px borders
  - Handle overflow: if next image exceeds canvas width, stop and save
  - Save intermediate snapshots after each placed image (numeric suffix)
  - Save final output to `output/<width>x<height>_<monitor_name>/height_width_uuid.<ext>`
  - Generate UUID for filename using `uuid.uuid4()`
  - Preserve all previous wallpapers in directory (no overwrite)
- **Why**: This is the rendering engine. The precomputed centered layout replaces the current left-aligned, buggy implementation.
- **Test**: Verify images are centered (equal background on both sides). Verify LANCZOS resampling. Verify aspect ratios preserved. Verify `height_width_uuid` naming. Verify overflow stops placement and saves correctly.

### 6. Wallpaper Setter (`wallpaper.py`)
- **Spec**: [[specs/per-monitor-wallpaper-setting|Per-Monitor Wallpaper Setting]]
- Implement `apply_wallpapers(monitors)`:
  - For each monitor, find its output directory
  - Select most recently generated wallpaper (by file modification time)
  - Run `osascript -e 'tell application "System Events" to set picture of every desktop to "<absolute_path>"'` per monitor
  - Skip monitors with no output directory or no wallpapers, with warning
  - Use absolute file paths only
- **Why**: Completes the workflow — without this, the user has to manually run osascript commands.
- **Test**: Verify absolute paths are used. Verify missing directories produce warnings not errors. Verify most recent file is selected.

### 7. CLI Entry Point (`cli.py`)
- **Spec**: [[specs/cli-commands|CLI Commands]]
- Implement three subcommands using `argparse`:
  - `load <image_path>`: Call image_loader.load(), print dimensions
  - `generate`: Call monitor detection → selection → composer for each monitor, print summary
  - `apply`: Call wallpaper setter, print results
- Each command runs independently
- Each command prints a user-facing summary of what it did
- **Why**: Replaces the hardcoded `__main__` block with a proper interface. This is the user-facing surface area.
- **Test**: Verify each command works independently. Verify output summaries are printed.

---

## Acceptance Criteria

### Image Load Operation
- [ ] Source image copied to `images/` directory
- [ ] Image dimensions read from file header only (no full pixel load)
- [ ] Common formats supported (JPEG, PNG, TIFF)
- [ ] Original filename preserved
- [ ] 1,000+ images handled efficiently

### Wallpaper Generation Algorithm
- [ ] Monitors detected via `screeninfo.get_monitors()`
- [ ] Random ~20% pool generated for selection
- [ ] One hero randomly selected from pool
- [ ] Second hero selected when first hero < 50% canvas width
- [ ] Second hero filtered to fit remaining canvas width
- [ ] Remaining space filled greedily (narrowest-first)
- [ ] New pools generated if current pool exhausted with space remaining
- [ ] All layout offsets precomputed before image processing
- [ ] Images centered on canvas with equal background on both sides
- [ ] Each monitor receives unique images; repeats only when catalog exhausted
- [ ] Image dimensions read from headers only during selection

### Image Rescaling and Layout
- [ ] Multiple images placed on single canvas
- [ ] Original aspect ratio maintained after rescaling
- [ ] Images arranged left-to-right with 20-pixel gap
- [ ] Canvas background filled with specified color
- [ ] Output saved to `output/<width>x<height>_<monitor_name>/`
- [ ] Filename follows `height_width_uuid.<ext>` naming convention
- [ ] Previous wallpapers preserved in monitor directory
- [ ] LANCZOS resampling used

### Output Overflow Handling
- [ ] System detects when next image would exceed canvas width
- [ ] Overflow-causing image not placed on canvas
- [ ] Intermediate snapshots saved after each successfully placed image
- [ ] On overflow: final output saved and remaining images skipped

### Per-Monitor Wallpaper Setting
- [ ] Each monitor matched to its output directory
- [ ] Most recent wallpaper selected from monitor's directory
- [ ] Each monitor receives own wallpaper via `osascript`
- [ ] Monitors without wallpapers skipped with warning
- [ ] Absolute file paths used

### CLI Commands
- [ ] `load` ingests image and reports dimensions
- [ ] `generate` produces wallpaper for each detected monitor
- [ ] `apply` sets wallpapers on desktop per monitor
- [ ] Each command runs independently
- [ ] Each command provides user-facing summary output
