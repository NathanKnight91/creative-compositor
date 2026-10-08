# Creative Compositor — Explainer Video

A ~58 second [Remotion](https://www.remotion.dev/) video that explains what Creative Compositor does, styled with the app's Channel 4-inspired theme.

## Scenes

1. **Intro** — title and tagline
2. **The problem** — heroes × overlays × formats multiplies into lots of manual work
3. **Step 1: Inputs** — the `inputs/` folder layout and `utils/file_scanner.py`
4. **Step 2: Positioning** — X/Y/scale/frame sliders, live preview, saved to `config.json`
5. **Step 3: Engine** — Pillow path for PNG overlays, FFmpeg path for video overlays
6. **Tool 2: Text overlays** — three lines, each with its own font style and size
7. **Step 4: Batch render** — `RENDER ALL` → `outputs/<format>/<subfolder>/`
8. **Architecture** — `app.py` router → `tools/` → `compositor.py`, plus `ui/` and `utils/`
9. **Outro** — how to run it

## Usage

```bash
cd explainer
npm install
npm run studio   # preview and edit in the browser
npm run render   # writes out/explainer.mp4 (1920x1080, 30fps)
```

## Structure

```
explainer/
├── src/
│   ├── index.ts          # Registers the Remotion root
│   ├── Root.tsx          # Composition definition (1920x1080 @ 30fps)
│   ├── Explainer.tsx     # Scene order and durations
│   ├── theme.ts          # Colours mirrored from ui/styles.py
│   ├── components.tsx    # Shared pieces (scene shell, slider, hero art, icon)
│   └── scenes/           # One file per scene
└── remotion.config.ts
```

To change the pacing, edit the `SCENES` list in `src/Explainer.tsx`. The total length is calculated from it.
