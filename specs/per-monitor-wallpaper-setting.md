# Per-Monitor Wallpaper Setting

## Topic of Concern
The apply operation sets a different generated wallpaper on each connected monitor.

## Overview
After wallpapers have been generated into per-monitor output directories, the apply command sets each monitor's desktop wallpaper to its most recently generated image using macOS AppleScript.

## Functional Requirements

### Monitor Matching
- Detects all connected monitors via `screeninfo.get_monitors()`
- Matches each monitor to its output directory (`output/<width>x<height>_<monitor_name>/`)
- Selects a random wallpaper from that directory

### Wallpaper Application
- Uses the macOS `osascript` command to set wallpapers
- Sets each monitor's wallpaper individually rather than one image across all desktops
- The image path provided to `osascript` must be an **absolute file path**

### Error Handling
- If a monitor has no output directory or no generated wallpapers, it is skipped with a warning
- If a monitor directory exists but the image file is missing, a warning is displayed

## Acceptance Criteria
- [ ] Each connected monitor is matched to its output directory
- [ ] A random wallpaper from each monitor's directory is selected
- [ ] Each monitor receives its own wallpaper via `osascript`
- [ ] Monitors without generated wallpapers are skipped with a warning
- [ ] Absolute file paths are used for the `osascript` command

## Related Specs
- [[cli-commands|CLI Commands]] - The `apply` command triggers this operation
- [[wallpaper-generation-algorithm|Wallpaper Generation Algorithm]] - Generates the wallpapers that are applied
- [[image-rescaling-and-layout|Image Rescaling and Layout]] - Defines the output directory structure
