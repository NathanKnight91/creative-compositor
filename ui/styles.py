"""
UI Styles - Channel 4 inspired dark theme
Custom CSS injection and icon definitions
"""

import streamlit as st


def inject_css():
    """Inject custom CSS for Channel 4 inspired theme"""
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
