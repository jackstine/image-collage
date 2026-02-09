import random


def scaled_dimensions(image_width, image_height, canvas_width, canvas_height):
    """Calculate the dimensions an image will occupy after thumbnail scaling.

    thumbnail() constrains to BOTH canvas width and height, preserving aspect ratio.
    Returns (scaled_width, scaled_height).
    """
    if image_width == 0 or image_height == 0:
        return (0, 0)
    ratio = min(canvas_width / image_width, canvas_height / image_height)
    return (image_width * ratio, image_height * ratio)


def get_scaled_width(image_width, image_height, canvas_width, canvas_height):
    """Convenience: return just the scaled width after thumbnail scaling."""
    return scaled_dimensions(image_width, image_height, canvas_width, canvas_height)[0]


def generate_pool(catalog, pool_ratio=0.2):
    """Randomly sample ~20% of the catalog as a selection pool.

    Returns the pool sorted by scaled_width ascending (set by caller via catalog entries).
    """
    pool_size = max(1, int(len(catalog) * pool_ratio))
    pool = random.sample(catalog, min(pool_size, len(catalog)))
    return pool


def _sw(img, canvas_width, canvas_height):
    """Shorthand for get_scaled_width."""
    return get_scaled_width(img["width"], img["height"], canvas_width, canvas_height)


def select_images(pool, canvas_width, canvas_height, border=20):
    """Select images from a pool using hero selection + greedy fill.

    1. Filter pool to images that fit within the canvas
    2. Randomly pick one hero image
    3. If hero's scaled width < 50% of canvas, pick a second hero that fits remaining space
    4. Greedily fill remaining space with narrowest-first from the rest of the pool

    Returns a list of selected image dicts from the pool.
    """
    if not pool:
        return []

    # Filter to images that actually fit on the canvas
    available = [img for img in pool if _sw(img, canvas_width, canvas_height) <= canvas_width]
    if not available:
        return []

    selected = []
    used_width = 0

    # --- Hero 1: random pick ---
    hero1 = random.choice(available)
    available.remove(hero1)
    hero1_sw = _sw(hero1, canvas_width, canvas_height)
    selected.append(hero1)
    used_width = hero1_sw

    # --- Hero 2: if hero1 < 50% of canvas width ---
    if hero1_sw < canvas_width * 0.5 and available:
        remaining = canvas_width - used_width - border
        candidates = [
            img for img in available
            if _sw(img, canvas_width, canvas_height) <= remaining
        ]
        if candidates:
            hero2 = random.choice(candidates)
            available.remove(hero2)
            hero2_sw = _sw(hero2, canvas_width, canvas_height)
            selected.append(hero2)
            used_width += border + hero2_sw

    # --- Greedy fill: narrowest first from remaining pool ---
    available.sort(key=lambda img: _sw(img, canvas_width, canvas_height))
    for img in available:
        img_sw = _sw(img, canvas_width, canvas_height)
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
    results = {}

    for monitor in monitors:
        canvas_width = monitor["width"]
        canvas_height = monitor["height"]

        selected = []
        working_catalog = list(catalog)

        while True:
            pool = generate_pool(working_catalog)
            newly_selected = select_images(pool, canvas_width, canvas_height, border)

            if not newly_selected:
                break

            selected.extend(newly_selected)

            # Remove selected from working catalog
            for img in newly_selected:
                if img in working_catalog:
                    working_catalog.remove(img)

            # Check if canvas is full enough
            total_sw = sum(
                get_scaled_width(img["width"], img["height"], canvas_width, canvas_height)
                for img in selected
            )
            total_borders = border * (len(selected) - 1) if len(selected) > 1 else 0
            if total_sw + total_borders >= canvas_width * 0.9:
                break

            if not working_catalog:
                break

        results[monitor["name"]] = selected

    return results
