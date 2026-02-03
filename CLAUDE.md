# Creative Compositor

Streamlit app for compositing hero images with overlays (static and video) across multiple aspect ratios.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Runs at `http://localhost:8501`

## Project Structure

```
creative-compositor/
├── app.py                      # Lightweight router (45 lines)
├── compositor.py               # Core compositing engine
├── config.json                 # Position storage
├── requirements.txt
├── CLAUDE.md
├── README.md
│
├── tools/                      # Feature modules
│   ├── __init__.py
│   └── overlay_tool.py         # Overlay compositor (476 lines)
│
├── ui/                         # Shared UI components
│   ├── __init__.py
│   ├── styles.py               # CSS theme (201 lines)
│   ├── preview.py              # Preview rendering (51 lines)
│   └── components.py           # Reusable components (future)
│
├── utils/                      # Shared utilities
│   ├── __init__.py
│   └── file_scanner.py         # Asset scanning (83 lines)
│
├── .streamlit/
│   └── config.toml             # Theme configuration
│
├── inputs/
│   ├── heroes/1x1/             # 1x1 hero images
│   ├── heroes/9x16/            # 9x16 hero images
│   └── overlays/
│       ├── static/1x1/         # Static PNG overlays (1x1)
│       ├── static/9x16/        # Static PNG overlays (9x16)
│       ├── video/1x1/          # Video overlays (1x1)
│       └── video/9x16/         # Video overlays (9x16)
│
└── outputs/                    # Rendered composites
    ├── 1x1/
    └── 9x16/
```

## Design System

Channel 4-inspired dark theme with green accent.

### Colors

| Variable | Hex | Usage |
|----------|-----|-------|
| `--accent` | `#7cb518` | Buttons, highlights, icons |
| `--accent-hover` | `#8fc926` | Hover states |
| `--bg-dark` | `#0a0a0f` | Page background |
| `--bg-card` | `#16161f` | Cards, sidebar |
| `--bg-elevated` | `#1e1e2a` | Elevated surfaces |
| `--border` | `#2a2a3a` | Subtle borders |
| `--text-primary` | `#f0f0f0` | Main text |
| `--text-muted` | `#8a8a9a` | Secondary text |

### Theme Config

Streamlit theme is set in `.streamlit/config.toml`:
- Primary: `#598c14`
- Background: `#0a0a0f`
- Secondary background: `#16161f`

### Icons

Uses Streamlit Material icons (`:material/icon_name:`) for buttons. Header uses inline SVG (Lucide-style layers icon).

## Architecture

**Modular Design:**
- **app.py**: Lightweight router that delegates to tools
- **tools/**: Independent feature modules (each has a `render()` function)
- **ui/**: Shared UI components (styles, preview, future widgets)
- **utils/**: Shared utilities (file scanning, validation, etc.)
- **compositor.py**: Core rendering engine (used by all tools)

**Adding New Tools:**
1. Create `tools/your_tool.py` with a `render(comp, inputs, base_path)` function
2. Import and call it from `app.py`
3. Share UI components from `ui/` and utilities from `utils/`

## Key Files

- **app.py**: Router (45 lines) - delegates to tools
- **compositor.py**: Image/video compositing engine
- **tools/overlay_tool.py**: Overlay compositor with positioning UI
- **ui/styles.py**: Channel 4 theme CSS and icon definitions
- **ui/preview.py**: Live preview rendering
- **utils/file_scanner.py**: File scanning and subfolder organization

## Development Philosophy

This is a learning project. Priorities:
1. Clean architecture over quick hacks
2. Explain the "why" behind technical decisions
3. Iterate and refactor as we learn
4. Build modular, scalable features

## Notes

- Positions are stored per-hero, per-overlay, per-aspect-ratio
- Supports 1x1 and 9x16 aspect ratios
- Video overlays require ffmpeg
