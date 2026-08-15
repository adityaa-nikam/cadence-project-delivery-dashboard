"""Custom design system & CSS injection for Cadence Project Delivery Dashboard."""

import streamlit as st


def load_custom_css() -> None:
    """Inject modern B2B SaaS CSS into Streamlit page."""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    /* Global Typography & Font Family */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }

    /* Clean Streamlit Default Header */
    header[data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(12px) !important;
        border-bottom: 1px solid rgba(226, 232, 240, 0.8) !important;
    }

    /* Hide Default Streamlit Sidebar Navigation Links (app, detail, overview) */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* Page Background */
    .stApp {
        background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%) !important;
    }

    /* Container Constraints */
    .main .block-container {
        padding-top: 1.75rem !important;
        padding-bottom: 4rem !important;
        max-width: 1280px !important;
    }

    /* Sidebar Styling (Modern Dark Slate Aesthetic) */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
        border-right: 1px solid #334155 !important;
    }

    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] label {
        color: #F8FAFC !important;
    }

    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(99, 102, 241, 0.25) !important;
        border-color: #6366F1 !important;
        color: #FFFFFF !important;
        transform: translateY(-1px) !important;
    }

    /* Sidebar Metric Cards Specific High Contrast Dark Styling */
    section[data-testid="stSidebar"] div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 10px !important;
        padding: 0.75rem 0.875rem !important;
        box-shadow: none !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stMetricLabel"],
    section[data-testid="stSidebar"] div[data-testid="stMetricLabel"] label,
    section[data-testid="stSidebar"] div[data-testid="stMetricLabel"] div,
    section[data-testid="stSidebar"] div[data-testid="stMetricLabel"] span,
    section[data-testid="stSidebar"] div[data-testid="stMetricLabel"] p {
        color: #94A3B8 !important;
        font-weight: 700 !important;
        font-size: 0.725rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stMetricValue"],
    section[data-testid="stSidebar"] div[data-testid="stMetricValue"] div,
    section[data-testid="stSidebar"] div[data-testid="stMetricValue"] span {
        color: #FFFFFF !important;
        font-size: 1.5rem !important;
        font-weight: 800 !important;
    }

    /* Main Content Metric Cards Styling */
    .main div[data-testid="stMetric"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 1rem 1.25rem !important;
        box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    .main div[data-testid="stMetric"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 12px -3px rgba(0, 0, 0, 0.06) !important;
    }

    .main div[data-testid="stMetricLabel"] {
        font-size: 0.775rem !important;
        font-weight: 700 !important;
        color: #64748B !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    .main div[data-testid="stMetricValue"] {
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        color: #0F172A !important;
    }

    /* Primary Action Buttons */
    .stButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.9375rem !important;
        padding: 0.6rem 1.25rem !important;
        box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.25), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stButton > button[kind="primary"]:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background: linear-gradient(135deg, #4338CA 0%, #4F46E5 100%) !important;
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.35) !important;
        transform: translateY(-1px) !important;
    }

    /* Secondary Buttons */
    .stButton > button[kind="secondary"] {
        background: #FFFFFF !important;
        color: #334155 !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background: #F8FAFC !important;
        border-color: #94A3B8 !important;
        color: #0F172A !important;
        transform: translateY(-1px) !important;
    }

    /* Card Containers with Borders */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03), 0 2px 4px -1px rgba(0, 0, 0, 0.02) !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 10px 18px -4px rgba(0, 0, 0, 0.06) !important;
        border-color: #CBD5E1 !important;
    }

    /* Form Fields (Inputs, Textarea, Selectbox) */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        border-radius: 8px !important;
        border: 1px solid #CBD5E1 !important;
        padding: 0.6rem 0.875rem !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
        outline: none !important;
    }

    /* Custom Scrollbars */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #F1F5F9;
    }
    ::-webkit-scrollbar-thumb {
        background: #CBD5E1;
        border-radius: 999px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #94A3B8;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: transparent !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        color: #64748B !important;
        border: 1px solid transparent !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #4F46E5 !important;
        border-color: #E2E8F0 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
