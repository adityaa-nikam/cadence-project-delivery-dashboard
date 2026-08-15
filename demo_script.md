# Demo Script — Project Delivery Dashboard

## Setup (before judges arrive)
- Open the app to the Overview page
- Ensure GEMINI_API_KEY is set and shows ✅ in sidebar
- Have this raw update text ready to paste (copy it):

### Demo Update Text (paste this when demoing):
```
hey team - quick update from the call with their IT guy this morning. 
the firewall rules are FINALLY approved and being pushed today or tmrw. 
so the integration testing should unblock by EOD friday hopefully. 
also the UAT environment issue is resolved, mike confirmed its back up. 
we're probably back on track for the original go-live date
```

## Demo Flow (5 minutes)

| Time | Step | Action | What Judges See |
|------|------|--------|-----------------|
| 0:00 | **Overview** | Open app to Overview page | 6 project cards, metrics bar (Projects 6, On Track 2, At Risk 2, Blocked Tasks 3, AI Updates 0), **⏰ Stale** badges on **NovaBridge** (12d) and **Stellar Dynamics** (9d) |
| 0:30 | **Click NovaBridge** | Click "View Details →" on NovaBridge card | Detail page: **CRITICAL** health score, 2 🚧 Blocked milestones (Database Migration, Firewall Rules), **⏰ Stale** banner (12d), internal notes about DevOps bottleneck |
| 1:00 | **Internal View** | Note the Internal Notes expander (open by default) | Shows internal context: "Two milestones blocked on their DevOps team... Last sync was 12 days ago" |
| 1:30 | **Customer View** | Toggle to "👤 Customer View" | Gradient "Customer Project Portal" banner appears; internal notes gone; **Blocked milestones still visible** (not internal); **Stale** badge gone; Issues panel shows only 2 issues (Bug hidden); Updates feed shows only structured summaries, no raw text |
| 2:00 | **Back to Internal** | Toggle back to "🔒 Internal View" | All internal content returns; Issues shows 3 items (Bug visible); Update feed shows "📧 Raw message" expanders |
| 2:30 | **Issues Panel** | Scroll to Issues section | Shows **Bug: Database migration timeout errors** — explains *why* health is Critical |
| 3:00 | **⭐ CORE DEMO: AI Update** | Paste demo update text → Click **"✨ Process with AI"** | Spinner → **Summary appears**: "Firewall rules approved and pushed; integration testing unblocked; go-live on track" → **Milestone updates**: "Firewall Rules Configuration" **Blocked → Done** → Toast: ✅ Milestone updated → **Health Score auto-refreshes** from Critical → **At Risk** or **Healthy** |
| 4:00 | **📧 Draft Email** | Click **"✉️ Draft Customer Email"** | AI generates: Subject "NovaBridge — Delivery Status Update", **🔴 Urgent tone** badge, professional 3-paragraph email acknowledging blocker, stating action, promising Friday update; editable body; "🔄 Regenerate" button |
| 4:30 | **Overview + NL Query** | Click "← All Projects" → Type "which projects need attention?" → Enter | AI Answer: "NovaBridge Systems is Critical with 2 blocked milestones and no updates in 12 days. Stellar Dynamics is Delayed with 9 days since last update. Both need attention." |
| 5:00 | **Wrap Up** | Mention deploy | "Deployed on Streamlit Community Cloud, zero-config beyond API key" |

## Key Talking Points
- **"No more status-update bottleneck — anyone can see live status"**  
- **"AI turns a messy Slack message into a structured project record"**  
- **"The customer never sees internal blockers — only the clean view"**  
- **"Health score updates automatically when a milestone is resolved"**  
- **"One-click email draft saves 15 minutes per status update"**  
- **"Natural language query means stakeholders self-serve — no more 'can you send me a status?'"**

## Quick Reset Between Demos
If you need to reset the demo state:
1. Click "← All Projects" to return to Overview
2. Refresh browser (F5) to reset session state
3. Orion's health will be "Healthy", NovaBridge will be "Critical" again

## Troubleshooting
- **AI features show warning**: Check `.env` has `GEMINI_API_KEY=your_key`
- **Milestone doesn't update**: Ensure demo text mentions "firewall" and "integration testing"
- **Health score doesn't change**: Click "🔄 Refresh Health Score" button
- **Email tone not urgent**: Regenerate (it samples)