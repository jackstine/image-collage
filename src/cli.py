import argparse
import sys

from src.image_loader import load, catalog
from src.monitor import detect_monitors, get_output_dir
from src.selection import select_for_monitors
from src.composer import compose
from src.wallpaper import apply_wallpapers


def cmd_load(args):
    """Ingest an image into the images/ directory and display its dimensions."""
    width, height = load(args.image_path)
    print(f"Loaded: {args.image_path}")
    print(f"  Dimensions: {width}x{height}")


def cmd_generate(args):
    """Generate wallpapers for each detected monitor."""
    count = args.count
    images = catalog()
    if not images:
        print("No images found in images/ directory. Use 'load' to add images first.", file=sys.stderr)
        sys.exit(1)

    monitors = detect_monitors()
    if not monitors:
        print("No monitors detected.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(images)} images, {len(monitors)} monitor(s), generating {count} per monitor")

    bg_color = (0, 0, 0)

    remaining = None
    for cycle in range(1, count + 1):
        if count > 1:
            print(f"\n  Cycle {cycle}/{count}:")

        if remaining is not None:
            # Pass per-monitor remaining catalogs from prior cycle
            selections, remaining = select_for_monitors(images, monitors, remaining_catalogs=remaining)
        else:
            selections, remaining = select_for_monitors(images, monitors)

        for monitor in monitors:
            name = monitor["name"]
            selected = selections.get(name, [])
            if not selected:
                print(f"    {name}: No images selected, skipping.")
                continue

            output_dir = get_output_dir(monitor)
            output_size = (monitor["width"], monitor["height"])
            output_path = compose(selected, output_size, output_dir, bg_color)
            print(f"    {name} ({monitor['width']}x{monitor['height']}): "
                  f"{len(selected)} images -> {output_path}")


def cmd_apply(args):
    """Apply the most recent wallpaper to each monitor."""
    results = apply_wallpapers()
    for r in results:
        if r["status"] == "applied":
            print(f"  {r['monitor']}: Applied {r['wallpaper']}")
        elif r["status"] == "skipped":
            print(f"  {r['monitor']}: Skipped (no wallpapers)")
        else:
            print(f"  {r['monitor']}: Failed")


def main():
    parser = argparse.ArgumentParser(description="ImageRescaler - Multi-monitor wallpaper generator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    load_parser = subparsers.add_parser("load", help="Ingest an image into the images/ directory")
    load_parser.add_argument("image_path", help="Path to the image file to load")

    gen_parser = subparsers.add_parser("generate", help="Generate wallpapers for all detected monitors")
    gen_parser.add_argument("count", nargs="?", type=int, default=1, help="Number of wallpapers to generate per monitor (default: 1)")

    subparsers.add_parser("apply", help="Apply most recent wallpapers to desktop")

    args = parser.parse_args()

    if args.command == "load":
        cmd_load(args)
    elif args.command == "generate":
        cmd_generate(args)
    elif args.command == "apply":
        cmd_apply(args)


if __name__ == "__main__":
    main()
