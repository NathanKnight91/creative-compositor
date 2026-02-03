"""
UI Preview Components
Functions for generating live preview composites
"""

from pathlib import Path
from PIL import Image
from typing import Optional


def create_preview(hero_path: Path, overlay_path: Path, position: dict, frame_position: float = 0.0, compositor=None) -> Image.Image:
    """
    Create a preview composite image

    Args:
        hero_path: Path to hero image
        overlay_path: Path to overlay (static PNG or video)
        position: Dict with x, y, scale keys
        frame_position: Position in video (0.0 = start, 1.0 = end) for video overlays
        compositor: Compositor instance for video frame extraction

    Returns:
        PIL Image of the composite preview
    """
    hero = Image.open(hero_path).convert("RGBA")

    # Handle video overlays - extract frame at specified position
    if overlay_path.suffix.lower() in ['.mov', '.mp4']:
        if compositor is None:
            # Fallback: show hero only if no compositor provided
            return hero

        overlay = compositor.extract_first_frame(overlay_path, frame_position)
        if overlay is None:
            # Fallback: show hero only if frame extraction fails
            return hero
    else:
        overlay = Image.open(overlay_path).convert("RGBA")

    # Scale overlay
    scale = position.get("scale", 1.0)
    if scale != 1.0:
        new_size = (int(overlay.width * scale), int(overlay.height * scale))
        overlay = overlay.resize(new_size, Image.Resampling.LANCZOS)

    # Composite
    result = hero.copy()
    x, y = int(position["x"]), int(position["y"])

    result.paste(overlay, (x, y), overlay)
    return result
