"""
File Scanner Utilities
Functions for scanning input directories and managing subfolder structures
"""

from pathlib import Path


def scan_inputs(base_path: Path) -> dict:
    """Scan input folders and return found files organized by subfolder"""

    def scan_with_subfolders(path: Path, extensions: list) -> dict:
        """Scan directory for files, organizing by subfolder"""
        result = {"root": [], "subfolders": {}}

        if not path.exists():
            return result

        # Get files in root
        for ext in extensions:
            result["root"].extend(list(path.glob(f"*.{ext}")))

        # Get subfolders and their files
        for subfolder in path.iterdir():
            if subfolder.is_dir():
                files = []
                for ext in extensions:
                    files.extend(list(subfolder.glob(f"*.{ext}")))
                if files:
                    result["subfolders"][subfolder.name] = files

        return result

    image_exts = ["png", "jpg", "jpeg", "PNG", "JPG", "JPEG"]
    video_exts = ["mov", "MOV", "mp4", "MP4"]

    return {
        "heroes_1x1": scan_with_subfolders(base_path / "inputs/heroes/1x1", image_exts),
        "heroes_9x16": scan_with_subfolders(base_path / "inputs/heroes/9x16", image_exts),
        "overlays_static_1x1": scan_with_subfolders(base_path / "inputs/overlays/static/1x1", ["png", "PNG"]),
        "overlays_static_9x16": scan_with_subfolders(base_path / "inputs/overlays/static/9x16", ["png", "PNG"]),
        "overlays_video_1x1": scan_with_subfolders(base_path / "inputs/overlays/video/1x1", video_exts),
        "overlays_video_9x16": scan_with_subfolders(base_path / "inputs/overlays/video/9x16", video_exts)
    }


def flatten_files(file_dict: dict) -> list[Path]:
    """Flatten subfolder structure into single file list"""
    files = list(file_dict.get("root", []))
    for subfolder_files in file_dict.get("subfolders", {}).values():
        files.extend(subfolder_files)
    return files


def get_subfolders(file_dict: dict) -> list[str]:
    """Get list of available subfolders"""
    subfolders = list(file_dict.get("subfolders", {}).keys())
    return ["all"] + sorted(subfolders) if subfolders else ["all"]


def filter_by_subfolder(file_dict: dict, subfolder: str) -> list[Path]:
    """Filter files by subfolder selection"""
    if subfolder == "all":
        return flatten_files(file_dict)
    else:
        return file_dict.get("subfolders", {}).get(subfolder, [])


def get_file_label(file_path: Path, file_dict: dict) -> str:
    """Get display label for file showing subfolder if applicable"""
    # Check if file is in a subfolder
    for subfolder_name, files in file_dict.get("subfolders", {}).items():
        if file_path in files:
            return f"[{subfolder_name}] {file_path.name}"
    return file_path.name


def get_all_subfolders(*file_dicts) -> list[str]:
    """Get combined list of all unique subfolders across multiple file dicts"""
    all_subfolders = set()
    for file_dict in file_dicts:
        all_subfolders.update(file_dict.get("subfolders", {}).keys())
    return ["all"] + sorted(all_subfolders) if all_subfolders else ["all"]


def scan_fonts(base_path: Path) -> list[Path]:
    """
    Scan assets/fonts/ directory for font files

    Returns:
        List of Path objects for TTF/OTF font files
    """
    fonts_path = base_path / "assets/fonts"

    # Create directory if it doesn't exist
    if not fonts_path.exists():
        fonts_path.mkdir(parents=True, exist_ok=True)
        return []

    fonts = []
    # Scan for TrueType and OpenType fonts
    for ext in ["ttf", "TTF", "otf", "OTF"]:
        fonts.extend(list(fonts_path.glob(f"*.{ext}")))

    return sorted(fonts)


def scan_font_families(base_path: Path) -> dict:
    """
    Scan fonts and group by family with available styles

    Returns:
        Dict mapping family names to available style variants
        Example: {
            "Arial": {
                "Regular": Path("Arial.ttf"),
                "Bold": Path("Arial-Bold.ttf"),
                "Italic": Path("Arial-Italic.ttf")
            }
        }
    """
    fonts = scan_fonts(base_path)
    families = {}

    for font_path in fonts:
        font_name = font_path.stem  # Filename without extension

        # Detect style from filename
        style = "Regular"
        family_name = font_name

        # Common naming patterns
        if "-Bold" in font_name or " Bold" in font_name:
            if "-BoldItalic" in font_name or " Bold Italic" in font_name:
                style = "Bold Italic"
                family_name = font_name.replace("-BoldItalic", "").replace(" Bold Italic", "")
            else:
                style = "Bold"
                family_name = font_name.replace("-Bold", "").replace(" Bold", "")
        elif "-Italic" in font_name or " Italic" in font_name:
            style = "Italic"
            family_name = font_name.replace("-Italic", "").replace(" Italic", "")
        elif "-Regular" in font_name or " Regular" in font_name:
            style = "Regular"
            family_name = font_name.replace("-Regular", "").replace(" Regular", "")

        # Group by family
        if family_name not in families:
            families[family_name] = {}

        families[family_name][style] = font_path

    return families
