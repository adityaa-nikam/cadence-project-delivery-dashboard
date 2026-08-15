"""Reusable, customer-safe project updates activity feed."""

from datetime import datetime
import streamlit as st


def customer_safe_updates(updates: list, visible_milestone_titles: set[str]) -> list:
    """Return only updates tied to milestones that can be shared externally."""
    return [update for update in updates if update.affected_milestone in visible_milestone_titles]


def time_ago(timestamp: str) -> str:
    """Convert ISO timestamp to human-readable relative time."""
    try:
        dt = datetime.fromisoformat(timestamp)
        delta = datetime.now() - dt
        if delta.days > 0:
            return f"{delta.days}d ago"
        hours = delta.seconds // 3600
        if hours > 0:
            return f"{hours}h ago"
        mins = delta.seconds // 60
        return f"{mins}m ago"
    except Exception:
        return timestamp


def render_update_entry(update, show_internal: bool) -> None:
    """Render a single update entry with modern timeline styling."""
    summary = update.structured_summary or f"Activity recorded for {update.affected_milestone}."
    entry_badge = "✨ AI Processed" if update.is_ai_processed else "📝 Manual Entry"
    badge_bg = "#EEF2FF" if update.is_ai_processed else "#F1F5F9"
    badge_fg = "#3730A3" if update.is_ai_processed else "#475569"

    with st.container(border=True):
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px;">
            <div style="font-size:0.95rem; font-weight:700; color:#0F172A; line-height:1.4;">{summary}</div>
            <span style="background:{badge_bg}; color:{badge_fg}; padding:3px 10px; border-radius:999px; font-size:11px; font-weight:700; flex-shrink:0;">
                {entry_badge}
            </span>
        </div>
        <div style="font-size:0.8125rem; color:#64748B; margin-bottom:4px;">
            ⏱️ {time_ago(update.timestamp)} • Milestone: <strong style="color:#334155;">{update.affected_milestone}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        if update.status_change:
            st.markdown(f"""
            <div style="background:#F0FDF4; border:1px solid #BBF7D0; color:#166534; padding:4px 10px; border-radius:6px; font-size:12px; font-weight:600; margin-top:6px; display:inline-block;">
                Status Updated: {update.status_change}
            </div>
            """, unsafe_allow_html=True)
            
        if show_internal:
            with st.expander("📧 View Raw Log Source"):
                st.markdown(f"<div style='font-size:0.875rem; color:#475569;'>{update.raw_text}</div>", unsafe_allow_html=True)


def render_update_feed(
    updates: list,
    show_internal: bool,
    visible_milestone_titles: set[str] | None = None,
) -> None:
    """Backward-compatible feed renderer used by pages that need a complete feed."""
    visible_updates = updates if show_internal else customer_safe_updates(updates, visible_milestone_titles or set())
    if not visible_updates:
        st.info("No updates yet")
        return
    for update in visible_updates:
        render_update_entry(update, show_internal)