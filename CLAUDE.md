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
├── app.py              # Streamlit frontend
├── compositor.py       # Core compositing logic
├── requirements.txt    # Dependencies
├── .streamlit/
│   └── config.toml     # Theme configuration
├── inputs/
│   ├── heroes/         # Source hero images
│   └── overlays/
│       ├── static/     # PNG overlays
│       └── video/      # Video overlays
└── outputs/            # Rendered composites
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

## Key Files

- **app.py**: Frontend with position controls, preview, render triggers. CSS injection block at top defines custom styling.
- **compositor.py**: Image/video compositing engine. Handles scaling, positioning, format conversion.

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
