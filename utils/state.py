"""Session-state helpers for mutable dashboard data."""

from copy import deepcopy

import streamlit as st

from mock_data import ISSUES


def init_state(projects, milestones, updates) -> None:
    """Initialize mutable, per-session copies of dashboard data once."""
    if "projects" not in st.session_state:
        st.session_state["projects"] = deepcopy(projects)
    if "milestones" not in st.session_state:
        st.session_state["milestones"] = deepcopy(milestones)
    if "updates" not in st.session_state:
        st.session_state["updates"] = deepcopy(updates)
    # UI state defaults
    if "selected_project_id" not in st.session_state:
        st.session_state["selected_project_id"] = None
    if "view_mode" not in st.session_state:
        st.session_state["view_mode"] = "internal"


def get_project(project_id):
    """Return a project from the mutable session state."""
    return next(
        (project for project in st.session_state.get("projects", []) if project.id == project_id),
        None,
    )


def get_milestones(project_id):
    """Return the selected project's mutable milestones."""
    return [milestone for milestone in st.session_state.get("milestones", []) if milestone.project_id == project_id]


def get_issues(project_id):
    """Return the selected project's source issues."""
    return [issue for issue in ISSUES if issue.project_id == project_id]


def get_updates(project_id):
    """Return updates newest first for the selected project."""
    try:
        return sorted(
            (update for update in st.session_state.get("updates", []) if update.project_id == project_id),
            key=lambda update: update.timestamp,
            reverse=True,
        )
    except Exception:
        return [update for update in st.session_state.get("updates", []) if update.project_id == project_id]


def update_milestone_status(milestone_id, new_status) -> None:
    """Mutate the status of one milestone in this browser session."""
    milestones = st.session_state.get("milestones", [])
    for i, milestone in enumerate(milestones):
        if milestone.id == milestone_id:
            st.session_state["milestones"][i].status = new_status
            return


def prepend_update(update_obj) -> None:
    """Add a newly created update to the front of this session's feed."""
    st.session_state.setdefault("updates", []).insert(0, update_obj)


def get_or_compute_health(project_id, project, milestones, issues, updates):
    """
    Get cached health score or compute new one.
    Cache invalidates when milestone statuses change.
    """
    cache_key = f"health_{project_id}"
    sig_key = f"health_sig_{project_id}"
    
    # Create signature from milestone statuses
    milestone_sig = str([(m.id, m.status) for m in milestones])
    
    if cache_key not in st.session_state or st.session_state.get(sig_key) != milestone_sig:
        from ai_helper import get_project_health
        health = get_project_health(project, milestones, issues, updates)
        st.session_state[cache_key] = health
        st.session_state[sig_key] = milestone_sig
    
    return st.session_state[cache_key]