"""Reusable milestone-row renderer with B2B SaaS design system."""

import streamlit as st

STATUS_CONFIG = {
    "Done": {
        "bg": "#ECFDF5",
        "border": "#A7F3D0",
        "text": "#047857",
        "dot": "#10B981"
    },
    "Open": {
        "bg": "#FFFBEB",
        "border": "#FDE68A",
        "text": "#B45309",
        "dot": "#F59E0B"
    },
    "Blocked": {
        "bg": "#FEF2F2",
        "border": "#FECACA",
        "text": "#B91C1C",
        "dot": "#EF4444"
    },
}


def render_milestone(milestone, show_internal: bool) -> None:
    """Render a milestone card unless it is hidden in customer view."""
    if not show_internal and milestone.internal_only:
        return

    cfg = STATUS_CONFIG.get(milestone.status, STATUS_CONFIG["Open"])
    blocked_icon = "🚧 " if milestone.status == "Blocked" else ""
    internal_badge = '<span style="background:#F1F5F9; color:#64748B; padding:2px 8px; border-radius:6px; font-size:11px; font-weight:600; margin-left:6px;">Internal Only</span>' if milestone.internal_only and show_internal else ""

    st.markdown(f"""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:14px 18px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 1px 2px rgba(0,0,0,0.03);">
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="font-weight:700; font-size:0.95rem; color:#0F172A;">
                {blocked_icon}{milestone.title} {internal_badge}
            </div>
        </div>
        <div style="display:flex; align-items:center; gap:16px;">
            <span style="font-size:0.8125rem; color:#64748B; font-weight:500;">Due {milestone.due_date}</span>
            <span style="background:{cfg['bg']}; border:1px solid {cfg['border']}; color:{cfg['text']}; padding:4px 12px; border-radius:999px; font-size:12px; font-weight:700; display:inline-flex; align-items:center; gap:6px;">
                <span style="width:6px; height:6px; border-radius:50%; background:{cfg['dot']};"></span>
                {milestone.status}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
