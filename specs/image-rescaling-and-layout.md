# Image Rescaling and Layout

## Topic of Concern
The image rescaling system combines multiple images into a single horizontally-laid-out canvas.

## Overview
The core functionality of ImageRescaler is to accept a list of input images and compose them onto a single output canvas. Each image is rescaled to fit within the output dimensions while preserving its original aspect ratio, then placed sequentially from left to right on the canvas.

## Functional Requirements

### Input
- A list of image file paths (absolute paths)
- An output size as a `(width, height)` tuple defining the canvas dimensions
- An optional background color as an `(R, G, B)` tuple (defaults to white `(255, 255, 255)`)

### Output Directory Structure
- Composed images are saved to `output/<width>x<height>_<monitor_name>/` (e.g., `output/3840x1080_HDMI-1/`)
- The monitor name is read from `screeninfo` (`monitor.name`)
- The output filename follows the pattern: `height_width_uuid.<ext>` (e.g., `1080_3840_a1b2c3d4.jpg`)
- All previously generated wallpapers are kept (history is preserved)

### Image Rescaling
- Each input image is resized using thumbnail mode with LANCZOS resampling
- The thumbnail is constrained to the output size dimensions
- The original aspect ratio of each image is preserved during rescaling

### Horizontal Layout
- Images are placed on the canvas from **left to right**
- The first image is placed at horizontal offset `0`
- Each subsequent image is placed at a horizontal offset equal to the right edge of the previous image plus a **20-pixel border**
- All images are vertically aligned to the **top** of the canvas (vertical offset `0`)

### Canvas
- The canvas is a new RGB image of the specified `output_size`
- The canvas is pre-filled with the specified `background_color`
- Any area not covered by an image remains the background color

## Acceptance Criteria
- [ ] Multiple images can be loaded from file paths and placed onto a single canvas
- [ ] Each image maintains its original aspect ratio after rescaling
- [ ] Images are arranged left-to-right with a 20-pixel gap between them
- [ ] The first image starts at the left edge of the canvas
- [ ] The canvas background is filled with the specified color
- [ ] The output image is saved to `output/<width>x<height>_<monitor_name>/`
- [ ] The output filename follows the `height_width_uuid.<ext>` naming convention
- [ ] Previous wallpapers are preserved in the monitor directory
- [ ] LANCZOS resampling is used for high-quality rescaling

## Related Specs
- [[output-overflow-handling|Output Overflow Handling]] - Describes behavior when images exceed canvas width
