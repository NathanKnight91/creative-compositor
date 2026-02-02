"""
Creative Compositor - Core rendering logic
Handles static PNG overlays and video MOV overlays on hero images
"""

import subprocess
import json
from pathlib import Path
from PIL import Image
from typing import Optional
import shutil
import tempfile


class Compositor:
    def __init__(self, base_path: Path = None):
        self.base_path = base_path or Path(__file__).parent
        self.config_path = self.base_path / "config.json"
        self.config = self.load_config()
    
    def load_config(self) -> dict:
        """Load position config or return defaults"""
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        return {
            "1x1_static": {"x": 0, "y": 0, "scale": 1.0},
            "1x1_video": {"x": 0, "y": 0, "scale": 1.0, "loop_count": 1},
            "9x16_static": {"x": 0, "y": 0, "scale": 1.0},
            "9x16_video": {"x": 0, "y": 0, "scale": 1.0, "loop_count": 1}
        }
    
    def save_config(self):
        """Save current config to file"""
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)
    
    def get_position(self, format_type: str, overlay_type: str = "static") -> dict:
        """Get overlay position for a format and overlay type"""
        key = f"{format_type}_{overlay_type}"
        defaults = {"x": 0, "y": 0, "scale": 1.0, "loop_count": 1} if overlay_type == "video" else {"x": 0, "y": 0, "scale": 1.0}
        return self.config.get(key, defaults)
    
    def set_position(self, format_type: str, x: int, y: int, scale: float = 1.0, loop_count: int = 1, overlay_type: str = "static"):
        """Set overlay position for a format and overlay type"""
        key = f"{format_type}_{overlay_type}"
        if overlay_type == "video":
            self.config[key] = {"x": x, "y": y, "scale": scale, "loop_count": loop_count}
        else:
            self.config[key] = {"x": x, "y": y, "scale": scale}
        self.save_config()
    
    def composite_static(
        self, 
        hero_path: Path, 
        overlay_path: Path, 
        output_path: Path,
        position: dict
    ) -> bool:
        """Composite a static PNG overlay onto a hero image"""
        try:
            hero = Image.open(hero_path).convert("RGBA")
            overlay = Image.open(overlay_path).convert("RGBA")
            
            # Scale overlay if needed
            if position.get("scale", 1.0) != 1.0:
                scale = position["scale"]
                new_size = (int(overlay.width * scale), int(overlay.height * scale))
                overlay = overlay.resize(new_size, Image.Resampling.LANCZOS)
            
            # Create output canvas
            result = hero.copy()
            
            # Paste overlay at position
            x, y = int(position["x"]), int(position["y"])
            result.paste(overlay, (x, y), overlay)
            
            # Save as PNG
            output_path.parent.mkdir(parents=True, exist_ok=True)
            result.save(output_path, "PNG")
            return True
            
        except Exception as e:
            print(f"Error compositing static: {e}")
            return False
    
    def composite_video_overlay(
        self,
        hero_path: Path,
        overlay_path: Path,
        output_path: Path,
        position: dict,
        duration: float = None
    ) -> bool:
        """
        Composite a video overlay (MOV with alpha) onto a static hero image.
        Output is H.264 MP4 compliant with META specs.
        """
        try:
            # Get overlay video duration if not specified
            if duration is None:
                base_duration = self._get_video_duration(overlay_path)
            else:
                base_duration = duration

            # Apply loop count
            loop_count = position.get("loop_count", 1)
            final_duration = base_duration * loop_count

            x, y = int(position["x"]), int(position["y"])
            scale = position.get("scale", 1.0)

            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Build FFmpeg command
            # Uses overlay filter with alpha channel support
            scale_filter = f"scale=iw*{scale}:ih*{scale}" if scale != 1.0 else "null"

            cmd = [
                "ffmpeg", "-y",
                "-loop", "1", "-i", str(hero_path),      # Loop static hero
                "-stream_loop", str(loop_count - 1), "-i", str(overlay_path),  # Loop overlay
                "-filter_complex",
                f"[1:v]{scale_filter},format=rgba[ovr];[0:v][ovr]overlay={x}:{y}:shortest=1",
                "-t", str(final_duration),
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", "18",
                "-pix_fmt", "yuv420p",                   # META compatibility
                "-movflags", "+faststart",               # Web optimization
                "-an",                                    # No audio
                str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"FFmpeg error: {result.stderr}")
                return False
            
            return True
            
        except Exception as e:
            print(f"Error compositing video: {e}")
            return False
    
    def _get_video_duration(self, video_path: Path) -> float:
        """Get duration of a video file in seconds"""
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(video_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        try:
            return float(result.stdout.strip())
        except:
            return 5.0  # Default fallback

    def extract_first_frame(self, video_path: Path, frame_position: float = 0.0) -> Optional[Image.Image]:
        """
        Extract frame from video as PIL Image for preview

        Args:
            video_path: Path to video file
            frame_position: Position in video (0.0 = start, 1.0 = end)
        """
        try:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp_path = tmp.name

            # Calculate timestamp based on position
            if frame_position > 0:
                duration = self._get_video_duration(video_path)
                timestamp = duration * frame_position
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", str(timestamp),
                    "-i", str(video_path),
                    "-vframes", "1",
                    "-f", "image2",
                    tmp_path
                ]
            else:
                cmd = [
                    "ffmpeg", "-y",
                    "-i", str(video_path),
                    "-vframes", "1",
                    "-f", "image2",
                    tmp_path
                ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                return None

            img = Image.open(tmp_path).convert("RGBA")
            Path(tmp_path).unlink()  # Clean up temp file
            return img

        except Exception as e:
            print(f"Error extracting frame: {e}")
            return None

    def get_hero_dimensions(self, hero_path: Path) -> tuple:
        """Get dimensions of a hero image"""
        with Image.open(hero_path) as img:
            return img.size
    
    def render_all(
        self,
        heroes_1x1: list[Path],
        heroes_9x16: list[Path],
        overlays_static_1x1: list[Path],
        overlays_static_9x16: list[Path],
        overlays_video_1x1: list[Path],
        overlays_video_9x16: list[Path],
        progress_callback=None
    ) -> dict:
        """
        Render all combinations of heroes and overlays.
        Format-specific overlays are paired with matching heroes.
        Returns dict with success/failure counts.
        """
        results = {"success": 0, "failed": 0, "outputs": []}

        all_tasks = []

        # Build task list - 1x1 heroes with 1x1 overlays
        for hero in heroes_1x1:
            format_type = "1x1"

            for overlay in overlays_static_1x1:
                pos = self.get_position(format_type, "static")
                output_name = f"{hero.stem}_{overlay.stem}.png"
                output_path = self.base_path / "outputs" / format_type / output_name
                all_tasks.append(("static", hero, overlay, output_path, pos, format_type))

            for overlay in overlays_video_1x1:
                pos = self.get_position(format_type, "video")
                output_name = f"{hero.stem}_{overlay.stem}.mp4"
                output_path = self.base_path / "outputs" / format_type / output_name
                all_tasks.append(("video", hero, overlay, output_path, pos, format_type))

        # 9x16 heroes with 9x16 overlays
        for hero in heroes_9x16:
            format_type = "9x16"

            for overlay in overlays_static_9x16:
                pos = self.get_position(format_type, "static")
                output_name = f"{hero.stem}_{overlay.stem}.png"
                output_path = self.base_path / "outputs" / format_type / output_name
                all_tasks.append(("static", hero, overlay, output_path, pos, format_type))

            for overlay in overlays_video_9x16:
                pos = self.get_position(format_type, "video")
                output_name = f"{hero.stem}_{overlay.stem}.mp4"
                output_path = self.base_path / "outputs" / format_type / output_name
                all_tasks.append(("video", hero, overlay, output_path, pos, format_type))
        
        # Execute tasks
        total = len(all_tasks)
        for i, task in enumerate(all_tasks):
            task_type, hero, overlay, output_path, pos, fmt = task
            
            if progress_callback:
                progress_callback(i + 1, total, f"Rendering {output_path.name}")
            
            if task_type == "static":
                success = self.composite_static(hero, overlay, output_path, pos)
            else:
                success = self.composite_video_overlay(hero, overlay, output_path, pos)
            
            if success:
                results["success"] += 1
                results["outputs"].append(str(output_path))
            else:
                results["failed"] += 1
        
        return results


def scan_inputs(base_path: Path) -> dict:
    """Scan input folders and return found files"""
    return {
        "heroes_1x1": list((base_path / "inputs/heroes/1x1").glob("*.png")) +
                      list((base_path / "inputs/heroes/1x1").glob("*.jpg")) +
                      list((base_path / "inputs/heroes/1x1").glob("*.jpeg")),
        "heroes_9x16": list((base_path / "inputs/heroes/9x16").glob("*.png")) +
                       list((base_path / "inputs/heroes/9x16").glob("*.jpg")) +
                       list((base_path / "inputs/heroes/9x16").glob("*.jpeg")),
        "overlays_static_1x1": list((base_path / "inputs/overlays/static/1x1").glob("*.png")),
        "overlays_static_9x16": list((base_path / "inputs/overlays/static/9x16").glob("*.png")),
        "overlays_video_1x1": list((base_path / "inputs/overlays/video/1x1").glob("*.mov")) +
                              list((base_path / "inputs/overlays/video/1x1").glob("*.MOV")),
        "overlays_video_9x16": list((base_path / "inputs/overlays/video/9x16").glob("*.mov")) +
                               list((base_path / "inputs/overlays/video/9x16").glob("*.MOV"))
    }


if __name__ == "__main__":
    # CLI test
    comp = Compositor()
    inputs = scan_inputs(comp.base_path)
    print("Found inputs:")
    for k, v in inputs.items():
        print(f"  {k}: {len(v)} files")
