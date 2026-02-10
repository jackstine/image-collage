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

### Centered Layout (Two-Pass Composition)
- **Pass 1**: Thumbnail all selected images to get **actual pixel sizes** (avoids float-to-integer rounding drift)
- Drop trailing images if actual total width exceeds canvas width
- Calculate total width from actual thumbnail sizes plus borders
- Compute `start_offset = (canvas_width - total_width) / 2`
- **Pass 2**: Place images on canvas starting from `start_offset`, proceeding left to right

### Multi-Monitor
- Each monitor receives its own independent copy of the full image catalog (the image collection)
- Pool generation and image selection for each monitor operates on that monitor's own collection
- Images may repeat across monitors since each monitor draws from the full set independently

### Multi-Cycle Persistence
- When `generate count` is greater than 1, each monitor's image collection persists across cycles
- Images selected in cycle N are removed from that monitor's collection for cycle N+1
- This ensures different images are used in each cycle for the same monitor
- A monitor's collection resets to the full catalog only when it is exhausted

### Scaled Width Calculation
- For any image, the scaling ratio is: `min(canvas_width / original_width, canvas_height / original_height)`
- The scaled width is: `original_width * ratio`
- This accounts for `thumbnail()` behavior which constrains to **both** canvas width and height, not just height
- Images wider than the canvas are scaled down by width, not height
- This value determines how much horizontal canvas space an image will occupy
- Read from the file header only — no full image loading during selection

### Image Fit Filtering
- Before hero selection, images whose scaled width exceeds the canvas width are excluded from the pool
- This prevents any single image from overflowing the canvas

## Acceptance Criteria
- [ ] Monitor dimensions are detected via `screeninfo.get_monitors()`
- [ ] A random pool of ~20% of available images is generated for selection
- [ ] One hero image is randomly selected from the pool
- [ ] A second hero is selected if the first hero's scaled width is less than 50% of canvas width
- [ ] The second hero is filtered to only images that fit within the remaining canvas width
- [ ] Remaining space is filled greedily with narrowest-first from the pool
- [ ] A new pool is generated if the current pool is exhausted and space remains
- [ ] Images that exceed canvas width are filtered out before selection
- [ ] Layout uses actual thumbnail pixel sizes (two-pass composition) to prevent clipping
- [ ] Trailing images are dropped if actual total exceeds canvas width
- [ ] Images are centered on the canvas with equal background on both sides
- [ ] Each monitor receives its own independent copy of the full image catalog for selection
- [ ] Images may repeat across monitors
- [ ] Across multiple cycles, each monitor's collection persists and selected images are removed
- [ ] A monitor's collection resets only when exhausted
- [ ] Image dimensions are read from file headers only (no full pixel loading during selection)

## Related Specs
- [[image-load-operation|Image Load Operation]] - Populates the `images/` directory and reads dimensions
- [[image-rescaling-and-layout|Image Rescaling and Layout]] - Handles the actual image rescaling and canvas composition
- [[macos-wallpaper-integration|macOS Wallpaper Integration]] - Sets the generated wallpaper on the desktop
