import os
import uuid
from PIL import Image



def compose(selected_images, output_size, output_dir, background_color=(255, 255, 255), border=20):
    """Compose selected images onto a centered canvas and save to output_dir.

    1. Precompute layout (scaled widths, total width, centering offset)
    2. Create canvas, rescale and place images
    3. Save with height_width_uuid.<ext> naming

    Returns the path to the saved output image.
    """
    canvas_width, canvas_height = output_size

    # --- Pass 1: Thumbnail all images to get actual pixel sizes ---
    thumbnails = []
    for img_info in selected_images:
        img = Image.open(img_info["path"])
        img.thumbnail(output_size, Image.Resampling.LANCZOS)
        thumbnails.append(img)

    # --- Precompute layout from actual sizes ---
    total_images_width = sum(img.size[0] for img in thumbnails)
    total_borders = border * (len(thumbnails) - 1) if len(thumbnails) > 1 else 0
    total_width = total_images_width + total_borders

    # Drop trailing images that would overflow the canvas
    while total_width > canvas_width and len(thumbnails) > 1:
        removed = thumbnails.pop()
        removed.close()
        total_images_width -= removed.size[0]
        total_borders = border * (len(thumbnails) - 1) if len(thumbnails) > 1 else 0
        total_width = total_images_width + total_borders

    start_offset = max(0, (canvas_width - total_width) // 2)

    # --- Pass 2: Place images on canvas ---
    canvas = Image.new("RGB", output_size, background_color)
    x_cursor = start_offset

    for img in thumbnails:
        y_offset = max(0, (canvas_height - img.size[1]) // 2)
        canvas.paste(img, (x_cursor, y_offset))
        x_cursor += img.size[0] + border
        img.close()

    # --- Save output ---
    os.makedirs(output_dir, exist_ok=True)
    file_uuid = uuid.uuid4().hex[:8]
    filename = f"{canvas_height}_{canvas_width}_{file_uuid}.jpg"
    output_path = os.path.join(output_dir, filename)
    canvas.save(output_path, "JPEG", quality=95)

    return output_path
