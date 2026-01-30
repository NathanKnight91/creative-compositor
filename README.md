# Creative Compositor

Streamlit app for compositing hero images with overlays (static PNG and video) across multiple aspect ratios.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- Composite hero images with static PNG overlays
- Video overlay support (requires ffmpeg)
- Multiple aspect ratios: 1x1, 9x16
- Per-image position controls with real-time preview
- Batch rendering

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/creative-compositor.git
cd creative-compositor

# Install dependencies
pip install -r requirements.txt

# For video overlay support, install ffmpeg
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
# Windows: https://ffmpeg.org/download.html
```

## Usage

1. Create your input folders:
```
creative-compositor/
├── inputs/
│   ├── heroes/         # Your hero images (PNG, JPG)
│   └── overlays/
│       ├── static/     # PNG overlays
│       └── video/      # Video overlays (MP4, MOV)
└── outputs/            # Rendered composites appear here
```

2. Run the app:
```bash
streamlit run app.py
```

3. Open `http://localhost:8501` in your browser

4. Select heroes and overlays, adjust positions, and render

## Requirements

- Python 3.8+
- ffmpeg (for video overlays)

## License

MIT
