# CLI Commands

## Topic of Concern
The CLI provides commands to load images, generate wallpapers, and apply them to monitors.

## Overview
The Python script exposes three commands that form the core workflow: loading source images, generating composed wallpapers per monitor, and applying them to the desktop.

## Functional Requirements

### `load`
- Accepts a source image file path
- Copies the image into the `images/` directory
- Reads and displays the image dimensions (width x height) from the file header
- See [[image-load-operation|Image Load Operation]] for full details

### `generate [count]`
- Accepts an optional `count` argument (default: `1`) specifying how many wallpapers to generate per monitor
- For each count cycle, runs a **completely independent** selection and composition pass for every monitor
- Example: `generate 5` with 2 monitors produces 10 wallpapers total (5 per monitor), each with a fresh pool and hero selection
- Detects all connected monitors via `screeninfo`
- Runs the [[wallpaper-generation-algorithm|Wallpaper Generation Algorithm]] for each monitor per cycle
- Composes a wallpaper per monitor using [[image-rescaling-and-layout|Image Rescaling and Layout]]
- Saves each wallpaper to `output/<width>x<height>_<monitor_name>/`
- Displays a summary of what was generated (monitor name, resolution, output path, cycle number)

### `apply`
- Sets the most recently generated wallpaper for each monitor on the desktop
- Uses per-monitor wallpaper setting via `osascript`
- See [[per-monitor-wallpaper-setting|Per-Monitor Wallpaper Setting]] for full details

## Acceptance Criteria
- [ ] `load` ingests an image and reports its dimensions
- [ ] `generate` accepts an optional count argument (defaults to 1)
- [ ] `generate` produces `count` wallpapers for each detected monitor, each from an independent selection cycle
- [ ] `apply` sets the wallpapers on the desktop per monitor
- [ ] Each command can be run independently
- [ ] Each command provides user-facing output summarizing what it did
