# UrbanNest Agent — Project Progress & Context

## What Is This Project?
UrbanNest is a property management company managing both residential and 
commercial tenants. This project builds a hierarchical multi-agent AI system 
powered by Python, LangGraph, and the Anthropic Claude API.

---

## The Big Picture — Agent Hierarchy

```
CEO Agent                          (1 instance)
    └── VP Agents                  (multiple)
            └── Director Agents    (multiple)
                    └── Regional Agents (multiple)
                            └── Portfolio Agents (multiple)
                                    └── PM Super Agents (multiple) ← primary focus
                                            └── Lead Agents per Module
                                                    └── Individual Task Agents
```

### Modules under PM Super Agent:
- Finance (invoice, budget, payroll agents)
- HR (hiring, onboarding agents)
- Operations (scheduling agent)
- Maintenance (intake, work order agents) ← built first

---

## Tech Stack
- Language: Python 3.14
- Agent Framework: LangGraph
- AI Model: Claude claude-sonnet-4-6 via Anthropic API
- Audio Transcription: OpenAI Whisper (runs locally, free)
- Audio Processing: ffmpeg
- Config: python-dotenv, pyyaml
- Version Control: Git + GitHub

---

## Folder Structure

```
UrbanNest-Agent/
├── agents/
│   ├── executive/
│   │   ├── ceo_agent.py
│   │   ├── vp_agent.py
│   │   └── director_agent.py
│   ├── management/
│   │   ├── regional_agent.py
│   │   └── portfolio_agent.py
│   ├── project/
│   │   └── pm_super_agent.py
│   └── modules/
│       ├── finance/
│       │   ├── lead_agent.py
│       │   ├── invoice_agent.py
│       │   ├── budget_agent.py
│       │   └── payroll_agent.py
│       ├── hr/
│       │   ├── lead_agent.py
│       │   ├── hiring_agent.py
│       │   └── onboarding_agent.py
│       ├── operations/
│       │   ├── lead_agent.py
│       │   └── scheduling_agent.py
│       └── maintenance/
│           ├── lead_agent.py        ← next to build
│           ├── state.py             ← DONE
│           ├── intake_agent.py      ← DONE
│           └── work_order_agent.py
├── graphs/
│   ├── executive_graph.py
│   ├── management_graph.py
│   ├── pm_graph.py
│   └── module_graph.py
├── state/
│   ├── base_state.py
│   ├── executive_state.py
│   ├── pm_state.py
│   └── module_state.py
├── tools/
│   ├── transcription.py    ← DONE (Whisper)
│   ├── summarizer.py       ← DONE (Claude API)
│   ├── extraction.py       ← DONE (Claude API + priority rules)
│   ├── finance_tools.py
│   ├── hr_tools.py
│   ├── ops_tools.py
│   └── escalation_tools.py
├── prompts/
│   ├── ceo.md
│   ├── vp.md
│   ├── pm_super.md
│   ├── finance_lead.md
│   ├── hr_lead.md
│   ├── ops_lead.md
│   └── maintenance_lead.md
├── memory/
│   ├── checkpointer.py
│   └── context_store.py
├── config/
│   ├── settings.py         ← DONE
│   └── hierarchy.yaml
├── tests/
│   ├── audio/
│   │   └── test_call.mp3   ← DONE (test audio file)
│   ├── test_pm_agent.py
│   └── test_graphs.py
├── main.py                 ← DONE (test runner)
├── requirements.txt
├── .env                    ← DONE (API key stored here, never commit)
├── .gitignore              ← DONE
└── README.md
```

---

## What Is Built and Working

### Session 1 — June 19, 2026

#### 1. Project Setup
- Created local folder: `UrbanNest-Agent`
- Created GitHub repository: `github.com/devwebknots/UrbanNest-Agent`
- Linked local folder to GitHub via VS Code
- Set up Python virtual environment (`venv`)
- Installed all dependencies:
  - langgraph, langchain-anthropic, anthropic
  - python-dotenv, pyyaml
  - openai-whisper, ffmpeg

#### 2. Anthropic API
- Created account at console.anthropic.com
- Generated API key (stored in `.env` only)
- Confirmed $5 free credit loaded
- Pay-as-you-go model — no monthly subscription needed
- Usage after Session 1: ~502 tokens (less than $0.001)

#### 3. Maintenance Intake Agent — FULLY WORKING
**Purpose:** Process tenant maintenance calls (audio or text) and 
produce a structured maintenance ticket automatically.

**Files built:**
- `config/settings.py` — loads API key and model name
- `agents/modules/maintenance/state.py` — defines agent memory/state
- `tools/summarizer.py` — sends transcript to Claude, returns clean summary
- `tools/extraction.py` — sends transcript to Claude, extracts structured fields
- `tools/transcription.py` — converts MP3 audio to text using Whisper
- `agents/modules/maintenance/intake_agent.py` — orchestrates all steps
- `main.py` — test runner

**Agent workflow:**
```
Input (audio or text transcript)
        ↓
Step 1: Summarize → clean professional summary
        ↓
Step 2: Extract fields → issue, unit, priority, category
        ↓
Step 3: Decision → should_create_ticket = true/false
        ↓
Output: JSON ticket
```

**Sample output:**
```json
{
  "transcript": "Hi, this is Mike from Unit 307...",
  "summary": "Tenant Mike from Unit 307 reported that his air 
               conditioning unit stopped working as of last night...",
  "issue": "Air conditioning unit has stopped working completely",
  "unit": "307",
  "priority": "high",
  "category": "hvac",
  "should_create_ticket": true,
  "error": null
}
```

**Tested with:**
- Option 2: Fake text transcript (Sarah, Unit 204, leaking pipe)
- Option 3: Real MP3 audio file (Mike, Unit 307, AC not working)
- Low priority scenario: Garden not cleaned up (Jennifer, Unit 512)

#### 4. Priority Rules Engine
Priority is determined by explicit rules given to Claude:

- **HIGH:** No electricity, no water, no heat, no AC, flooding, 
  fire risk, gas leak, sewage, security issues, elderly or children 
  affected, words like "urgent" / "emergency" / "dangerous"
- **LOW:** Cosmetic issues (paint, carpet, scratches), non-essential 
  appliances, tenant says "no rush" or "whenever"
- **MEDIUM:** Everything else

---

## Key Decisions Made

### 1. Rules should be configurable by PM, not hardcoded
Currently priority rules live inside `extraction.py` as a prompt.
In the next phase, these rules should:
- Be stored in a database
- Be editable by the PM through a portal (PM Portal)
- Be fetched dynamically by the agent at runtime
- Require no developer involvement to change

### 2. Audio transcription uses Whisper (local), not Claude API
Claude API does not support audio files directly.
Whisper runs locally on the Mac, is free, and works offline after 
the first model download (~140MB).

### 3. In production, audio comes from a telephony provider
Real tenant calls will go through a service like Twilio or Bland.ai.
The phone provider records the call and sends the MP3 to the agent 
automatically. No manual file handling needed.

---

## What To Build Next

### Immediate next steps:
1. **Maintenance Lead Agent** — receives tickets from Intake Agent, 
   assigns to work order agent, tracks status
2. **Database connection** — store tickets in a real database (SQLite 
   to start, PostgreSQL for production)
3. **PM Portal rules engine** — allow PM to configure priority rules, 
   categories, and routing without touching code

### Further out:
4. PM Super Agent — oversees all module lead agents
5. Portfolio Agent — oversees multiple PM Super Agents
6. Regional → Director → VP → CEO agents
7. Twilio integration for real phone calls
8. Dashboard for viewing and managing tickets

---

## Important Notes
- Never commit `.env` to GitHub — API key lives there
- Always activate venv before running: `source venv/bin/activate`
- Model in use: `claude-sonnet-4-6`
- GitHub repo: `https://github.com/devwebknots/UrbanNest-Agent`
- All agent files that are not yet built are empty placeholder files
