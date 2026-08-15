# Project Delivery Dashboard 📦

A unified internal + customer-facing delivery dashboard with AI-powered 
update parsing. Built for the FlytBase "AI-Native Customer Teams" hackathon.

## 🚀 Quick Start (Local)

```bash
git clone <your-repo-url>
cd project-delivery-dashboard
pip install -r requirements.txt

# Set your Gemini API key (get free key at aistudio.google.com)
export GEMINI_API_KEY=your_key_here   # Mac/Linux
set GEMINI_API_KEY=your_key_here      # Windows

streamlit run app.py
```

## 🌐 Deploy to Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to share.streamlit.io → New app → select your repo
3. Main file: `app.py`
4. In app settings → Secrets, add:
   `GEMINI_API_KEY = "your_key_here"`
5. Click Deploy

## 📁 File Structure

- `app.py` — Entry point, routing, sidebar
- `mock_data.py` — All synthetic project/milestone/issue/update data
- `ai_helper.py` — Gemini API: update parsing, health score, email draft, NL query
- `pages/overview.py` — Projects list with metrics and NL query
- `pages/detail.py` — Project detail, toggle, milestones, issues, updates feed
- `components/` — Reusable UI widgets
- `utils/state.py` — Session state helpers

## 🔑 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | Yes (for AI features) | Get free at aistudio.google.com |

## ✨ Features

- Projects overview with health metrics
- Internal vs Customer-facing view toggle  
- AI update parsing (messy text → structured status)
- AI project health score (auto-updates on milestone changes)
- One-click customer email draft
- Natural language project queries
- Stale project detection