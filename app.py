"""
Creative Compositor - Streamlit UI
Modular architecture with multiple creative tools
"""

import streamlit as st
from pathlib import Path
from compositor import Compositor
from ui.styles import inject_css, ICONS
from utils.file_scanner import scan_inputs
from tools import overlay_tool


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
    st.markdown('<p style="color: #8a8a9a; margin-top: -10px;">Position overlays on hero images and batch render all combinations</p>', unsafe_allow_html=True)

    # Scan for files
    inputs = scan_inputs(BASE_PATH)

    # For now, we only have one tool (overlay compositor)
    # In the future, we'll add a tool selector here:
    # tool = st.sidebar.radio("Select Tool", ["Overlay Compositor", "Text Overlay", ...])

    # Render the overlay compositor tool
    overlay_tool.render(comp, inputs, BASE_PATH)


if __name__ == "__main__":
    main()
