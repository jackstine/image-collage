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

### `generate`
- Detects all connected monitors via `screeninfo`
- Runs the [[wallpaper-generation-algorithm|Wallpaper Generation Algorithm]] for each monitor
- Composes a wallpaper per monitor using [[image-rescaling-and-layout|Image Rescaling and Layout]]
- Saves each wallpaper to `output/<width>x<height>_<monitor_name>/`
- Displays a summary of what was generated (monitor name, resolution, output path)

### `apply`
- Sets the most recently generated wallpaper for each monitor on the desktop
- Uses per-monitor wallpaper setting via `osascript`
- See [[per-monitor-wallpaper-setting|Per-Monitor Wallpaper Setting]] for full details

## Acceptance Criteria
- [ ] `load` ingests an image and reports its dimensions
- [ ] `generate` produces a wallpaper for each detected monitor
- [ ] `apply` sets the wallpapers on the desktop per monitor
- [ ] Each command can be run independently
- [ ] Each command provides user-facing output summarizing what it did
