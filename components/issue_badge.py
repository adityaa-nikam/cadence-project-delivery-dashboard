"""Reusable issue-row renderer with B2B SaaS design system."""

import streamlit as st

CATEGORY_CONFIG = {
    "Bug": ("#FEF2F2", "#FECACA", "#991B1B"),
    "Feature Request": ("#EFF6FF", "#BFDBFE", "#1E40AF"),
    "Question": ("#F5F3FF", "#DDD6FE", "#5B21B6"),
    "Support": ("#FFFBEB", "#FDE68A", "#92400E"),
    "Implementation": ("#F8FAFC", "#E2E8F0", "#334155"),
}


def render_issue(issue, show_internal: bool) -> None:
    """Render a compact issue row unless hidden in customer view."""
    if not show_internal and issue.internal_only:
        return

    bg, border, text_color = CATEGORY_CONFIG.get(issue.category, ("#F8FAFC", "#E2E8F0", "#334155"))
    
    st.markdown(f"""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:12px 16px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
        <div style="font-size:0.9rem; font-weight:600; color:#1E293B;">
            {issue.title}
        </div>
        <div>
            <span style="background:{bg}; border:1px solid {border}; color:{text_color}; padding:3px 10px; border-radius:999px; font-size:11px; font-weight:700;">
                {issue.category}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
