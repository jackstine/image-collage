import os
from screeninfo import get_monitors

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")


def detect_monitors():
    """Detect all connected monitors via screeninfo.

    Returns a list of dicts with name, width, height, x, y, is_primary.
    On macOS, monitor.name is None so we use 'monitor<index>' as fallback.
    """
    monitors = get_monitors()
    results = []
    for i, m in enumerate(monitors):
        name = m.name if m.name else f"monitor{i}"
        results.append({
            "name": name,
            "width": m.width,
            "height": m.height,
            "x": m.x,
            "y": m.y,
            "is_primary": m.is_primary,
        })
    return results


def get_output_dir(monitor):
    """Return the output directory path for a monitor and create it if needed.

    Format: output/<width>x<height>_<name>/
    """
    dirname = f"{monitor['width']}x{monitor['height']}_{monitor['name']}"
    dirpath = os.path.join(OUTPUT_DIR, dirname)
    os.makedirs(dirpath, exist_ok=True)
    return dirpath
