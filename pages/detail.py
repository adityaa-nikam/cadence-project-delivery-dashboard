"""Project-detail page for delivery, issue, and update management with B2B SaaS design aesthetics."""

from datetime import datetime
import streamlit as st

from ai_helper import draft_customer_email, parse_update
from components.health_score import render_health_score
from components.issue_badge import render_issue
from components.milestone_card import render_milestone
from components.update_feed import customer_safe_updates, render_update_entry
from mock_data import Update
from utils.state import (
    get_issues,
    get_milestones,
    get_or_compute_health,
    get_project,
    get_updates,
    prepend_update,
    update_milestone_status,
)


STATUS_CONFIG = {
    "On Track": {
        "bg": "#ECFDF5",
        "border": "#A7F3D0",
        "text": "#047857",
        "dot": "#10B981"
    },
    "At Risk": {
        "bg": "#FFFBEB",
        "border": "#FDE68A",
        "text": "#B45309",
        "dot": "#F59E0B"
    },
    "Delayed": {
        "bg": "#FEF2F2",
        "border": "#FECACA",
        "text": "#B91C1C",
        "dot": "#EF4444"
    },
}


def _render_back_button():
    """Render the back navigation button at top level."""
    col1, _ = st.columns([2, 8])
    with col1:
        if st.button("← Back to All Projects", key="back_all_projects", type="secondary"):
            st.session_state["selected_project_id"] = None
            st.rerun()


def render_detail() -> None:
    """Render the selected project's internal or customer-safe detail view."""
    _render_back_button()

    project_id = st.session_state.get("selected_project_id")
    project = get_project(project_id)
    if project is None:
        st.session_state["selected_project_id"] = None
        st.rerun()

    cfg = STATUS_CONFIG.get(project.overall_status, STATUS_CONFIG["On Track"])

    # Project Title Banner Card
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 1.75rem 2rem; margin-top: 0.75rem; margin-bottom: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03);">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
            <div>
                <div style="font-size: 0.8125rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Project Delivery View</div>
                <h1 style="font-size: 1.85rem; font-weight: 800; color: #0F172A; margin: 0; letter-spacing: -0.025em;">{project.name}</h1>
                <div style="font-size: 0.875rem; color: #64748B; margin-top: 6px; display:flex; align-items:center; gap:8px;">
                    <span>👤 Delivery Lead: <strong style="color:#334155;">{', '.join(project.owners)}</strong></span>
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:12px;">
                <span style="background:{cfg['bg']}; border:1px solid {cfg['border']}; color:{cfg['text']}; padding:6px 16px; border-radius:999px; font-size:13px; font-weight:700; display:inline-flex; align-items:center; gap:8px;">
                    <span style="width:8px; height:8px; border-radius:50%; background:{cfg['dot']};"></span>
                    {project.overall_status}
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Health Score & Completion Progress
    milestones = get_milestones(project_id)
    issues = get_issues(project_id)
    updates = get_updates(project_id)
    health = get_or_compute_health(project_id, project, milestones, issues, updates)
    
    render_health_score(health)
    
    done_count = sum(1 for m in milestones if m.status == "Done")
    total_count = len(milestones)
    pct = done_count / total_count if total_count > 0 else 0

    col_prog, col_ref = st.columns([4, 1])
    with col_prog:
        st.progress(pct, text=f"Milestone Execution: {done_count}/{total_count} Completed ({pct*100:.0f}%)")
    with col_ref:
        if st.button("🔄 Refresh Health", key="refresh_health", type="secondary", use_container_width=True):
            cache_key = f"health_{project_id}"
            sig_key = f"health_sig_{project_id}"
            if cache_key in st.session_state:
                del st.session_state[cache_key]
            if sig_key in st.session_state:
                del st.session_state[sig_key]
            st.rerun()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # View Mode Segmented Control Banner
    st.markdown("""
    <div style="background: #EEF2FF; border: 1px solid #C7D2FE; padding: 12px 18px; border-radius: 12px; margin-bottom: 1rem; display: flex; align-items: center; justify-content: space-between;">
        <span style="font-size: 0.875rem; font-weight: 700; color: #3730A3;">👁️ Dashboard View Perspective</span>
        <span style="font-size: 0.775rem; color: #4338CA;">Toggle between internal engineering notes and external client portal</span>
    </div>
    """, unsafe_allow_html=True)
    
    current_mode = st.session_state.get("view_mode", "internal")
    view_choice = st.radio(
        "",
        ["🔒 Internal View", "👤 Customer View"],
        index=0 if current_mode == "internal" else 1,
        horizontal=True,
        key="detail_view_mode",
        label_visibility="collapsed",
    )
    show_internal = view_choice == "🔒 Internal View"
    st.session_state["view_mode"] = "internal" if show_internal else "customer"

    if show_internal:
        with st.expander("🔒 Internal Team Notes & Context", expanded=True):
            st.markdown(f"<div style='font-size:0.925rem; color:#334155; line-height:1.6;'>{project.internal_notes}</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%); color: white; padding: 18px 24px; border-radius: 14px; margin-bottom: 1.5rem; box-shadow: 0 10px 20px -5px rgba(79,70,229,0.3);">
            <div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.85;">Client Portal</div>
            <h3 style="margin: 4px 0 0; color: white; font-weight: 800; font-size: 1.25rem;">Customer Delivery Status</h3>
            <p style="margin: 4px 0 0; opacity: 0.9; font-size: 0.875rem;">Verified project status shared by your customer success & delivery lead.</p>
        </div>
        """, unsafe_allow_html=True)

    visible_milestone_titles = {milestone.title for milestone in milestones if not milestone.internal_only}

    # Milestones Section
    st.markdown("<h3 style='font-size:1.25rem; font-weight:700; color:#0F172A; margin-top:1.5rem; margin-bottom:0.75rem;'>📋 Milestones & Deliverables</h3>", unsafe_allow_html=True)
    if not show_internal:
        st.caption("Showing customer-visible milestones only")
    for milestone in milestones:
        render_milestone(milestone, show_internal)

    # 📧 Customer Communication - AI Draft Email Component (Internal View Only)
    if show_internal:
        st.markdown("<hr style='border-color:#E2E8F0; margin: 2rem 0;'>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 1.75rem 2rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03);">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
                <div>
                    <h3 style="font-size: 1.15rem; font-weight: 700; color: #0F172A; margin: 0;">📧 AI Customer Status Draft</h3>
                    <p style="color: #64748B; font-size: 0.875rem; margin-top: 4px; margin-bottom: 0;">Generate an executive-ready customer update email using live milestone metrics.</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("<div style='font-size:0.875rem; color:#475569; margin-top:8px;'>AI evaluates recent milestones, open blockages, and progress to calibrate tone (Positive, Cautious, or Urgent).</div>", unsafe_allow_html=True)
        with col2:
            generate_btn = st.button(
                "✨ Draft Customer Email", 
                key=f"draft_email_{project_id}",
                type="primary",
                use_container_width=True
            )

        email_cache_key = f"email_draft_{project_id}"

        if generate_btn:
            with st.spinner("✍️ Drafting email with AI..."):
                result = draft_customer_email(project, milestones, issues, updates)
                st.session_state[email_cache_key] = result

        if email_cache_key in st.session_state:
            draft = st.session_state[email_cache_key]
            
            if draft.get("error") and not draft.get("body"):
                st.error(f"Could not generate email: {draft['error']}")
            else:
                if draft.get("error"):
                    st.warning(draft["error"])
                
                tone = draft.get("tone", "cautious")
                tone_color = {"positive": ("#ECFDF5", "#047857"), "cautious": ("#FFFBEB", "#B45309"), "urgent": ("#FEF2F2", "#B91C1C")}
                t_bg, t_fg = tone_color.get(tone, ("#F3F4F6", "#374151"))
                
                st.markdown(f"""
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:14px; padding:1.5rem; margin-top:1rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                        <span style="font-size:0.8125rem; font-weight:700; color:#64748B; text-transform:uppercase;">Email Preview</span>
                        <span style="background:{t_bg}; color:{t_fg}; padding:4px 12px; border-radius:999px; font-size:12px; font-weight:700;">
                            ● {tone.capitalize()} Tone Calibrated
                        </span>
                    </div>
                    <div style="font-size:0.95rem; font-weight:700; color:#0F172A; margin-bottom:12px;">Subject: {draft['subject']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                edited_body = st.text_area(
                    "Email Body (editable):",
                    value=draft["body"].replace("\\n", "\n"),
                    height=240,
                    key=f"email_body_edit_{project_id}"
                )
                
                act_col1, act_col2 = st.columns([1, 4])
                with act_col1:
                    if st.button("🔄 Regenerate", key=f"regen_email_{project_id}", type="secondary"):
                        if email_cache_key in st.session_state:
                            del st.session_state[email_cache_key]
                        st.rerun()
                with act_col2:
                    st.info("💡 Copy the email draft text above directly into your email client.")

    # Issues Section
    st.markdown("<hr style='border-color:#E2E8F0; margin: 2rem 0;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:1.25rem; font-weight:700; color:#0F172A; margin-bottom:0.75rem;'>🐛 Reported Issues & Support Items</h3>", unsafe_allow_html=True)
    
    visible_issues = [issue for issue in issues if show_internal or not issue.internal_only]
    if not visible_issues:
        st.success("✅ No open issues reported for this project.")
    else:
        for issue in visible_issues:
            render_issue(issue, show_internal)

    # Updates & Activity Section
    st.markdown("<hr style='border-color:#E2E8F0; margin: 2rem 0;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:1.25rem; font-weight:700; color:#0F172A; margin-bottom:0.75rem;'>📨 Project Activity & AI Update Feed</h3>", unsafe_allow_html=True)

    if show_internal:
        with st.form(f"update_form_{project.id}", clear_on_submit=True):
            st.markdown("<div style='font-weight:600; font-size:0.9rem; color:#334155; margin-bottom:6px;'>Log Raw Update (Email, Slack note, or call summary):</div>", unsafe_allow_html=True)
            raw_text = st.text_area(
                "Raw update content",
                height=110,
                placeholder="e.g., Just spoke with engineering, database migration completed ahead of schedule. Starting API testing.",
                key=f"update_input_{project.id}",
                label_visibility="collapsed"
            )
            submit = st.form_submit_button("✨ Process Update with AI", type="primary")
            if submit and raw_text.strip():
                milestones_list = st.session_state.get("milestones", [])
                result = parse_update(raw_text, milestones_list)

                if result["error"]:
                    st.warning(result["error"])
                else:
                    new_update = Update(
                        id=f"upd_ai_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                        project_id=project.id,
                        timestamp=datetime.now().replace(microsecond=0).isoformat(),
                        raw_text=raw_text.strip(),
                        structured_summary=result["summary"],
                        affected_milestone=result["affected_milestone"],
                        status_change="",
                        is_ai_processed=True,
                    )

                    if result["new_status"] is not None:
                        for milestone in milestones:
                            if milestone.title == result["affected_milestone"]:
                                old_status = milestone.status
                                update_milestone_status(milestone.id, result["new_status"])
                                status_change = f"{old_status} → {result['new_status']}"
                                new_update.status_change = status_change
                                st.success(f"✅ Milestone '{result['affected_milestone']}' status updated to {result['new_status']}")

                    prepend_update(new_update)
                    st.rerun()

    visible_updates = updates if show_internal else customer_safe_updates(updates, visible_milestone_titles)
    
    if not visible_updates:
        st.info("No activity updates logged yet.")
    else:
        for update in visible_updates:
            render_update_entry(update, show_internal)