# Wallpaper Generation Algorithm

## Topic of Concern
The wallpaper generation algorithm selects and arranges images from the images directory to fill each monitor's dimensions.

## Overview
For each connected monitor, the system detects its resolution via `screeninfo`, then selects images from the `images/` directory using a pool-based selection algorithm. Hero images are randomly chosen for visual variety, and remaining space is filled greedily. The final composition is centered on the canvas.

## Functional Requirements

### Monitor Detection
- Uses the `screeninfo` package (`get_monitors()`) to detect all connected monitors
- Reads each monitor's width, height, position, and name
- A wallpaper is generated for each detected monitor

### Pool Generation
- All images in the `images/` directory are cataloged with their scaled widths (based on the target monitor height)
- A pool of approximately **20% of available images** is randomly sampled from the full set
- Only the pool is sorted by scaled width; the full set is unordered

### Hero Selection
1. **First hero** — randomly pick one image from the pool
2. **Second hero decision** — if the first hero's scaled width is **less than 50% of the canvas width**, select a second hero:
   - Calculate `remaining_width = canvas_width - hero1_scaled_width - border`
   - Filter the pool to images whose `scaled_width <= remaining_width`
   - Randomly pick one image from that filtered set
3. If the first hero's scaled width is **50% or more** of the canvas width, skip the second hero

### Greedy Fill
- After hero images are placed, calculate the remaining horizontal space
- From the remaining images in the pool, sort by scaled width ascending (narrowest first)
- Greedily add images (plus border spacing) until no more images fit in the remaining space
- If the pool is exhausted and space remains, generate a **new pool** from remaining unused images and repeat from [[#Hero Selection]]

### Centered Layout
- All layout math is **precomputed before any image processing**
- Calculate total width of all selected images plus borders between them
- Compute `start_offset = (canvas_width - total_width) / 2`
- Place images starting from `start_offset`, proceeding left to right

### Multi-Monitor
- Each monitor receives a unique set of images — images used on one monitor are removed from the available set for subsequent monitors
- Repeats are only allowed if the total number of images requested across all monitors exceeds the number of images in the `images/` directory

### Scaled Width Calculation
- For any image, the scaled width is: `original_width * (monitor_height / original_height)`
- This value determines how much horizontal canvas space an image will occupy
- Read from the file header only — no full image loading during selection

## Acceptance Criteria
- [ ] Monitor dimensions are detected via `screeninfo.get_monitors()`
- [ ] A random pool of ~20% of available images is generated for selection
- [ ] One hero image is randomly selected from the pool
- [ ] A second hero is selected if the first hero's scaled width is less than 50% of canvas width
- [ ] The second hero is filtered to only images that fit within the remaining canvas width
- [ ] Remaining space is filled greedily with narrowest-first from the pool
- [ ] A new pool is generated if the current pool is exhausted and space remains
- [ ] All layout offsets are precomputed before image processing
- [ ] Images are centered on the canvas with equal background on both sides
- [ ] Each monitor gets unique images; repeats only occur when images are exhausted
- [ ] Image dimensions are read from file headers only (no full pixel loading during selection)

## Related Specs
- [[image-load-operation|Image Load Operation]] - Populates the `images/` directory and reads dimensions
- [[image-rescaling-and-layout|Image Rescaling and Layout]] - Handles the actual image rescaling and canvas composition
- [[macos-wallpaper-integration|macOS Wallpaper Integration]] - Sets the generated wallpaper on the desktop
