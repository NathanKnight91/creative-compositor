"""
Creative Compositor - Streamlit UI
Visual overlay positioning and batch rendering
"""

import streamlit as st
from pathlib import Path
from PIL import Image
import io
from compositor import Compositor, scan_inputs


# Page config
st.set_page_config(
    page_title="Creative Compositor",
    page_icon=None,
    layout="wide"
)

# Custom CSS for professional polish - Channel 4 inspired
st.markdown("""
<style>
/* Color variables - Channel 4 inspired palette */
:root {
    --accent: #7cb518;
    --accent-hover: #8fc926;
    --bg-dark: #0a0a0f;
    --bg-card: #16161f;
    --bg-elevated: #1e1e2a;
    --border: #2a2a3a;
    --text-primary: #f0f0f0;
    --text-muted: #8a8a9a;
}

/* Base styling */
.stApp {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Muted section headers */
.section-header {
    color: var(--text-muted);
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}

/* Monospace for position values */
.mono-value {
    font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
    color: var(--accent);
}

/* Button styling */
.stButton > button {
    border: 1px solid var(--border);
    transition: all 0.15s ease;
}

.stButton > button:hover {
    border-color: var(--accent);
}

/* Slider track accent color */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, var(--accent), #598c14) !important;
}

/* Progress bar styling */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent), #598c14) !important;
}

/* Subtle dividers */
hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 16px 0;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    border-right: 1px solid var(--border);
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 1px solid var(--border);
}

.stTabs [data-baseweb="tab"] {
    padding: 10px 20px;
    border-radius: 6px 6px 0 0;
    color: var(--text-muted);
}

.stTabs [aria-selected="true"] {
    background-color: var(--bg-card);
    color: var(--text-primary);
}

/* Metric styling - improved readability */
[data-testid="stMetric"] {
    background: var(--bg-elevated);
    padding: 16px 20px;
    border-radius: 8px;
    border: 1px solid var(--border);
}

[data-testid="stMetric"] label {
    color: var(--text-muted) !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-size: 2rem !important;
    font-weight: 600 !important;
}

/* Caption styling */
.stCaption {
    font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
    color: var(--text-muted);
    font-size: 0.8rem;
}

/* Expander styling */
.streamlit-expanderHeader {
    background-color: var(--bg-card);
    border-radius: 6px;
}

/* JSON display styling */
[data-testid="stJson"] {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 12px;
}

/* Image container - cleaner styling */
[data-testid="stImage"] {
    background: transparent;
    border: none;
    padding: 0;
}

[data-testid="stImage"] img {
    border-radius: 8px;
    border: 1px solid var(--border);
}

/* Icon helper class */
.icon {
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.icon svg {
    width: 18px;
    height: 18px;
    stroke: currentColor;
    stroke-width: 2;
    fill: none;
}

/* Title styling */
h1 {
    display: flex;
    align-items: center;
    gap: 12px;
}

/* Selectbox styling */
[data-baseweb="select"] {
    border-radius: 6px;
}

/* Warning/info boxes */
.stAlert {
    border-radius: 6px;
    border: none;
}

/* Checkbox styling */
.stCheckbox label {
    color: var(--text-primary);
}
</style>
""", unsafe_allow_html=True)

# SVG icons (Lucide-style)
ICONS = {
    "layers": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>',
    "folder": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-.82-1.2A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13c0 1.1.9 2 2 2Z"></path></svg>',
    "square": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"></rect></svg>',
    "smartphone": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="20" x="5" y="2" rx="2" ry="2"></rect><path d="M12 18h.01"></path></svg>',
    "play": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>',
    "check": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>',
    "refresh": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path><path d="M3 3v5h5"></path><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"></path><path d="M16 16h5v5"></path></svg>',
}

# Initialize
BASE_PATH = Path(__file__).parent
comp = Compositor(BASE_PATH)


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


def create_preview(hero_path: Path, overlay_path: Path, position: dict, frame_position: float = 0.0) -> Image.Image:
    """Create a preview composite image"""
    hero = Image.open(hero_path).convert("RGBA")

    # Handle video overlays - extract frame at specified position
    if overlay_path.suffix.lower() in ['.mov', '.mp4']:
        overlay = comp.extract_first_frame(overlay_path, frame_position)
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


def main():
    st.markdown(f'<h1><span style="color: #7cb518">{ICONS["layers"]}</span> Creative Compositor</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #8a8a9a; margin-top: -10px;">Position overlays on hero images and batch render all combinations</p>', unsafe_allow_html=True)

    # Scan for files
    inputs = scan_inputs(BASE_PATH)

    # Sidebar - file status
    with st.sidebar:
        st.markdown(f'<div class="icon" style="font-size: 1.2rem; font-weight: 600; margin-bottom: 16px;">{ICONS["folder"]} Input Files</div>', unsafe_allow_html=True)

        st.markdown('<p class="section-header">Heroes</p>', unsafe_allow_html=True)
        st.write(f"1x1: {len(flatten_files(inputs['heroes_1x1']))} files")
        st.write(f"9x16: {len(flatten_files(inputs['heroes_9x16']))} files")

        st.markdown('<p class="section-header" style="margin-top: 16px;">Overlays (1x1)</p>', unsafe_allow_html=True)
        st.write(f"Static: {len(flatten_files(inputs['overlays_static_1x1']))} files")
        st.write(f"Video: {len(flatten_files(inputs['overlays_video_1x1']))} files")

        st.markdown('<p class="section-header" style="margin-top: 16px;">Overlays (9x16)</p>', unsafe_allow_html=True)
        st.write(f"Static: {len(flatten_files(inputs['overlays_static_9x16']))} files")
        st.write(f"Video: {len(flatten_files(inputs['overlays_video_9x16']))} files")

        st.markdown('<div style="border-top: 1px solid #2a2a3a; margin: 20px 0;"></div>', unsafe_allow_html=True)

        heroes_1x1_all = flatten_files(inputs['heroes_1x1'])
        heroes_9x16_all = flatten_files(inputs['heroes_9x16'])
        overlays_1x1_all = flatten_files(inputs['overlays_static_1x1']) + flatten_files(inputs['overlays_video_1x1'])
        overlays_9x16_all = flatten_files(inputs['overlays_static_9x16']) + flatten_files(inputs['overlays_video_9x16'])

        total_1x1 = len(heroes_1x1_all) * len(overlays_1x1_all)
        total_9x16 = len(heroes_9x16_all) * len(overlays_9x16_all)
        st.metric("Total outputs", total_1x1 + total_9x16)

        st.markdown('<div style="border-top: 1px solid #2a2a3a; margin: 20px 0;"></div>', unsafe_allow_html=True)

        if st.button(f"Refresh Files", icon=":material/refresh:"):
            st.rerun()
    
    # Main area - tabs for each format
    tab1, tab2, tab3 = st.tabs([
        f"1x1 Position",
        f"9x16 Position",
        f"Render"
    ])
    
    # --- 1x1 Tab ---
    with tab1:
        st.markdown(f'<h3 style="display: flex; align-items: center; gap: 10px; color: #f0f0f0;"><span style="color: #7cb518">{ICONS["square"]}</span> 1x1 Format Positioning</h3>', unsafe_allow_html=True)

        heroes_1x1_flat = flatten_files(inputs['heroes_1x1'])
        overlays_static_1x1_flat = flatten_files(inputs['overlays_static_1x1'])
        overlays_video_1x1_flat = flatten_files(inputs['overlays_video_1x1'])

        if not heroes_1x1_flat:
            st.warning("No 1x1 heroes found. Add images to `inputs/heroes/1x1/`")
        elif not overlays_static_1x1_flat and not overlays_video_1x1_flat:
            st.warning("No 1x1 overlays found. Add files to `inputs/overlays/static/1x1/` or `inputs/overlays/video/1x1/`")
        else:
            col1, col2 = st.columns([1, 2])

            with col1:
                # Select preview files
                hero_1x1 = st.selectbox(
                    "Preview Hero",
                    heroes_1x1_flat,
                    format_func=lambda x: x.name,
                    key="hero_1x1"
                )

                # Combine static and video overlays for preview
                all_overlays_1x1 = overlays_static_1x1_flat + overlays_video_1x1_flat
                overlay_preview = st.selectbox(
                    "Preview Overlay",
                    all_overlays_1x1,
                    format_func=lambda x: f"{x.name} {'[VIDEO]' if x.suffix.lower() in ['.mov', '.mp4'] else '[STATIC]'}",
                    key="overlay_1x1"
                )
                
                # Get hero dimensions for slider bounds
                if hero_1x1:
                    hero_dims = comp.get_hero_dimensions(hero_1x1)
                    st.caption(f"Hero size: {hero_dims[0]}x{hero_dims[1]}")

                st.divider()

                # Detect overlay type and load appropriate position
                is_video_1x1 = overlay_preview and overlay_preview.suffix.lower() in ['.mov', '.mp4']
                overlay_type_1x1 = "video" if is_video_1x1 else "static"
                pos = comp.get_position("1x1", overlay_type_1x1)

                # Frame position slider for video previews
                if is_video_1x1:
                    frame_pos_1x1 = st.slider(
                        "Preview Frame Position",
                        min_value=0.0,
                        max_value=1.0,
                        value=0.5,
                        step=0.01,
                        help="Scrub through video to find positioning frame (0% = start, 100% = end)",
                        key=f"frame_pos_1x1_{overlay_type_1x1}"
                    )
                    st.caption(f"Preview at: {int(frame_pos_1x1 * 100)}%")
                else:
                    frame_pos_1x1 = 0.0

                x_1x1 = st.slider(
                    "X Position",
                    min_value=-(hero_dims[0] // 2) if hero_1x1 else -540,
                    max_value=hero_dims[0] if hero_1x1 else 1080,
                    value=int(pos["x"]),
                    key=f"x_1x1_{overlay_type_1x1}"
                )

                y_1x1 = st.slider(
                    "Y Position",
                    min_value=-(hero_dims[1] // 2) if hero_1x1 else -540,
                    max_value=hero_dims[1] if hero_1x1 else 1080,
                    value=int(pos["y"]),
                    key=f"y_1x1_{overlay_type_1x1}"
                )

                scale_1x1 = st.slider(
                    "Scale",
                    min_value=0.1,
                    max_value=2.0,
                    value=float(pos.get("scale", 1.0)),
                    step=0.05,
                    key=f"scale_1x1_{overlay_type_1x1}"
                )

                # Video loop settings
                if overlay_preview and overlay_preview.suffix.lower() in ['.mov', '.mp4']:
                    st.divider()
                    overlay_duration = comp._get_video_duration(overlay_preview)
                    st.caption(f"Overlay duration: {overlay_duration:.2f}s")

                    loop_count_1x1 = st.slider(
                        "Loop Count",
                        min_value=1,
                        max_value=10,
                        value=int(pos.get("loop_count", 1)),
                        key=f"loop_1x1_{overlay_type_1x1}"
                    )

                    final_duration = overlay_duration * loop_count_1x1
                    st.caption(f"Final video: {final_duration:.2f}s")
                else:
                    loop_count_1x1 = 1

                st.divider()

                if st.button("Save 1x1 Position", type="primary", icon=":material/check:"):
                    comp.set_position("1x1", x_1x1, y_1x1, scale_1x1, loop_count_1x1, overlay_type_1x1)
                    st.success(f"Position saved for 1x1 {overlay_type_1x1} overlays!")
            
            with col2:
                # Live preview
                if hero_1x1 and overlay_preview:
                    preview_pos = {"x": x_1x1, "y": y_1x1, "scale": scale_1x1}
                    preview = create_preview(hero_1x1, overlay_preview, preview_pos, frame_pos_1x1)
                    
                    # Resize for display if needed
                    max_display = 600
                    if preview.width > max_display or preview.height > max_display:
                        ratio = min(max_display / preview.width, max_display / preview.height)
                        display_size = (int(preview.width * ratio), int(preview.height * ratio))
                        preview = preview.resize(display_size, Image.Resampling.LANCZOS)
                    
                    st.image(preview, caption="Live Preview", use_container_width=False)
    
    # --- 9x16 Tab ---
    with tab2:
        st.markdown(f'<h3 style="display: flex; align-items: center; gap: 10px; color: #f0f0f0;"><span style="color: #7cb518">{ICONS["smartphone"]}</span> 9x16 Format Positioning</h3>', unsafe_allow_html=True)

        heroes_9x16_flat = flatten_files(inputs['heroes_9x16'])
        overlays_static_9x16_flat = flatten_files(inputs['overlays_static_9x16'])
        overlays_video_9x16_flat = flatten_files(inputs['overlays_video_9x16'])

        if not heroes_9x16_flat:
            st.warning("No 9x16 heroes found. Add images to `inputs/heroes/9x16/`")
        elif not overlays_static_9x16_flat and not overlays_video_9x16_flat:
            st.warning("No 9x16 overlays found. Add files to `inputs/overlays/static/9x16/` or `inputs/overlays/video/9x16/`")
        else:
            col1, col2 = st.columns([1, 2])

            with col1:
                hero_9x16 = st.selectbox(
                    "Preview Hero",
                    heroes_9x16_flat,
                    format_func=lambda x: x.name,
                    key="hero_9x16"
                )

                # Combine static and video overlays for preview
                all_overlays_9x16 = overlays_static_9x16_flat + overlays_video_9x16_flat
                overlay_preview_9x16 = st.selectbox(
                    "Preview Overlay",
                    all_overlays_9x16,
                    format_func=lambda x: f"{x.name} {'[VIDEO]' if x.suffix.lower() in ['.mov', '.mp4'] else '[STATIC]'}",
                    key="overlay_9x16"
                )
                
                if hero_9x16:
                    hero_dims_9x16 = comp.get_hero_dimensions(hero_9x16)
                    st.caption(f"Hero size: {hero_dims_9x16[0]}x{hero_dims_9x16[1]}")

                st.divider()

                # Detect overlay type and load appropriate position
                is_video_9x16 = overlay_preview_9x16 and overlay_preview_9x16.suffix.lower() in ['.mov', '.mp4']
                overlay_type_9x16 = "video" if is_video_9x16 else "static"
                pos_9x16 = comp.get_position("9x16", overlay_type_9x16)

                # Frame position slider for video previews
                if is_video_9x16:
                    frame_pos_9x16 = st.slider(
                        "Preview Frame Position",
                        min_value=0.0,
                        max_value=1.0,
                        value=0.5,
                        step=0.01,
                        help="Scrub through video to find positioning frame (0% = start, 100% = end)",
                        key=f"frame_pos_9x16_{overlay_type_9x16}"
                    )
                    st.caption(f"Preview at: {int(frame_pos_9x16 * 100)}%")
                else:
                    frame_pos_9x16 = 0.0

                x_9x16 = st.slider(
                    "X Position",
                    min_value=-(hero_dims_9x16[0] // 2) if hero_9x16 else -540,
                    max_value=hero_dims_9x16[0] if hero_9x16 else 1080,
                    value=int(pos_9x16["x"]),
                    key=f"x_9x16_{overlay_type_9x16}"
                )

                y_9x16 = st.slider(
                    "Y Position",
                    min_value=-(hero_dims_9x16[1] // 2) if hero_9x16 else -960,
                    max_value=hero_dims_9x16[1] if hero_9x16 else 1920,
                    value=int(pos_9x16["y"]),
                    key=f"y_9x16_{overlay_type_9x16}"
                )

                scale_9x16 = st.slider(
                    "Scale",
                    min_value=0.1,
                    max_value=2.0,
                    value=float(pos_9x16.get("scale", 1.0)),
                    step=0.05,
                    key=f"scale_9x16_{overlay_type_9x16}"
                )

                # Video loop settings
                if overlay_preview_9x16 and overlay_preview_9x16.suffix.lower() in ['.mov', '.mp4']:
                    st.divider()
                    overlay_duration = comp._get_video_duration(overlay_preview_9x16)
                    st.caption(f"Overlay duration: {overlay_duration:.2f}s")

                    loop_count_9x16 = st.slider(
                        "Loop Count",
                        min_value=1,
                        max_value=10,
                        value=int(pos_9x16.get("loop_count", 1)),
                        key=f"loop_9x16_{overlay_type_9x16}"
                    )

                    final_duration = overlay_duration * loop_count_9x16
                    st.caption(f"Final video: {final_duration:.2f}s")
                else:
                    loop_count_9x16 = 1

                st.divider()

                if st.button("Save 9x16 Position", type="primary", icon=":material/check:"):
                    comp.set_position("9x16", x_9x16, y_9x16, scale_9x16, loop_count_9x16, overlay_type_9x16)
                    st.success(f"Position saved for 9x16 {overlay_type_9x16} overlays!")
            
            with col2:
                if hero_9x16 and overlay_preview_9x16:
                    preview_pos = {"x": x_9x16, "y": y_9x16, "scale": scale_9x16}
                    preview = create_preview(hero_9x16, overlay_preview_9x16, preview_pos, frame_pos_9x16)
                    
                    max_display = 500
                    if preview.width > max_display or preview.height > max_display:
                        ratio = min(max_display / preview.width, max_display / preview.height)
                        display_size = (int(preview.width * ratio), int(preview.height * ratio))
                        preview = preview.resize(display_size, Image.Resampling.LANCZOS)
                    
                    st.image(preview, caption="Live Preview", use_container_width=False)
    
    # --- Render Tab ---
    with tab3:
        st.markdown(f'<h3 style="display: flex; align-items: center; gap: 10px; color: #f0f0f0;"><span style="color: #7cb518">{ICONS["play"]}</span> Batch Render</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<p class="section-header">Current Positions</p>', unsafe_allow_html=True)

            st.json({
                "1x1_static": comp.get_position("1x1", "static"),
                "1x1_video": comp.get_position("1x1", "video"),
                "9x16_static": comp.get_position("9x16", "static"),
                "9x16_video": comp.get_position("9x16", "video")
            })
        
        with col2:
            st.markdown('<p class="section-header">Output Summary</p>', unsafe_allow_html=True)

            static_1x1 = len(inputs['heroes_1x1']) * len(inputs['overlays_static_1x1'])
            static_9x16 = len(inputs['heroes_9x16']) * len(inputs['overlays_static_9x16'])
            video_1x1 = len(inputs['heroes_1x1']) * len(inputs['overlays_video_1x1'])
            video_9x16 = len(inputs['heroes_9x16']) * len(inputs['overlays_video_9x16'])

            st.write(f"1x1 outputs: **{static_1x1 + video_1x1}** ({static_1x1} static, {video_1x1} video)")
            st.write(f"9x16 outputs: **{static_9x16 + video_9x16}** ({static_9x16} static, {video_9x16} video)")
            st.write(f"**Total: {static_1x1 + static_9x16 + video_1x1 + video_9x16}**")
        
        st.divider()

        # Render filters
        st.markdown('<p class="section-header">Render Filters</p>', unsafe_allow_html=True)

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            render_1x1 = st.checkbox("1x1 Format", value=True, key="render_1x1_check")
            render_static = st.checkbox("Static overlays (PNG)", value=True, key="render_static_check")

        with col_f2:
            render_9x16 = st.checkbox("9x16 Format", value=True, key="render_9x16_check")
            render_video = st.checkbox("Video overlays (MP4)", value=True, key="render_video_check")

        # Subfolder selection
        hero_subfolders = get_subfolders(inputs['heroes_1x1'])  # Use 1x1 as reference
        overlay_subfolders = get_subfolders(inputs['overlays_static_1x1'])

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            hero_subfolder_filter = st.selectbox("Hero subfolder", hero_subfolders, key="hero_subfolder")
        with col_s2:
            overlay_subfolder_filter = st.selectbox("Overlay subfolder", overlay_subfolders, key="overlay_subfolder")

        # Output subfolder name
        output_subfolder = st.text_input(
            "Output subfolder name",
            value="render",
            help="Subdirectory within outputs/{format}/ for this render batch",
            key="output_subfolder"
        )

        st.divider()
        
        if st.button("RENDER ALL", type="primary", use_container_width=True, icon=":material/play_arrow:"):
            # Filter heroes by subfolder
            heroes_1x1_filtered = filter_by_subfolder(inputs['heroes_1x1'], hero_subfolder_filter) if render_1x1 else []
            heroes_9x16_filtered = filter_by_subfolder(inputs['heroes_9x16'], hero_subfolder_filter) if render_9x16 else []

            # Filter overlays by subfolder and type
            overlays_s_1x1 = filter_by_subfolder(inputs['overlays_static_1x1'], overlay_subfolder_filter) if (render_static and render_1x1) else []
            overlays_s_9x16 = filter_by_subfolder(inputs['overlays_static_9x16'], overlay_subfolder_filter) if (render_static and render_9x16) else []
            overlays_v_1x1 = filter_by_subfolder(inputs['overlays_video_1x1'], overlay_subfolder_filter) if (render_video and render_1x1) else []
            overlays_v_9x16 = filter_by_subfolder(inputs['overlays_video_9x16'], overlay_subfolder_filter) if (render_video and render_9x16) else []

            if not heroes_1x1_filtered and not heroes_9x16_filtered:
                st.error("No hero images match your filters!")
            elif not any([overlays_s_1x1, overlays_s_9x16, overlays_v_1x1, overlays_v_9x16]):
                st.error("No overlays match your filters!")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()

                def update_progress(current, total, message):
                    progress_bar.progress(current / total)
                    status_text.text(message)

                with st.spinner("Rendering..."):
                    results = comp.render_all(
                        heroes_1x1=heroes_1x1_filtered,
                        heroes_9x16=heroes_9x16_filtered,
                        overlays_static_1x1=overlays_s_1x1,
                        overlays_static_9x16=overlays_s_9x16,
                        overlays_video_1x1=overlays_v_1x1,
                        overlays_video_9x16=overlays_v_9x16,
                        output_subfolder=output_subfolder,
                        progress_callback=update_progress
                    )
                
                progress_bar.progress(1.0)
                status_text.text("Complete!")
                
                st.success(f"Rendered {results['success']} files successfully")
                if results['failed'] > 0:
                    st.warning(f"{results['failed']} files failed")
                
                st.write(f"Outputs saved to: `{BASE_PATH / 'outputs'}`")
                
                with st.expander("View output files"):
                    for output in results['outputs']:
                        st.text(output)


if __name__ == "__main__":
    main()
