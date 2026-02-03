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


def create_text_preview(hero_path: Path, text: str, font_path: Path, font_size: int, color: str, position: dict) -> Image.Image:
    """
    Create a preview with text overlay

    Args:
        hero_path: Path to hero image
        text: Text to overlay
        font_path: Path to font file (TTF/OTF)
        font_size: Font size in pixels
        color: Hex color code (e.g., "#FFFFFF")
        position: Dict with x, y, alignment keys

    Returns:
        PIL Image with text overlay
    """
    from PIL import ImageDraw, ImageFont

    # Load hero image
    hero = Image.open(hero_path).convert("RGBA")

    # Create drawing context
    draw = ImageDraw.Draw(hero)

    # Load font
    if font_path and font_path.exists():
        font = ImageFont.truetype(str(font_path), font_size)
    else:
        # Fallback to default font if no font file provided
        font = ImageFont.load_default()

    # Get position and alignment
    x = int(position.get("x", 0))
    y = int(position.get("y", 0))
    alignment = position.get("alignment", "mm")

    # Convert hex color to RGB tuple
    # Color picker returns "#FFFFFF", PIL needs (255, 255, 255)
    color_rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    # Draw text
    draw.text(
        xy=(x, y),
        text=text,
        font=font,
        fill=color_rgb,
        anchor=alignment
    )

    return hero


def create_multiline_text_preview(
    hero_path: Path,
    lines: list[dict],
    font_family: dict,
    color: str,
    position: dict,
    line_spacing: int = 10
) -> Image.Image:
    """
    Create a preview with multiple text lines with different styles

    Args:
        hero_path: Path to hero image
        lines: List of dicts with text, size, style keys
        font_family: Dict of font style variants
        color: Hex color code
        position: Dict with x, y, alignment keys
        line_spacing: Vertical spacing between lines

    Returns:
        PIL Image with multi-line text overlay
    """
    from PIL import ImageDraw, ImageFont

    # Load hero image
    hero = Image.open(hero_path).convert("RGBA")
    draw = ImageDraw.Draw(hero)

    # Convert hex color to RGB
    color_rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    # Get base position
    base_x = int(position.get("x", 0))
    base_y = int(position.get("y", 0))
    alignment = position.get("alignment", "mm")

    # Calculate total height and load fonts
    total_height = 0
    loaded_lines = []

    for line_data in lines:
        text = line_data.get("text", "")
        if not text:  # Skip empty lines
            continue

        size = line_data.get("size", 48)
        style = line_data.get("style", "Regular")

        # Load appropriate font variant
        font_path = font_family.get(style, font_family.get("Regular"))
        if font_path and font_path.exists():
            font = ImageFont.truetype(str(font_path), size)
        else:
            font = ImageFont.load_default()

        # Get text dimensions
        bbox = draw.textbbox((0, 0), text, font=font, anchor=alignment)
        text_height = bbox[3] - bbox[1]

        loaded_lines.append({
            "text": text,
            "font": font,
            "height": text_height
        })

        total_height += text_height

    # Add spacing
    if len(loaded_lines) > 1:
        total_height += line_spacing * (len(loaded_lines) - 1)

    # Adjust starting Y based on alignment
    if "m" in alignment:  # Middle
        current_y = base_y - (total_height // 2)
    elif "b" in alignment:  # Bottom
        current_y = base_y - total_height
    else:  # Top
        current_y = base_y

    # Draw each line
    for line_info in loaded_lines:
        draw.text(
            xy=(base_x, current_y),
            text=line_info["text"],
            font=line_info["font"],
            fill=color_rgb,
            anchor=alignment
        )
        current_y += line_info["height"] + line_spacing

    return hero
