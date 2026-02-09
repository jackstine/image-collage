import os
import uuid
from PIL import Image

from src.selection import scaled_width


def compose(selected_images, output_size, output_dir, background_color=(255, 255, 255), border=20):
    """Compose selected images onto a centered canvas and save to output_dir.

    1. Precompute layout (scaled widths, total width, centering offset)
    2. Create canvas, rescale and place images
    3. Save with height_width_uuid.<ext> naming

    Returns the path to the saved output image.
    """
    canvas_width, canvas_height = output_size

    # --- Precompute layout ---
    layout = []
    for img_info in selected_images:
        sw = scaled_width(img_info["width"], img_info["height"], canvas_height)
        layout.append({"info": img_info, "scaled_width": sw})

    total_images_width = sum(item["scaled_width"] for item in layout)
    total_borders = border * (len(layout) - 1) if len(layout) > 1 else 0
    total_width = total_images_width + total_borders

    start_offset = max(0, (canvas_width - total_width) / 2)

    # --- Create canvas and place images ---
    canvas = Image.new("RGB", output_size, background_color)
    x_cursor = int(start_offset)

    for i, item in enumerate(layout):
        img_path = item["info"]["path"]
        with Image.open(img_path) as img:
            img.thumbnail(output_size, Image.Resampling.LANCZOS)
            canvas.paste(img, (x_cursor, 0))
            x_cursor += img.size[0] + border

    # --- Save output ---
    os.makedirs(output_dir, exist_ok=True)
    file_uuid = uuid.uuid4().hex[:8]
    filename = f"{canvas_height}_{canvas_width}_{file_uuid}.jpg"
    output_path = os.path.join(output_dir, filename)
    canvas.save(output_path, "JPEG", quality=95)

    return output_path
