import os
import shutil
from PIL import Image

IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")


def load(source_path):
    """Ingest an image file into the images/ directory and return its dimensions.

    Copies the file and reads width/height from the file header only (no pixel loading).
    Returns (width, height) tuple.
    """
    os.makedirs(IMAGES_DIR, exist_ok=True)
    filename = os.path.basename(source_path)
    dest_path = os.path.join(IMAGES_DIR, filename)
    source_abs = os.path.abspath(source_path)
    dest_abs = os.path.abspath(dest_path)
    if source_abs != dest_abs:
        shutil.copy2(source_path, dest_path)

    with Image.open(dest_path) as img:
        width, height = img.size
    return width, height


def catalog(images_dir=None):
    """Scan all images in a directory and return their paths and dimensions.

    Reads dimensions from file headers only — no pixel data is loaded.
    Returns a list of dicts: [{"path": str, "width": int, "height": int}, ...]
    """
    if images_dir is None:
        images_dir = IMAGES_DIR

    supported_extensions = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp", ".webp"}
    results = []

    if not os.path.isdir(images_dir):
        return results

    for filename in os.listdir(images_dir):
        ext = os.path.splitext(filename)[1].lower()
        if ext not in supported_extensions:
            continue
        filepath = os.path.join(images_dir, filename)
        try:
            with Image.open(filepath) as img:
                w, h = img.size
            results.append({"path": filepath, "width": w, "height": h})
        except Exception:
            continue

    return results
