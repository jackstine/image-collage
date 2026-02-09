# Output Overflow Handling

## Topic of Concern
The output overflow system saves intermediate results when images exceed canvas width.

## Overview
When placing images left-to-right on the canvas, the system detects if the next image would extend beyond the canvas width. When overflow is detected, the system saves the current canvas state and stops processing further images. Additionally, intermediate snapshots are saved after each image is successfully placed.

## Functional Requirements

### Overflow Detection
- Before placing each image (after the first), the system calculates whether the image's right edge would exceed the canvas width
- The right edge is calculated as: `current_horizontal_offset + border + image_width`
- If the right edge exceeds the canvas width, the image is **not placed**

### Intermediate Saves
- After each image is **successfully placed** on the canvas, an intermediate file is saved
- The intermediate file path is the output path with a numeric suffix appended (e.g., `output.jpg1.jpg`, `output.jpg2.jpg`)
- The numeric suffix corresponds to the image's position in the input list (1-indexed)

### Final Save on Overflow
- When an overflow is detected, the canvas is saved to the **original output path** (without numeric suffix)
- Processing stops immediately after saving — remaining images in the list are skipped

### Final Save Without Overflow
- If all images fit on the canvas without overflow, the canvas is saved to the original output path after all images are placed

## Acceptance Criteria
- [ ] The system detects when the next image would exceed the canvas width
- [ ] An image that would cause overflow is not placed on the canvas
- [ ] Intermediate snapshots are saved after each successfully placed image
- [ ] Intermediate files use a numeric suffix based on image position
- [ ] On overflow, the final output is saved to the original output path
- [ ] On overflow, remaining images are skipped
- [ ] If no overflow occurs, the final output is saved after all images are placed

## Related Specs
- [[image-rescaling-and-layout|Image Rescaling and Layout]] - Describes the core rescaling and layout logic
