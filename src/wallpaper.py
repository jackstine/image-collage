import os
import subprocess
import sys

from src.monitor import detect_monitors, get_output_dir


def get_most_recent_wallpaper(output_dir):
    """Return the most recently modified image file in the output directory."""
    if not os.path.isdir(output_dir):
        return None

    files = []
    for f in os.listdir(output_dir):
        filepath = os.path.join(output_dir, f)
        if os.path.isfile(filepath) and f.lower().endswith((".jpg", ".jpeg", ".png")):
            files.append(filepath)

    if not files:
        return None

    return max(files, key=os.path.getmtime)


def apply_wallpaper(image_path):
    """Set a single image as the desktop wallpaper on macOS via osascript."""
    abs_path = os.path.abspath(image_path)
    script = f'tell application "System Events" to set picture of every desktop to "{abs_path}"'
    subprocess.run(["osascript", "-e", script], check=True)


def apply_wallpapers():
    """Set the most recent wallpaper for each monitor.

    Returns a list of dicts describing what was applied or skipped.
    """
    monitors = detect_monitors()
    results = []

    for monitor in monitors:
        output_dir = get_output_dir(monitor)
        wallpaper = get_most_recent_wallpaper(output_dir)

        if wallpaper is None:
            print(f"Warning: No wallpapers found for {monitor['name']} "
                  f"({monitor['width']}x{monitor['height']}), skipping.",
                  file=sys.stderr)
            results.append({"monitor": monitor["name"], "status": "skipped"})
            continue

        try:
            apply_wallpaper(wallpaper)
            results.append({
                "monitor": monitor["name"],
                "status": "applied",
                "wallpaper": wallpaper,
            })
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to set wallpaper for {monitor['name']}: {e}",
                  file=sys.stderr)
            results.append({"monitor": monitor["name"], "status": "failed"})

    return results
