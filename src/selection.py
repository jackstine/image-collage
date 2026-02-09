import random


def scaled_width(image_width, image_height, monitor_height):
    """Calculate the width an image will occupy when scaled to fit monitor height."""
    if image_height == 0:
        return 0
    return image_width * (monitor_height / image_height)


def generate_pool(catalog, pool_ratio=0.2):
    """Randomly sample ~20% of the catalog as a selection pool.

    Returns the pool sorted by scaled_width ascending (set by caller via catalog entries).
    """
    pool_size = max(1, int(len(catalog) * pool_ratio))
    pool = random.sample(catalog, min(pool_size, len(catalog)))
    return pool


def select_images(pool, canvas_width, monitor_height, border=20):
    """Select images from a pool using hero selection + greedy fill.

    1. Randomly pick one hero image
    2. If hero's scaled width < 50% of canvas, pick a second hero that fits remaining space
    3. Greedily fill remaining space with narrowest-first from the rest of the pool

    Returns a list of selected image dicts from the pool.
    """
    if not pool:
        return []

    available = list(pool)
    selected = []
    used_width = 0

    # --- Hero 1: random pick ---
    hero1 = random.choice(available)
    available.remove(hero1)
    hero1_sw = scaled_width(hero1["width"], hero1["height"], monitor_height)
    selected.append(hero1)
    used_width = hero1_sw

    # --- Hero 2: if hero1 < 50% of canvas width ---
    if hero1_sw < canvas_width * 0.5 and available:
        remaining = canvas_width - used_width - border
        candidates = [
            img for img in available
            if scaled_width(img["width"], img["height"], monitor_height) <= remaining
        ]
        if candidates:
            hero2 = random.choice(candidates)
            available.remove(hero2)
            hero2_sw = scaled_width(hero2["width"], hero2["height"], monitor_height)
            selected.append(hero2)
            used_width += border + hero2_sw

    # --- Greedy fill: narrowest first from remaining pool ---
    available.sort(key=lambda img: scaled_width(img["width"], img["height"], monitor_height))
    for img in available:
        img_sw = scaled_width(img["width"], img["height"], monitor_height)
        needed = border + img_sw if selected else img_sw
        if used_width + needed <= canvas_width:
            selected.append(img)
            used_width += needed

    return selected


def select_for_monitors(catalog, monitors, border=20):
    """Select images for each monitor, removing used images between monitors.

    Returns a dict mapping monitor name to list of selected image dicts.
    Allows repeats only when the catalog is exhausted.
    """
    remaining_catalog = list(catalog)
    results = {}

    for monitor in monitors:
        canvas_width = monitor["width"]
        monitor_height = monitor["height"]

        if not remaining_catalog:
            remaining_catalog = list(catalog)

        selected = []
        working_catalog = list(remaining_catalog)

        while True:
            pool = generate_pool(working_catalog)
            newly_selected = select_images(pool, canvas_width, monitor_height, border)

            if not newly_selected:
                break

            selected.extend(newly_selected)

            # Remove selected from working catalog
            for img in newly_selected:
                if img in working_catalog:
                    working_catalog.remove(img)

            # Check if canvas is full enough
            total_sw = sum(
                scaled_width(img["width"], img["height"], monitor_height)
                for img in selected
            )
            total_borders = border * (len(selected) - 1) if len(selected) > 1 else 0
            if total_sw + total_borders >= canvas_width * 0.9:
                break

            if not working_catalog:
                break

        # Remove used images from remaining catalog
        for img in selected:
            if img in remaining_catalog:
                remaining_catalog.remove(img)

        results[monitor["name"]] = selected

    return results
