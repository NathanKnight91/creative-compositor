"""
Text Overlay Tool
Add custom 3-line text overlays with independent font styles
"""

import streamlit as st
from pathlib import Path
from PIL import Image
from ui.styles import ICONS
from ui.preview import create_multiline_text_preview
from utils.file_scanner import flatten_files, scan_font_families


def render(comp, inputs, base_path):
    """
    Render the text overlay tool UI

    Args:
        comp: Compositor instance
        inputs: Dict of scanned input files
        base_path: Base path for the project
    """
    # Scan for available font families
    font_families = scan_font_families(base_path)

    # Sidebar - font status
    with st.sidebar:
        st.markdown(f'<div class="icon" style="font-size: 1.2rem; font-weight: 600; margin-bottom: 16px;">🔤 Fonts</div>', unsafe_allow_html=True)

        if font_families:
            st.write(f"✅ {len(font_families)} font famil{'y' if len(font_families) == 1 else 'ies'}")
            with st.expander("Available fonts"):
                for family, styles in font_families.items():
                    st.caption(f"**{family}**: {', '.join(styles.keys())}")
        else:
            st.warning("⚠️ No fonts found")
            st.caption("Add .ttf or .otf files to `assets/fonts/`")
            st.caption("For best results, add font variants:")
            st.caption("• FontName-Regular.ttf")
            st.caption("• FontName-Bold.ttf")
            st.caption("• FontName-Italic.ttf")
            st.caption("• FontName-BoldItalic.ttf")

        st.markdown('<div style="border-top: 1px solid #2a2a3a; margin: 20px 0;"></div>', unsafe_allow_html=True)

        # Hero file counts
        st.markdown('<p class="section-header">Heroes</p>', unsafe_allow_html=True)
        st.write(f"1x1: {len(flatten_files(inputs['heroes_1x1']))} files")
        st.write(f"9x16: {len(flatten_files(inputs['heroes_9x16']))} files")

    # Main area - tabs
    tab1, tab2 = st.tabs([
        "Design Text",
        "Batch Render"
    ])

    with tab1:
        render_design_tab(comp, inputs, base_path, font_families)

    with tab2:
        render_batch_tab(comp, inputs, base_path, font_families)


def render_design_tab(comp, inputs, base_path, font_families):
    """Render the 3-line text design and preview tab"""
    st.markdown(f'<h3 style="display: flex; align-items: center; gap: 10px; color: #f0f0f0;"><span style="color: #7cb518">✏️</span> 3-Line Text Design</h3>', unsafe_allow_html=True)

    if not font_families:
        st.error("No fonts available. Add .ttf or .otf files to `assets/fonts/` to get started.")
        st.info("💡 Download free fonts from [Google Fonts](https://fonts.google.com/) - get Regular, Bold, Italic, and Bold Italic variants!")
        return

    col1, col2 = st.columns([1, 2])

    with col1:
        # Format selector
        format_type = st.selectbox(
            "Format",
            ["1x1", "9x16"],
            key="text_format"
        )

        # Get heroes for selected format
        heroes_key = f"heroes_{format_type}"
        heroes_flat = flatten_files(inputs[heroes_key])

        if not heroes_flat:
            st.warning(f"No {format_type} heroes found. Add images to `inputs/heroes/{format_type}/`")
            return

        # Hero selector
        hero = st.selectbox(
            "Preview Hero",
            heroes_flat,
            format_func=lambda x: x.name,
            key="text_hero"
        )

        # Get hero dimensions
        if hero:
            hero_dims = comp.get_hero_dimensions(hero)
            st.caption(f"Hero size: {hero_dims[0]}x{hero_dims[1]}")

        st.divider()

        # Font family selector
        family_names = list(font_families.keys())
        selected_family = st.selectbox(
            "Font Family",
            family_names,
            key="font_family"
        )

        font_family = font_families[selected_family]
        available_styles = list(font_family.keys())

        # Shared color
        color = st.color_picker(
            "Text Color",
            value="#FFFFFF",
            key="text_color"
        )

        st.divider()

        # 3 Text Lines
        st.markdown('<p class="section-header">Text Lines</p>', unsafe_allow_html=True)

        lines = []
        for i in range(1, 4):
            with st.expander(f"📝 Line {i}", expanded=(i == 1)):
                text = st.text_input(
                    f"Text",
                    value=f"LINE {i}" if i == 1 else "",
                    key=f"line{i}_text",
                    label_visibility="collapsed"
                )

                col_size, col_style = st.columns(2)
                with col_size:
                    size = st.slider(
                        "Size",
                        min_value=12,
                        max_value=200,
                        value=72 if i == 1 else (48 if i == 2 else 36),
                        key=f"line{i}_size"
                    )

                with col_style:
                    # Only show available styles for this font family
                    style = st.selectbox(
                        "Style",
                        available_styles,
                        index=0 if "Bold" not in available_styles or i != 1 else available_styles.index("Bold"),
                        key=f"line{i}_style"
                    )

                lines.append({
                    "text": text,
                    "size": size,
                    "style": style
                })

        st.divider()

        # Position controls
        st.markdown('<p class="section-header">Position</p>', unsafe_allow_html=True)

        x_pos = st.slider(
            "X Position",
            min_value=0,
            max_value=hero_dims[0] if hero else 1080,
            value=hero_dims[0] // 2 if hero else 540,
            key="text_x"
        )

        y_pos = st.slider(
            "Y Position",
            min_value=0,
            max_value=hero_dims[1] if hero else 1080,
            value=hero_dims[1] // 2 if hero else 540,
            key="text_y"
        )

        # Line spacing
        line_spacing = st.slider(
            "Line Spacing",
            min_value=0,
            max_value=50,
            value=10,
            help="Vertical pixels between lines",
            key="line_spacing"
        )

        # Alignment
        st.markdown('<p class="section-header">Alignment</p>', unsafe_allow_html=True)

        alignment_options = {
            "Left": "lm",
            "Center": "mm",
            "Right": "rm"
        }

        alignment = st.radio(
            "Text Alignment",
            options=list(alignment_options.keys()),
            index=1,  # Default to Center
            horizontal=True,
            key="text_alignment"
        )

        alignment_anchor = alignment_options[alignment]

        st.divider()

        # Save button
        if st.button("Save Text Config", type="primary", icon=":material/check:"):
            # Save configuration (you can extend this later)
            st.success(f"Text config saved for {format_type} format!")
            st.caption("Config saving coming soon - for now, positions reset on refresh")

    with col2:
        # Live preview
        if hero:
            preview_pos = {
                "x": x_pos,
                "y": y_pos,
                "alignment": alignment_anchor
            }

            # Only render lines that have text
            active_lines = [line for line in lines if line["text"]]

            if active_lines:
                preview = create_multiline_text_preview(
                    hero,
                    active_lines,
                    font_family,
                    color,
                    preview_pos,
                    line_spacing
                )

                # Resize for display if needed
                max_display = 600
                if preview.width > max_display or preview.height > max_display:
                    ratio = min(max_display / preview.width, max_display / preview.height)
                    display_size = (int(preview.width * ratio), int(preview.height * ratio))
                    preview = preview.resize(display_size, Image.Resampling.LANCZOS)

                st.image(preview, caption="Live Preview", use_container_width=False)
            else:
                st.info("👆 Enter text in Line 1, 2, or 3 to see preview")


def render_batch_tab(comp, inputs, base_path, font_families):
    """Render the batch rendering tab"""
    st.markdown(f'<h3 style="display: flex; align-items: center; gap: 10px; color: #f0f0f0;"><span style="color: #7cb518">{ICONS["play"]}</span> Batch 3-Line Text Render</h3>', unsafe_allow_html=True)

    if not font_families:
        st.error("No fonts available. Add .ttf or .otf files to `assets/fonts/` first.")
        return

    st.info("ℹ️ Batch rendering with saved configs coming soon! For now, use the Design tab to create individual outputs.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<p class="section-header">Available Heroes</p>', unsafe_allow_html=True)

        heroes_1x1_count = len(flatten_files(inputs['heroes_1x1']))
        heroes_9x16_count = len(flatten_files(inputs['heroes_9x16']))

        st.write(f"1x1 heroes: **{heroes_1x1_count}** files")
        st.write(f"9x16 heroes: **{heroes_9x16_count}** files")
        st.write(f"**Total: {heroes_1x1_count + heroes_9x16_count}**")

    with col2:
        st.markdown('<p class="section-header">Font Families</p>', unsafe_allow_html=True)

        for family, styles in font_families.items():
            st.caption(f"**{family}**: {', '.join(styles.keys())}")

    st.divider()

    st.markdown("### 🚧 Coming Soon")
    st.write("Batch rendering features:")
    st.write("• Save 3-line configurations per format")
    st.write("• Apply saved config to multiple heroes")
    st.write("• CSV import for dynamic text replacement")
    st.write("• Per-hero text customization")
