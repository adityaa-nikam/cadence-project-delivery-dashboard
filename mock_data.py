"""Compelling demo mock data for the Cadence delivery dashboard."""

from dataclasses import dataclass
from datetime import datetime, timedelta


def days_ago(n: int) -> str:
    """Return ISO timestamp for n days ago."""
    return (datetime.now() - timedelta(days=n)).isoformat()


@dataclass
class Project:
    id: str
    name: str
    owners: list
    overall_status: str
    internal_notes: str


@dataclass
class Milestone:
    id: str
    project_id: str
    title: str
    status: str
    due_date: str
    internal_only: bool


@dataclass
class Issue:
    id: str
    project_id: str
    title: str
    category: str
    internal_only: bool


@dataclass
class Update:
    id: str
    project_id: str
    timestamp: str
    raw_text: str
    structured_summary: str
    affected_milestone: str
    status_change: str
    is_ai_processed: bool


PROJECTS = [
    Project(
        "orion",
        "Orion Logistics",
        ["Maya Chen", "Jake Porter"],
        "On Track",
        "Firewall approval was the key schedule risk; escalation with their CIO resolved it. "
        "Client's VP of Ops wants weekly status emails - keep them high-level."
    ),
    Project(
        "novabridge",
        "NovaBridge Systems",
        ["Priya Shah"],
        "At Risk",
        "Two milestones blocked on their DevOps team - database migration and firewall rules. "
        "Their lead dev is on PTO until next week. Last sync was 12 days ago."
    ),
    Project(
        "celera",
        "Celera Health",
        ["Dr. Elena Ruiz", "Samir Patel"],
        "At Risk",
        "HIPAA compliance review pending - legal team needs to sign off before UAT. "
        "Feature request for audit export is blocking scope lock."
    ),
    Project(
        "driftwood",
        "Driftwood Retail",
        ["Tessa Morgan"],
        "On Track",
        "Holiday launch window fixed for Nov 15. Inventory sync stable. "
        "Only minor catalog QA items remaining."
    ),
    Project(
        "quantum",
        "Quantum Perch",
        ["Leo Grant", "Nina Okafor"],
        "On Track",
        "New project - kickoff completed last week. Mostly discovery phase. "
        "Vendor sandbox access just granted yesterday."
    ),
    Project(
        "stellar",
        "Stellar Dynamics",
        ["Arun Mehta"],
        "Delayed",
        "Customer's security team added new compliance requirements mid-project. "
        "Two milestones delayed by 3 weeks. Weekly evidence packets now required."
    ),
]

MILESTONES = [
    # Orion Logistics - 80% done, healthy (5 milestones, 1 internal)
    Milestone("orion-m1", "orion", "Discovery & Requirements", "Done", "2026-07-15", False),
    Milestone("orion-m2", "orion", "Architecture Review", "Done", "2026-07-28", False),
    Milestone("orion-m3", "orion", "API Integration Development", "Done", "2026-08-10", False),
    Milestone("orion-m4", "orion", "Firewall Access Approval", "Done", "2026-08-20", False),  # Was blocked, now done
    Milestone("orion-m5", "orion", "Dispatcher Pilot & Go-Live", "Open", "2026-09-05", True),  # Internal

    # NovaBridge Systems - CRITICAL, 2 blocked, stale (5 milestones, 1 internal)
    Milestone("nova-m1", "novabridge", "Project Kickoff", "Done", "2026-07-01", False),
    Milestone("nova-m2", "novabridge", "Database Migration", "Blocked", "2026-08-15", False),  # BLOCKED
    Milestone("nova-m3", "novabridge", "Firewall Rules Configuration", "Blocked", "2026-08-18", False),  # BLOCKED
    Milestone("nova-m4", "novabridge", "Integration Testing", "Open", "2026-09-01", False),
    Milestone("nova-m5", "novabridge", "UAT & Go-Live", "Open", "2026-09-15", True),  # Internal

    # Celera Health - At Risk, 1 blocked, important feature request (5 milestones, 1 internal)
    Milestone("celera-m1", "celera", "Requirements & Compliance Scoping", "Done", "2026-07-10", False),
    Milestone("celera-m2", "celera", "HIPAA Compliance Review", "Blocked", "2026-08-25", False),  # BLOCKED
    Milestone("celera-m3", "celera", "FHIR API Development", "Done", "2026-08-20", False),
    Milestone("celera-m4", "celera", "Audit Export Feature", "Open", "2026-09-10", False),  # Feature request tied here
    Milestone("celera-m5", "celera", "Care Team UAT & Go-Live", "Open", "2026-09-20", True),  # Internal

    # Driftwood Retail - On Track, straightforward (5 milestones, 1 internal)
    Milestone("drift-m1", "driftwood", "Catalog Data Audit", "Done", "2026-07-20", False),
    Milestone("drift-m2", "driftwood", "Inventory Sync Setup", "Done", "2026-08-05", False),
    Milestone("drift-m3", "driftwood", "Storefront Theme QA", "Done", "2026-08-28", False),
    Milestone("drift-m4", "driftwood", "Holiday Launch Prep", "Open", "2026-09-01", False),
    Milestone("drift-m5", "driftwood", "Holiday Launch Go-Live", "Open", "2026-11-15", True),  # Internal

    # Quantum Perch - New project, mostly open (5 milestones, 1 internal)
    Milestone("quant-m1", "quantum", "Project Kickoff & Discovery", "Done", "2026-08-10", False),
    Milestone("quant-m2", "quantum", "Vendor Sandbox Access", "Done", "2026-08-18", False),  # Just granted
    Milestone("quant-m3", "quantum", "Telemetry Pipeline Design", "Open", "2026-09-05", False),
    Milestone("quant-m4", "quantum", "Control Room Dashboard", "Open", "2026-09-20", False),
    Milestone("quant-m5", "quantum", "Pilot & Production Rollout", "Open", "2026-10-15", True),  # Internal

    # Stellar Dynamics - Delayed, multiple issues (5 milestones, 1 internal)
    Milestone("stellar-m1", "stellar", "Security Discovery", "Done", "2026-07-15", False),
    Milestone("stellar-m2", "stellar", "Identity Federation", "Done", "2026-08-01", False),
    Milestone("stellar-m3", "stellar", "Simulation Data Import", "Open", "2026-09-10", False),  # Delayed
    Milestone("stellar-m4", "stellar", "Mission Control Pilot", "Open", "2026-09-25", False),  # Delayed
    Milestone("stellar-m5", "stellar", "Security Evidence Pack Delivery", "Open", "2026-10-05", True),  # Internal
]

ISSUES = [
    # Orion - clean
    Issue("orion-i1", "orion", "Rate-limit handling for legacy API", "Bug", False),
    Issue("orion-i2", "orion", "Request for manual route override screen", "Feature Request", False),
    Issue("orion-i3", "orion", "Internal security review for firewall rules", "Implementation", True),

    # NovaBridge - CRITICAL, has Bug, stale
    Issue("nova-i1", "novabridge", "Database migration timeout errors", "Bug", False),
    Issue("nova-i2", "novabridge", "Question about contractor SSO access", "Question", False),
    Issue("nova-i3", "novabridge", "Low pilot engagement in finance team", "Support", True),

    # Celera - At Risk, Feature Request important
    Issue("celera-i1", "celera", "FHIR allergy field mapping ambiguity", "Question", False),
    Issue("celera-i2", "celera", "Request for patient consent audit export", "Feature Request", False),  # Tied to blocked milestone
    Issue("celera-i3", "celera", "Legal clause escalation tracker", "Implementation", True),

    # Driftwood - clean
    Issue("drift-i1", "driftwood", "Variant images intermittently missing", "Bug", False),
    Issue("drift-i2", "driftwood", "Support request for bulk catalog edits", "Support", False),
    Issue("drift-i3", "driftwood", "Internal margin review for holiday promos", "Implementation", True),

    # Quantum - new project
    Issue("quant-i1", "quantum", "Sandbox token expires during long test runs", "Bug", False),
    Issue("quant-i2", "quantum", "Question about sensor data retention", "Question", False),
    Issue("quant-i3", "quantum", "Internal vendor assessment pending", "Implementation", True),

    # Stellar - Delayed, multiple issues
    Issue("stellar-i1", "stellar", "Request for weekly security evidence export", "Feature Request", False),
    Issue("stellar-i2", "stellar", "Simulation upload checksum mismatch", "Bug", False),
    Issue("stellar-i3", "stellar", "Internal threat-model follow-up", "Implementation", True),
]

UPDATES = [
    # Orion Logistics - 80% done, recent AI-friendly update (4 days ago, 8 days ago, 12 days ago)
    # Latest is 4 days ago - NOT stale
    Update(
        "orion-u1", "orion", days_ago(4),
        "ok so the firewall rules finally got pushed to prod this morning - their network team confirmed. "
        "integration testing unblocked, jake ran the full suite and everything green. "
        "moving Dispatcher Pilot to Open, target go-live still sept 5th. "
        "also their VP of ops asked for weekly status emails, maya drafting template now",
        "", "Firewall Access Approval", "", False
    ),
    Update(
        "orion-u2", "orion", days_ago(8),
        "their network guy said firewall rules approved by CIO but waiting on infra team to push. "
        "might be tomorrow, might be next week - no firm ETA. "
        "blocking integration testing for now. jake set up retry logic as workaround. "
        "maya sending escalation email to their CTO",
        "", "Firewall Access Approval", "", False
    ),
    Update(
        "orion-u3", "orion", days_ago(12),
        "architecture review passed, their CTO signed off. "
        "api integration dev complete - jake pushed last commit yesterday. "
        "just waiting on firewall access now. their infra team is slow to respond. "
        "may need to escalate through maya's contact at their CIO office",
        "", "API Integration Development", "", False
    ),

    # NovaBridge Systems - CRITICAL, 2 BLOCKED milestones, STALE (12 days ago latest)
    Update(
        "nova-u1", "novabridge", days_ago(12),
        "ok so the database migration is technically done but their devops guy said "
        "the firewall rules haven't been pushed yet so we're still blocked on the integration testing. "
        "also mike mentioned the UAT env is down for maintenance till thursday. "
        "FYI the kickoff recording is in drive",
        "", "Database Migration", "", False
    ),
    Update(
        "nova-u2", "novabridge", days_ago(18),
        "database migration scripts ran clean in staging. "
        "their lead dev (alex) is on PTO until next monday - no one else has prod access. "
        "firewall rules PR is open but needs security team approval. "
        "priya said she'll follow up with their security lead tomorrow",
        "", "Database Migration", "", False
    ),
    Update(
        "nova-u3", "novabridge", days_ago(24),
        "kickoff went well, their team seems engaged. "
        "database migration is the big risk - their devops is a bottleneck. "
        "priya set up weekly syncs for tuesdays 10am. "
        "also need to clarify contractor SSO access - they have 3 contractors",
        "", "Project Kickoff", "", False
    ),

    # Celera Health - At Risk, 1 blocked, important feature request
    Update(
        "celera-u1", "celera", days_ago(3),
        "legal team reviewed the HIPAA compliance checklist - they need one more "
        "round of edits on the data processing agreement. "
        "samir said it might take another week. "
        "audit export feature request is now blocking scope lock for UAT. "
        "dr. ruiz said clinical team can't sign off without it",
        "", "HIPAA Compliance Review", "", False
    ),
    Update(
        "celera-u2", "celera", days_ago(9),
        "FHIR API development complete, all endpoints tested. "
        "clinical team signed off on requirements. "
        "allergies mapping still confusing - source has 3 different code sets. "
        "samir working with their clinical informatics lead to resolve",
        "", "FHIR API Development", "", False
    ),
    Update(
        "celera-u3", "celera", days_ago(15),
        "requirements scoping done. compliance team flagged the audit export requirement "
        "that wasn't in original scope. samir checking if it's phase 1 or phase 2. "
        "legal needs to review data processing agreement for HIPAA",
        "", "Requirements & Compliance Scoping", "", False
    ),

    # Driftwood Retail - On Track, clean
    Update(
        "drift-u1", "driftwood", days_ago(2),
        "theme QA passed - all viewport sizes look good. "
        "inventory sync has been stable for 2 weeks straight. "
        "tessa confirmed holiday launch on track for nov 15. "
        "just need to finish catalog QA on the new product variants",
        "", "Storefront Theme QA", "", False
    ),
    Update(
        "drift-u2", "driftwood", days_ago(6),
        "inventory sync ran clean overnight again. "
        "catalog data audit complete - only 12 variant images missing. "
        "merchant team wants bulk edit help before holiday load. "
        "tessa sent them the csv template",
        "", "Inventory Sync Setup", "", False
    ),
    Update(
        "drift-u3", "driftwood", days_ago(10),
        "catalog audit done. theme QA starting monday. "
        "holiday launch window locked for nov 15 - no scope changes. "
        "tessa confirmed with their VP of ecommerce",
        "", "Catalog Data Audit", "", False
    ),

    # Quantum Perch - New project, one AI update (recent)
    Update(
        "quant-u1", "quantum", days_ago(1),
        "vendor sandbox access finally granted yesterday - their security team "
        "approved after 2 weeks of back and forth. "
        "nina and leo can now start telemetry pipeline design. "
        "kickoff recording is in the drive folder",
        "", "Vendor Sandbox Access", "", False
    ),
    Update(
        "quant-u2", "quantum", days_ago(5),
        "kickoff went well - their team is small but technical. "
        "we need sandbox access to start telemetry design. "
        "their security team said 2 weeks for approval. "
        "nina drafting the data retention questionnaire for their legal team",
        "", "Vendor Sandbox Access", "", False
    ),
    Update(
        "quant-u3", "quantum", days_ago(10),
        "project kickoff completed. team is leo, nina, and their cto + 2 engineers. "
        "scope is telemetry ingestion + control room dashboard. "
        "timeline is aggressive - 8 weeks to pilot. "
        "first milestone: get vendor sandbox access",
        "", "Project Kickoff & Discovery", "", False
    ),

    # Stellar Dynamics - Delayed, multiple issues, stale (9 days ago)
    Update(
        "stellar-u1", "stellar", days_ago(9),
        "their security team dropped new compliance requirements on us mid-project - "
        "now need weekly evidence packets instead of monthly. "
        "simulation data import delayed by 2 weeks because of this. "
        "arun is updating the project plan and will send revised timeline by friday. "
        "mission control pilot now targeting late september",
        "", "Simulation Data Import", "", False
    ),
    Update(
        "stellar-u2", "stellar", days_ago(16),
        "identity federation passed their test suite - good. "
        "simulation upload had checksum mismatch on one file but rerun worked. "
        "arun adding better logging. their security team also wants the evidence "
        "packet weekly not monthly now - that's a lot of extra work",
        "", "Simulation Data Import", "", False
    ),
    Update(
        "stellar-u3", "stellar", days_ago(22),
        "security discovery phase complete. their team is very thorough - "
        "requesting threat model review and weekly evidence. "
        "mission control pilot invite list drafted. customer is super excited "
        "but we need to manage expectations on timeline given new requirements",
        "", "Security Discovery", "", False
    ),
]