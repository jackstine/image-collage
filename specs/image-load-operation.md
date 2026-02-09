# Image Load Operation

## Topic of Concern
The load operation ingests an image file and catalogs it in the images directory.

## Overview
The load operation accepts an image file path, reads its dimensions from the file header (without loading full pixel data), and places the file into the `images/` directory. This enables fast cataloging of image metadata for later sorting, filtering, and composition.

## Functional Requirements

### File Ingestion
- Accepts a source image file path as input
- Copies the image file into the `images/` directory
- Preserves the original filename

### Dimension Reading
- Reads image width and height in pixels from the file header
- Does **not** load the full image pixel data into memory
- Works with common image formats (JPEG, PNG, TIFF, etc.)

### Performance
- Header-only reads enable processing of 1,000+ images with minimal time and memory
- No full image decoding is performed during the load operation

## Acceptance Criteria
- [ ] A source image file can be ingested and copied to the `images/` directory
- [ ] The image's width and height in pixels are read from the file header
- [ ] Full pixel data is not loaded into memory during the load operation
- [ ] Common image formats (JPEG, PNG) are supported
- [ ] The original filename is preserved in the `images/` directory

## Related Specs
- [[image-rescaling-and-layout|Image Rescaling and Layout]] - Uses loaded images for canvas composition
