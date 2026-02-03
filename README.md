# Creative Compositor

> Professional video and image compositing tool for social media creative workflows

[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Streamlit-powered compositor for overlaying static and animated graphics onto hero images. Built for marketing teams running multi-format social campaigns (1x1, 9x16) with precise positioning control and batch rendering.

## Features

### Core Compositing
- ✅ **Static PNG overlays** - Transparency-aware compositing
- ✅ **Video overlays** - MOV/MP4 with alpha channel support
- ✅ **Multiple formats** - 1x1 (Instagram) and 9x16 (Stories) aspect ratios
- ✅ **Real-time preview** - Visual positioning before render

### Advanced Controls
- 🎬 **Video frame scrubber** - Preview any frame for accurate positioning (perfect for delayed animations)
- 🔁 **Loop control** - Set video overlay loop count with duration preview
- 📐 **Negative positioning** - Shift overlays beyond canvas bounds for precise alignment
- ⚖️ **Scale slider** - Resize overlays independently
- 🎯 **Separate static/video positions** - Different alignment per overlay type

### Workflow Optimization
- 📁 **Subfolder organization** - Group assets by campaign/version
- 🎛️ **Format filtering** - Render only 1x1 or 9x16 selectively
- 🗂️ **Custom output naming** - Organize render batches (e.g., `outputs/9x16/v2-finals/`)
- 🚀 **Batch rendering** - Process all combinations automatically
- 💾 **Position memory** - Saves per-format, per-overlay-type

## Quick Start

```bash
# Clone and install
git clone https://github.com/NathanKnight91/creative-compositor.git
cd creative-compositor
pip install -r requirements.txt

# Install ffmpeg (required for video overlays)
brew install ffmpeg  # macOS
# OR: sudo apt install ffmpeg  # Ubuntu

# Run
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

## Usage

### 1. Organize Your Assets

```
creative-compositor/
├── inputs/
│   ├── heroes/
│   │   ├── 1x1/
│   │   │   ├── campaign-a/         # Optional subfolders
│   │   │   │   └── hero_v1.png
│   │   │   └── campaign-b/
│   │   └── 9x16/
│   │       └── ...
│   └── overlays/
│       ├── static/
│       │   ├── 1x1/
│       │   │   └── logo.png
│       │   └── 9x16/
│       └── video/
│           ├── 1x1/
│           │   └── animation.mov   # Must have alpha channel
│           └── 9x16/
└── outputs/                         # Rendered files appear here
```

**Supported formats:**
- Heroes: PNG, JPG, JPEG
- Static overlays: PNG (with transparency)
- Video overlays: MOV, MP4 (must include alpha channel for transparency)

### 2. Position Overlays

#### 1x1 Tab
1. Select hero and overlay from dropdowns
2. Use **subfolder filters** to narrow down assets
3. For video overlays:
   - Drag **Preview Frame Position** slider to find the right frame (0-100%)
   - Adjust **Loop Count** (shows final video duration)
4. Adjust **X/Y position** and **Scale**
5. Click **Save 1x1 Position**

#### 9x16 Tab
Same workflow as 1x1, but for Stories/Reels format.

**Pro tip:** Static and video overlays save separate positions. Switch between them in the dropdown to fine-tune each type.

### 3. Render

#### Render Tab
1. **Format filters:** Check 1x1, 9x16, or both
2. **Overlay types:** Select static and/or video
3. **Subfolder filters:** Choose specific campaigns/sets or "all"
4. **Output name:** Enter custom subfolder (e.g., "final-v3")
5. Click **RENDER ALL**

Output structure: `outputs/{format}/{your-custom-name}/hero_overlay.{png|mp4}`

## Example Workflow

```
1. Upload Valentine's Day heroes to inputs/heroes/9x16/valentines/
2. Add animated logo to inputs/overlays/video/9x16/brand-assets/
3. In 9x16 tab:
   - Filter: Hero folder = "valentines", Overlay folder = "brand-assets"
   - Scrub video to 50% (animation peak)
   - Position at X: 540, Y: 100, Scale: 0.8
   - Set Loop Count = 3 (9 second final video)
   - Save position
4. Render tab:
   - Format: ✓ 9x16 only
   - Subfolder: valentines + brand-assets
   - Output name: "valentines-v1"
   - Render
5. Find outputs in: outputs/9x16/valentines-v1/
```

## Project Structure

```
├── app.py                      # Lightweight router
├── compositor.py               # Core rendering engine
├── config.json                 # Position memory (auto-generated)
│
├── tools/                      # Feature modules
│   └── overlay_tool.py         # Overlay compositor tool
│
├── ui/                         # Shared UI components
│   ├── styles.py               # CSS theme (Channel 4-inspired)
│   └── preview.py              # Live preview rendering
│
├── utils/                      # Shared utilities
│   └── file_scanner.py         # Asset scanning
│
├── .streamlit/
│   └── config.toml             # Streamlit theme config
│
├── inputs/                     # Your assets (not in repo)
└── outputs/                    # Rendered files (not in repo)
```

**Modular architecture** - Each tool is isolated in `tools/`, making it easy to add new features (text overlay, templates, etc.) without touching existing code.

## Requirements

- **Python 3.8+**
- **ffmpeg** - Required for video overlay compositing
- **Pillow** - Image processing
- **Streamlit** - Web interface

## Tips

- **Video overlays:** Export with alpha channel (ProRes 4444, PNG sequence rendered to MOV, or H.264 with alpha)
- **Negative positioning:** Drag sliders into negative values to crop alpha padding
- **Frame scrubber:** Essential for overlays with delayed animations (swipes, fades)
- **Subfolder naming:** Use clear names like `q1-2024`, `test-batch`, `finals`

## Contributing

Issues and PRs welcome. For major changes, open an issue first.

## License

MIT © Nathan Knight

---

Built with [Streamlit](https://streamlit.io/) • Powered by [FFmpeg](https://ffmpeg.org/)
