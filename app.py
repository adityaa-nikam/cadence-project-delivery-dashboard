"""Cadence Streamlit application entry point."""

import os

import streamlit as st
from dotenv import load_dotenv

# Load .env FIRST before any other imports that might read env vars
load_dotenv()

from mock_data import MILESTONES, PROJECTS, UPDATES
from pages.detail import render_detail
from pages.overview import render_overview
from utils.state import init_state
from utils.theme import load_custom_css

st.set_page_config(page_title="Cadence - Project Delivery Dashboard", layout="wide", page_icon="⚡")
load_custom_css()

# API key check (supports local env + Streamlit Cloud secrets)
def _get_api_key():
    key = os.environ.get("GROQ_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")
    if not key:
        try:
            key = st.secrets.get("GROQ_API_KEY", "") or st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            pass
    return key

st.session_state["has_gemini_api_key"] = bool(_get_api_key())

# Initialize mutable data copies
init_state(PROJECTS, MILESTONES, UPDATES)

with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;padding:4px 0;">
        <div style="background:linear-gradient(135deg,#4F46E5,#6366F1);width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;color:white;font-weight:800;font-size:18px;">
            ⚡
        </div>
        <div>
            <div style="font-weight:700;font-size:16px;letter-spacing:-0.3px;color:#F8FAFC;">Cadence</div>
            <div style="font-size:11px;color:#94A3B8;font-weight:500;">Delivery Workspace</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🏠 All Projects", use_container_width=True, type="secondary"):
        st.session_state["selected_project_id"] = None
        st.rerun()

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    
    # API Status Card
    if st.session_state["has_gemini_api_key"]:
        st.markdown("""
        <div style="background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.3);padding:8px 12px;border-radius:8px;font-size:12px;color:#34D399;font-weight:600;display:flex;align-items:center;gap:6px;">
            ● Groq AI Active
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(245,158,11,0.12);border:1px solid rgba(245,158,11,0.3);padding:8px 12px;border-radius:8px;font-size:12px;color:#FBBF24;font-weight:600;display:flex;align-items:center;gap:6px;">
            ⚠️ AI Offline (Key Missing)
        </div>
        """, unsafe_allow_html=True)

    # Portfolio Quick Stats
    st.sidebar.markdown("<hr style='border-color:#334155;margin:16px 0;'>", unsafe_allow_html=True)
    st.sidebar.markdown("<div style='font-size:12px;font-weight:700;letter-spacing:0.05em;color:#94A3B8;text-transform:uppercase;margin-bottom:8px;'>Portfolio Overview</div>", unsafe_allow_html=True)
    all_ms = st.session_state.get("milestones", [])
    all_upd = st.session_state.get("updates", [])
    
    s_col1, s_col2 = st.sidebar.columns(2)
    s_col1.metric("Done", sum(1 for m in all_ms if m.status == "Done"))
    s_col2.metric("Blocked", sum(1 for m in all_ms if m.status == "Blocked"))
    s_col1.metric("Open", sum(1 for m in all_ms if m.status == "Open"))
    s_col2.metric("AI Logs", sum(1 for u in all_upd if u.is_ai_processed))

if st.session_state["selected_project_id"] is None:
    render_overview()
else:
    render_detail()