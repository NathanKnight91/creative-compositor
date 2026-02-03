"""
Creative Compositor - Streamlit UI
Modular architecture with multiple creative tools
"""

import streamlit as st
from pathlib import Path
from compositor import Compositor
from ui.styles import inject_css, ICONS
from utils.file_scanner import scan_inputs
from tools import overlay_tool, text_tool


# Page config
st.set_page_config(
    page_title="Creative Compositor",
    page_icon=None,
    layout="wide"
)

# Inject custom CSS
inject_css()

# Initialize
BASE_PATH = Path(__file__).parent
comp = Compositor(BASE_PATH)


def main():
    st.markdown(f'<h1><span style="color: #7cb518">{ICONS["layers"]}</span> Creative Compositor</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #8a8a9a; margin-top: -10px;">Multiple creative tools for compositing and text overlays</p>', unsafe_allow_html=True)

    # Scan for files
    inputs = scan_inputs(BASE_PATH)

    # Tool selector in sidebar
    st.sidebar.markdown('<div style="border-bottom: 2px solid #7cb518; margin-bottom: 20px; padding-bottom: 10px;"><h3 style="margin: 0;">🛠️ Tools</h3></div>', unsafe_allow_html=True)

    tool = st.sidebar.radio(
        "Select Tool",
        ["Overlay Compositor", "Text Overlay"],
        label_visibility="collapsed"
    )

    st.sidebar.markdown('<div style="border-top: 1px solid #2a2a3a; margin: 20px 0;"></div>', unsafe_allow_html=True)

    # Route to selected tool
    if tool == "Overlay Compositor":
        overlay_tool.render(comp, inputs, BASE_PATH)
    elif tool == "Text Overlay":
        text_tool.render(comp, inputs, BASE_PATH)


if __name__ == "__main__":
    main()
