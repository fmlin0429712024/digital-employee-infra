# Capstone Project: OpenClaw Digital Employee

## Context

This repository is my capstone project. I built a practical “Digital Employee” using **OpenClaw** (open-source agent framework) running on **GCP**.

**Presenter:** Forest Lin  
**Date:** February 8, 2026

---

## Knowledge Alignment (Course Topics → What I Built)

| Knowledge area | In this project |
|---|---|
| GenAI stack | Channels → Gateway → LLM → SKILLS → APIs |
| LLMOps | Fallbacks, cost controls, runbooks |
| Foundational models | Gemini routing (Flash/Pro), Ollama option |
| Local deployment | Attempted GPU/local inference; not used in current deployment |
| Prompt engineering | `SKILL.md` patterns + examples |
| APIs / integration | Google Workspace via Python CLIs |
| Retrieval | Web search + Drive search |
| Memory | Persistent memory (SQLite) |
| Agentic AI | Tool selection + action execution |
| Fine-tuning / quantization | Explored (LoRA/QLoRA concepts); not used in production |

---

## 1) Digital Assistant Value Propositions (Early Adoption Guide)

### Key experience goals
- **Proactive** (suggest next steps)
- **24×7** (long-lasting process)

### What it does for me (safe value)
1. **Manage my knowledge & information**
   - Notes, summaries, TODOs, checklists
   - Drive / docs search

2. **No sensitive jobs**
   - No passwords / banking / tax / legal / medical
   - No delete / IAM / external share without confirm

3. **Do activities without sensitivities (examples)**
   - Email draft + summary (send after confirm)
   - Docs: notes / SOP / weekly report
   - Checklists: travel / onboarding
   - Calendar: suggest times, create after confirm

4. **Personal assistant: no public leaking**
   - Private by default
   - No public post; no external Drive share without confirm

---

## 2) The Solution

**OpenClaw Gateway** runs on a GCP VM and connects:
- **Channels** (Telegram / WhatsApp / Voice)
- **Models** (Antigravity + Vertex AI + optional local Ollama)
- **SKILLS** (Python scripts that call real APIs)
- **Memory** (persistent recall)

---

## 3) System Architecture (High-Level)

```
User (Telegram/WhatsApp/Voice)
  -> OpenClaw Gateway (GCP VM)
     -> Memory (persistent)
     -> Model (LLM)
     -> SKILLS (Python tools)
        -> Google Workspace APIs
  -> Response
```

---

## 4) Core Design Choices (Why it Works)

### A) Agentic workflow (not a chatbot)
- The agent decides which SKILL to call
- Executes a command/tool
- Returns structured results

### B) SKILLS as the automation engine
SKILLS are simple, testable Python CLIs described by `SKILL.md`. This makes the system extensible without modifying the framework.

Example (pattern):
```bash
python3 ~/.openclaw/scripts/<skill>-cli.py <action> [--flags]
```

### C) Reliability via model fallback
Multiple providers/models ensure the agent keeps working if one tier fails or quotas are hit.

---

## 5) Model Strategy (Cost + Availability)

The system routes requests across:
- **Tier 1:** Antigravity (FREE)
- **Tier 2:** Vertex AI `gemini-2.0-flash` (paid, cost-optimized)
- **Tier 3:** Vertex AI `gemini-1.5-pro` (paid, for harder tasks)
- **Optional local:** Ollama `llama3.2:1b` (CPU)

### Cost Optimization Result
We switched primary Vertex model:
- From: `gemini-2.5-flash` ($0.15 / 1M input tokens)
- To: `gemini-2.0-flash` ($0.10 / 1M input tokens)

**Result:** ~33% input-token cost reduction.

### Attempted (Not Used in Current Deployment)
- **Local deployment** (GPU/local inference): tested as an option, but not cost-effective / not needed for current setup.
- **Fine-tuning** (LoRA/QLoRA): evaluated as a concept; current solution uses prompt + SKILLS instead.

---

## 6) Google Workspace Automation (Showcase)

### Active and verified on the VM
- **Gmail:** list/read/send
- **Calendar:** list/create
- **Drive:** list/search/upload/download/share

### Ready to deploy (same OAuth flow approach)
- **Sheets:** create/read/write/append
- **Docs:** create/read/append
- **Slides:** create/read/add-slide

---

## 7) Security & Privacy (Practical)

- **Dedicated environment:** Run the assistant on a dedicated VM/machine (not your primary laptop) to reduce blast radius.
- **Isolated credentials:** Use a dedicated Google account for the assistant (separate from personal/work accounts).
- **Granular permissions:** Share only specific folders/files and grant only required Google scopes (principle of least privilege).
- **Credential storage:** OAuth tokens in `~/.openclaw/keys/` (restricted file permissions); secrets never committed to git (`.env`, tokens, keys).
- **GCP IAM:** Access via VM **service account** with least privilege.
- **Network access:** SSH via **IAP tunnel** (no open inbound SSH).
- **Prompt injection awareness:** Treat email/web content as untrusted input; avoid running destructive actions from unverified instructions; add confirmation steps for deletes/shares.

---

## 8) Demo Script (What I’ll Show Live)

### A) Email
"Check my unread emails"  
"Send an email to X with subject Y"

### B) Calendar
"What’s on my calendar this week?"  
"Schedule a meeting tomorrow at 2pm"

### C) Drive
"List my recent Drive files"  
"Search Drive for <keyword>"  
"Upload this file to Drive and share it with <email>"

### D) (Optional) Sheets/Docs/Slides
"Create a spreadsheet called Q1 Report"  
"Create a document called Meeting Notes"  
"Create a presentation called Team Update"

---

## 9) Key Takeaways

1. Agents become useful when they can **take actions** through tools.
2. SKILLS make the system extensible and testable.
3. Reliability requires fallback and observability.
4. Cost control is real: routing + model choice reduced spend.
5. Google Workspace integration makes the agent immediately valuable.

---

## Links (Repo Map)

- Setup commands: `setup/commands.md`
- Security practices: `security/best-practices.md`
- Architecture: `architecture/system-overview.md`
- Skills inventory: `skills/current-skills.md`
- Google Workspace showcase: `skills/google-workspace-showcase.md`

---

## Thank You

Project: https://github.com/fmlin0429712024/digital-employee-infra
