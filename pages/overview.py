"""Filterable project-overview page for B2B SaaS Delivery Dashboard."""

from datetime import date, datetime
import streamlit as st

from mock_data import PROJECTS, ISSUES
from ai_helper import query_projects


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


def is_project_stale(project_id, updates, days_threshold=7):
    """Check if a project has no updates within the threshold days."""
    project_updates = [u for u in updates if u.project_id == project_id]
    if not project_updates:
        return True
    latest = max(project_updates, key=lambda u: u.timestamp)
    try:
        latest_dt = datetime.fromisoformat(latest.timestamp)
        return (datetime.now() - latest_dt).days > days_threshold
    except Exception:
        return False


def render_overview() -> None:
    """Render the filterable project grid and analytics dashboard."""
    
    # ---- Portfolio Header Banner ----
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); padding: 1.75rem 2rem; border-radius: 16px; border: 1px solid #334155; margin-bottom: 2rem; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
            <div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span style="background: rgba(99,102,241,0.2); border: 1px solid rgba(99,102,241,0.4); color: #818CF8; font-size: 11px; font-weight: 700; padding: 2px 10px; border-radius: 999px; text-transform: uppercase; letter-spacing: 0.05em;">Enterprise Workspace</span>
                    <span style="color: #64748B; font-size: 13px;">• Live Delivery Status</span>
                </div>
                <h1 style="font-size: 1.85rem; font-weight: 800; color: #FFFFFF; margin: 0; letter-spacing: -0.025em;">Project Delivery Dashboard</h1>
                <p style="color: #94A3B8; font-size: 0.925rem; margin-top: 4px; margin-bottom: 0;">Real-time progress, health scores, and AI status generation across active client projects.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- Metrics Bar ----
    all_milestones = st.session_state.get("milestones", [])
    all_updates = st.session_state.get("updates", [])
    projects_list = st.session_state.get("projects", PROJECTS)

    total = len(projects_list)
    on_track = sum(1 for p in projects_list if p.overall_status == "On Track")
    at_risk = sum(1 for p in projects_list if p.overall_status == "At Risk")
    total_blocked = sum(1 for m in all_milestones if m.status == "Blocked")
    ai_updates = sum(1 for u in all_updates if u.is_ai_processed)

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Projects", total)
    m2.metric("On Track", on_track)
    m3.metric("At Risk", at_risk, delta=f"-{at_risk}" if at_risk > 0 else None, delta_color="inverse")
    m4.metric("Blocked Tasks", total_blocked, delta=f"-{total_blocked}" if total_blocked > 0 else None, delta_color="inverse")
    m5.metric("AI Updates Logged", ai_updates)

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

    # ---- Filter Controls ----
    filter_col1, filter_col2 = st.columns([3, 2])
    with filter_col1:
        st.markdown("<h3 style='font-size: 1.25rem; font-weight: 700; color: #0F172A; margin: 0;'>Active Delivery Projects</h3>", unsafe_allow_html=True)
    with filter_col2:
        selected_status = st.selectbox(
            "Filter by status",
            ["All Projects", "On Track", "At Risk", "Delayed"],
            label_visibility="collapsed",
        )

    projects = st.session_state.get("projects", PROJECTS)
    updates = st.session_state.get("updates", [])
    
    filtered_projects = [
        p for p in projects
        if selected_status == "All Projects" or p.overall_status == selected_status
    ]

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # ---- Project Cards Grid ----
    left_column, right_column = st.columns(2)
    
    for index, project in enumerate(filtered_projects):
        column = left_column if index % 2 == 0 else right_column
        cfg = STATUS_CONFIG.get(project.overall_status, STATUS_CONFIG["On Track"])
        
        # Calculate milestone completion percentage for project card
        p_milestones = [m for m in all_milestones if m.project_id == project.id]
        p_done = sum(1 for m in p_milestones if m.status == "Done")
        p_total = len(p_milestones)
        pct = (p_done / p_total) * 100 if p_total > 0 else 0
        
        stale_flag = is_project_stale(project.id, updates)
        
        with column:
            with st.container(border=True):
                stale_badge = f'<span style="background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:6px;font-size:11px;font-weight:600;">⏰ Stale (No Update &gt;7d)</span>' if stale_flag else ''
                card_header_html = (
                    f'<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:12px;">'
                    f'<div>'
                    f'<div style="font-size:1.15rem;font-weight:700;color:#0F172A;line-height:1.3;">{project.name}</div>'
                    f'<div style="font-size:0.8125rem;color:#64748B;margin-top:4px;">👤 Owners: <strong style="color:#334155;">{", ".join(project.owners)}</strong></div>'
                    f'</div>'
                    f'<div style="display:flex;flex-direction:column;align-items:flex-end;gap:4px;">'
                    f'<span style="background:{cfg["bg"]};border:1px solid {cfg["border"]};color:{cfg["text"]};padding:4px 12px;border-radius:999px;font-size:12px;font-weight:700;display:inline-flex;align-items:center;gap:6px;">'
                    f'<span style="width:7px;height:7px;border-radius:50%;background:{cfg["dot"]};display:inline-block;"></span>'
                    f'{project.overall_status}'
                    f'</span>'
                    f'{stale_badge}'
                    f'</div>'
                    f'</div>'
                )
                st.markdown(card_header_html, unsafe_allow_html=True)
                
                # Progress Bar & Milestone metrics
                st.progress(pct / 100, text=f"Completion: {p_done}/{p_total} Milestones ({pct:.0f}%)")
                
                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                
                # Action Button
                if st.button("View Delivery Details →", key=f"btn_{project.id}", type="primary", use_container_width=True):
                    st.session_state["selected_project_id"] = project.id
                    st.rerun()

    # ---- Natural Language Query Section ----
    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 1.75rem 2rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03);">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom: 4px;">
            <div style="background: linear-gradient(135deg, #4F46E5, #7C3AED); color: white; width: 32px; height: 32px; border-radius: 8px; display:flex; align-items:center; justify-content:center; font-weight: 700;">✨</div>
            <h3 style="font-size: 1.15rem; font-weight: 700; color: #0F172A; margin:0;">AI Delivery Assistant</h3>
        </div>
        <p style="color: #64748B; font-size: 0.875rem; margin-bottom: 1.25rem;">Ask natural language questions about risk factors, milestone blockages, or owner responsibilities across all client accounts.</p>
    </div>
    """, unsafe_allow_html=True)

    query_col, btn_col = st.columns([5, 1])
    with query_col:
        query = st.text_input(
            label="query_input",
            label_visibility="collapsed",
            placeholder="e.g., 'Which projects are blocked?' or 'Who owns Orion Logistics?' or 'What is at risk?'",
            key="nl_query"
        )
    with btn_col:
        ask_btn = st.button("Ask AI ✨", key="ask_btn", use_container_width=True, type="primary")

    # Quick question chips
    st.markdown("<div style='font-size: 0.8125rem; font-weight: 600; color: #64748B; margin-top: 8px; margin-bottom: 6px;'>Suggested Queries:</div>", unsafe_allow_html=True)
    chip_cols = st.columns(4)
    quick_questions = [
        "Which projects are blocked?",
        "Who owns each project?",
        "What's at risk?",
        "Which projects have open bugs?"
    ]
    for i, qq in enumerate(quick_questions):
        with chip_cols[i]:
            if st.button(qq, key=f"chip_{i}", use_container_width=True, type="secondary"):
                st.session_state["run_query"] = qq
                st.rerun()

    # Run query logic
    run_query = st.session_state.pop("run_query", None) if "run_query" in st.session_state else None
    query_to_run = run_query or (query if ask_btn else None)

    if query_to_run:
        with st.spinner("✨ Analyzing project data with AI..."):
            answer = query_projects(
                query_to_run,
                st.session_state.get("projects", []),
                st.session_state.get("milestones", []),
                ISSUES,
                st.session_state.get("updates", [])
            )
        st.markdown(f"""
        <div style="background:#EEF2FF; border:1px solid #C7D2FE; border-radius:12px; padding:1.25rem 1.5rem; margin-top:1rem;">
            <div style="font-size:0.8125rem; font-weight:700; color:#4338CA; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:6px;">AI Executive Summary</div>
            <div style="font-size:0.95rem; color:#1E1B4B; line-height:1.6;">{answer}</div>
        </div>
        """, unsafe_allow_html=True)