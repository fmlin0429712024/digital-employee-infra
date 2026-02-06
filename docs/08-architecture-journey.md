# 08 - Architecture Journey: From Baseline to Digital Employee

This document maps the complete architecture evolution, comparing baseline capabilities with enhancements, and providing a clear roadmap for future extensibility.

---

## Part 1: The GAP Analysis

### What is Claude Code CLI (The Gold Standard)?

**Claude Code CLI** is Anthropic's official command-line interface for Claude. It represents the current state-of-the-art in AI-powered development agents.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        CLAUDE CODE CLI ARCHITECTURE                       │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│   ┌─────────────────────────────────────────────────────────────────┐    │
│   │                    👤 USER (Terminal/IDE)                        │    │
│   └─────────────────────────────────────────────────────────────────┘    │
│                                   │                                       │
│                                   ▼                                       │
│   ┌─────────────────────────────────────────────────────────────────┐    │
│   │                      CLAUDE CODE CLI                             │    │
│   │                    (Local Application)                           │    │
│   │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐    │    │
│   │  │ Chat Loop   │ │ Tool Engine │ │ Context Management      │    │    │
│   │  │ (Agentic)   │ │ (Native)    │ │ (Auto-summarization)    │    │    │
│   │  └─────────────┘ └─────────────┘ └─────────────────────────┘    │    │
│   └─────────────────────────────────────────────────────────────────┘    │
│                                   │                                       │
│          ┌────────────────────────┼────────────────────────┐             │
│          ▼                        ▼                        ▼             │
│   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐        │
│   │BUILT-IN TOOLS│        │ MCP SERVERS │         │  SKILLS     │        │
│   ├─────────────┤         ├─────────────┤         ├─────────────┤        │
│   │ Read        │         │ Filesystem  │         │ /commit     │        │
│   │ Write       │         │ GitHub      │         │ /review-pr  │        │
│   │ Edit        │         │ Database    │         │ /init       │        │
│   │ Bash        │         │ Pencil      │         │ Custom...   │        │
│   │ Glob        │         │ Custom...   │         │             │        │
│   │ Grep        │         │             │         │             │        │
│   │ WebFetch    │         │             │         │             │        │
│   │ WebSearch   │         │             │         │             │        │
│   │ Task        │         │             │         │             │        │
│   │ TodoWrite   │         │             │         │             │        │
│   └─────────────┘         └─────────────┘         └─────────────┘        │
│                                   │                                       │
│                                   ▼                                       │
│   ┌─────────────────────────────────────────────────────────────────┐    │
│   │                      ANTHROPIC API                               │    │
│   │                  Claude Opus / Sonnet                            │    │
│   └─────────────────────────────────────────────────────────────────┘    │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

### Claude Code CLI Key Characteristics

| Feature | Description |
|---------|-------------|
| **Runs Locally** | Executes on developer's machine (macOS/Linux) |
| **Single AI Provider** | Anthropic Claude exclusively |
| **On-Demand** | Active only when user runs it |
| **IDE Integration** | VSCode extension available |
| **Built-in Tools** | File ops, bash, search, web access |
| **MCP Protocol** | Extensible via Model Context Protocol servers |
| **Skills System** | Slash commands for common workflows |
| **Task Agents** | Spawns sub-agents for parallel work |
| **Context Unlimited** | Auto-summarization for long sessions |

---

### What is OpenClaw? (Baseline Installation)

**OpenClaw** is an open-source AI gateway that can host multiple AI providers and run as a persistent daemon.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                  OPENCLAW BASELINE (Fresh Install)                        │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│   ┌─────────────────────────────────────────────────────────────────┐    │
│   │                    👤 USER (Local Terminal)                      │    │
│   └─────────────────────────────────────────────────────────────────┘    │
│                                   │                                       │
│                                   ▼                                       │
│   ┌─────────────────────────────────────────────────────────────────┐    │
│   │                      OPENCLAW GATEWAY                            │    │
│   │                    (Local Daemon/CLI)                            │    │
│   │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐    │    │
│   │  │ Chat Loop   │ │ Basic Tools │ │ Session Management      │    │    │
│   │  │ (Agentic)   │ │ (exec/bash) │ │ (Memory optional)       │    │    │
│   │  └─────────────┘ └─────────────┘ └─────────────────────────┘    │    │
│   └─────────────────────────────────────────────────────────────────┘    │
│                                   │                                       │
│                                   ▼                                       │
│   ┌─────────────────────────────────────────────────────────────────┐    │
│   │                    DEFAULT AI PROVIDER                           │    │
│   │           (Configured during install - e.g., OpenAI)             │    │
│   └─────────────────────────────────────────────────────────────────┘    │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

### OpenClaw Baseline Characteristics

| Feature | Description |
|---------|-------------|
| **Runs Locally/Server** | Can run as daemon (24/7 capable) |
| **Multi-Provider** | Supports multiple AI backends |
| **Basic Tools** | exec, bash, file operations |
| **Skills Framework** | Extensible via SKILL.md files |
| **Workspace Config** | TOOLS.md, SOUL.md, AGENTS.md |
| **No Built-in MCP** | Not MCP-native (different extension model) |
| **No Built-in Messaging** | No Telegram/WhatsApp out of box |
| **No Built-in Voice** | No STT/TTS |
| **No Built-in Search** | No web search |

---

## Detailed Comparison: Claude Code vs OpenClaw Baseline

### Tool Capabilities

| Capability | Claude Code CLI | OpenClaw Baseline | GAP |
|------------|-----------------|-------------------|-----|
| **File Read** | Native (Read tool) | Via exec/bash | ~ Similar |
| **File Write** | Native (Write tool) | Via exec/bash | ~ Similar |
| **File Edit** | Native (Edit tool) | Via exec/bash | ~ Similar |
| **Pattern Search** | Native (Glob tool) | Via find/bash | ~ Similar |
| **Content Search** | Native (Grep tool) | Via grep/bash | ~ Similar |
| **Bash Commands** | Native (Bash tool) | Native (exec/bash) | = Same |
| **Web Fetch** | Native (WebFetch) | Not included | GAP |
| **Web Search** | Native (WebSearch) | Not included | GAP |
| **Task Agents** | Native (Task tool) | Not included | GAP |
| **Todo Tracking** | Native (TodoWrite) | Not included | GAP |

### Extension Mechanisms

| Extension Type | Claude Code CLI | OpenClaw Baseline |
|----------------|-----------------|-------------------|
| **Skills** | SKILL.md in ~/.claude/skills/ | SKILL.md in ~/.openclaw/skills/ |
| **MCP Servers** | Full MCP protocol support | Not MCP-native |
| **CLI Scripts** | Via bash/exec | Via exec + CLI scripts |
| **Config Location** | ~/.claude/ | ~/.openclaw/ |

### Operational Model

| Aspect | Claude Code CLI | OpenClaw Baseline |
|--------|-----------------|-------------------|
| **Execution** | On-demand (user runs) | Can run as daemon |
| **Persistence** | Session-based | Configurable |
| **Remote Access** | Local only | Configurable |
| **AI Provider** | Anthropic only | Multi-provider |
| **Cost Model** | API usage (paid) | Provider-dependent |

---

## Part 2: The Journey - What We've Built

### Evolution Timeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EVOLUTION TIMELINE                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PHASE 1: Foundation                                                         │
│  ═══════════════════                                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  OpenClaw Baseline ──► GCP VM Deployment ──► Cloud Persistence       │   │
│  │  (Local install)        (n2-standard-4)       (24/7 availability)    │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  PHASE 2: Intelligence                                                       │
│  ════════════════════                                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Single Provider ──► Multi-Tier Fallback ──► $18K Safety Net         │   │
│  │  (Antigravity)        (3 tiers: FREE→FREE→PAID)  (Vertex AI)         │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  PHASE 3: Communication                                                      │
│  ═════════════════════                                                       │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  CLI Only ──► Telegram ("Pet") ──► WhatsApp ("Mirror") ──► Voice     │   │
│  │  (Terminal)    (Quick commands)    (Deep thinking)       (STT/TTS)   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  PHASE 4: Capabilities                                                       │
│  ════════════════════                                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Basic Agent ──► Browser ──► Memory ──► Documents ──► Search         │   │
│  │  (bash/exec)    (Playwright) (SQLite)   (PDF/OCR)    (Brave API)     │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  PHASE 5: Reliability                                                        │
│  ════════════════════                                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Manual Ops ──► Systemd ──► Log Cleanup ──► Backups ──► Monitoring   │   │
│  │  (manual start)  (auto-start)  (30-day)    (GCS daily)  (health)     │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  PHASE 6: Skills (CURRENT)                                                   │
│  ═════════════════════════                                                   │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Built-in Only ──► Gmail Skill ──► Calendar Skill ──► [Next...]      │   │
│  │  (bash/exec)        (send/read)     (events)          (Drive? Slack?)│   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Part 3: Current Architecture (Full Picture)

### Complete System Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      DIGITAL EMPLOYEE "TURTLE" - CURRENT STATE                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ╔═══════════════════════════════════════════════════════════════════════════╗  │
│  ║                           COMMAND CENTER                                   ║  │
│  ╠═══════════════════════════════════════════════════════════════════════════╣  │
│  ║                                                                           ║  │
│  ║   📱 Telegram        📱 WhatsApp         🎤 Voice           💻 CLI       ║  │
│  ║     "Pet"             "Mirror"          (FFmpeg)          (Direct)       ║  │
│  ║  Quick commands     Deep thinking     Voice notes       Dev access       ║  │
│  ║                                                                           ║  │
│  ╚═════════════════════════════════╦═════════════════════════════════════════╝  │
│                                    ║                                             │
│                                    ▼                                             │
│  ╔═══════════════════════════════════════════════════════════════════════════╗  │
│  ║                        🦞 OPENCLAW GATEWAY                                 ║  │
│  ║                         (2026 Core Engine)                                 ║  │
│  ║                     24/7 Persistent Agent Host                             ║  │
│  ╠═══════════════════════════════════════════════════════════════════════════╣  │
│  ║                                                                           ║  │
│  ║  ┌─────────────────────────────────────────────────────────────────────┐ ║  │
│  ║  │                        CORE ENGINE                                   │ ║  │
│  ║  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐│ ║  │
│  ║  │  │ Agentic  │  │ Tool     │  │ Skill    │  │ Context/Memory       ││ ║  │
│  ║  │  │ Loop     │  │ Engine   │  │ Loader   │  │ Management           ││ ║  │
│  ║  │  └──────────┘  └──────────┘  └──────────┘  └──────────────────────┘│ ║  │
│  ║  └─────────────────────────────────────────────────────────────────────┘ ║  │
│  ║                                                                           ║  │
│  ║  ┌─────────────────┬──────────────────┬──────────────────────────────┐   ║  │
│  ║  │   BUILT-IN      │    SKILLS        │      CAPABILITIES            │   ║  │
│  ║  │   TOOLS         │    (Installed)   │      (Configured)            │   ║  │
│  ║  ├─────────────────┼──────────────────┼──────────────────────────────┤   ║  │
│  ║  │ • exec          │ 📧 Gmail         │ 🌐 Browser (Playwright)      │   ║  │
│  ║  │ • bash          │   - send         │ 🧠 Memory (SQLite)           │   ║  │
│  ║  │ • read_file     │   - list         │ 📄 Documents (PDF/OCR)       │   ║  │
│  ║  │ • write_file    │   - read         │ 🔍 Search (Brave API)        │   ║  │
│  ║  │                 │                  │ 📁 Storage (GCS)             │   ║  │
│  ║  │                 │ 📅 Calendar      │                              │   ║  │
│  ║  │                 │   - list         │                              │   ║  │
│  ║  │                 │   - create       │                              │   ║  │
│  ║  │                 │   - delete       │                              │   ║  │
│  ║  └─────────────────┴──────────────────┴──────────────────────────────┘   ║  │
│  ║                                                                           ║  │
│  ╚═══════════════════════════════╦═══════════════════════════════════════════╝  │
│                                  ║                                               │
│          ┌───────────────────────╬───────────────────────┐                      │
│          ▼                       ▼                       ▼                      │
│  ╔═══════════════════╗  ╔═══════════════════╗  ╔═══════════════════╗           │
│  ║   TIER 1: FREE    ║  ║   TIER 2: FREE    ║  ║   TIER 3: PAID    ║           │
│  ║   Antigravity     ║  ║   AI Studio       ║  ║   Vertex AI       ║           │
│  ╠═══════════════════╣  ╠═══════════════════╣  ╠═══════════════════╣           │
│  ║ Claude 3.5 Opus   ║  ║ Gemini 1.5 Pro    ║  ║ Gemini 2.x/2.5    ║           │
│  ║ Gemini 3 Pro      ║  ║ Rate limited      ║  ║ $18K credits      ║           │
│  ║ Claude Sonnet 4.5 ║  ║ Immediate fail-   ║  ║ Safety net for    ║           │
│  ║ 5hr quota reset   ║  ║ over capability   ║  ║ production use    ║           │
│  ╚═══════════════════╝  ╚═══════════════════╝  ╚═══════════════════╝           │
│                                                                                  │
│  ╔═══════════════════════════════════════════════════════════════════════════╗  │
│  ║                           INFRASTRUCTURE                                   ║  │
│  ╠═══════════════════════════════════════════════════════════════════════════╣  │
│  ║                                                                           ║  │
│  ║  ☁️ GCP COMPUTE ENGINE                    📦 STORAGE                      ║  │
│  ║  ├─ Instance: openclaw-desktop           ├─ SQLite: memory.db            ║  │
│  ║  ├─ Type: n2-standard-4                  ├─ GCS: openclaw-files-*        ║  │
│  ║  ├─ Zone: us-central1-a                  └─ Backups: daily to GCS        ║  │
│  ║  ├─ OS: Ubuntu 22.04 LTS                                                 ║  │
│  ║  └─ Disk: 100GB SSD                                                      ║  │
│  ║                                                                           ║  │
│  ║  🔄 RELIABILITY                           🔐 SECURITY                     ║  │
│  ║  ├─ Systemd: auto-start                  ├─ OAuth tokens (Gmail/Cal)     ║  │
│  ║  ├─ Health: 15-min checks                ├─ Service Account (Vertex)     ║  │
│  ║  ├─ Logs: 30-day retention               ├─ SSH keys (GitHub)            ║  │
│  ║  └─ Updates: unattended                  └─ Bot tokens (Telegram)        ║  │
│  ║                                                                           ║  │
│  ╚═══════════════════════════════════════════════════════════════════════════╝  │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Part 4: Where to Add Future Capabilities

### Extension Points Matrix

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         EXTENSION POINTS REFERENCE                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │  WHAT DO YOU WANT TO ADD?                                               │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│         │                                                                        │
│         ├── New AI Provider ──────────────────► AI TIER CONFIGURATION           │
│         │                                       ~/.openclaw/openclaw.json        │
│         │                                       + systemd env vars              │
│         │                                                                        │
│         ├── New External API (Gmail, Slack) ──► SKILL SYSTEM                    │
│         │                                       ~/.openclaw/skills/<name>/       │
│         │                                       ~/.openclaw/scripts/<name>-cli.py│
│         │                                       ~/.openclaw/workspace/TOOLS.md   │
│         │                                                                        │
│         ├── New Communication Channel ────────► GATEWAY INTEGRATION             │
│         │   (Discord, SMS, etc.)               Module in OpenClaw gateway       │
│         │                                       + Bot token configuration        │
│         │                                                                        │
│         ├── New Scheduled Task ───────────────► CRON JOBS                       │
│         │   (Daily report, checks)             crontab -e                       │
│         │                                       ~/.openclaw/scripts/<task>.sh    │
│         │                                                                        │
│         ├── New Storage Backend ──────────────► GCS / CLOUD CONFIG              │
│         │   (S3, Azure, etc.)                  Service account + bucket setup   │
│         │                                                                        │
│         └── New Local Capability ─────────────► SYSTEM PACKAGES                 │
│             (OCR, video, etc.)                 apt install + CLI wrapper        │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Adding a New Skill (Step-by-Step)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    ADDING A NEW SKILL - WORKFLOW                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   STEP 1: Plan                                                                   │
│   ─────────────────────────────────────────────────────────────────────────────  │
│   • Identify the API/service                                                     │
│   • Determine authentication method (OAuth, API key, etc.)                       │
│   • List the operations needed (list, create, delete, etc.)                      │
│                                                                                  │
│   STEP 2: Create CLI Script                                                      │
│   ─────────────────────────────────────────────────────────────────────────────  │
│   Location: ~/.openclaw/scripts/<name>-cli.py                                    │
│                                                                                  │
│   • Accept command-line arguments                                                │
│   • Handle authentication (read from ~/.openclaw/keys/)                          │
│   • Return clear, parseable output                                               │
│   • chmod +x to make executable                                                  │
│                                                                                  │
│   STEP 3: Create SKILL.md                                                        │
│   ─────────────────────────────────────────────────────────────────────────────  │
│   Location: ~/.openclaw/skills/<name>/SKILL.md                                   │
│                                                                                  │
│   • YAML frontmatter with name, description, requirements                        │
│   • Document each command with examples                                          │
│   • Specify required credentials/files                                           │
│                                                                                  │
│   STEP 4: Update TOOLS.md                                                        │
│   ─────────────────────────────────────────────────────────────────────────────  │
│   Location: ~/.openclaw/workspace/TOOLS.md                                       │
│                                                                                  │
│   • Add quick reference section for the skill                                    │
│   • Common commands and examples                                                 │
│                                                                                  │
│   STEP 5: Store Credentials                                                      │
│   ─────────────────────────────────────────────────────────────────────────────  │
│   Location: ~/.openclaw/keys/<service>-token.pickle (or .json)                   │
│                                                                                  │
│   • Run OAuth flow or save API key                                               │
│   • Ensure proper file permissions (600)                                         │
│                                                                                  │
│   STEP 6: Restart & Test                                                         │
│   ─────────────────────────────────────────────────────────────────────────────  │
│   $ systemctl --user restart openclaw-gateway                                    │
│   $ openclaw skills list                                                         │
│   $ openclaw "test the new <skill> skill"                                        │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Part 5: Future Roadmap

### Planned Enhancements

| Priority | Capability | Type | Extension Point |
|----------|------------|------|-----------------|
| **High** | Google Drive | Skill | ~/.openclaw/skills/drive/ |
| **High** | Slack Integration | Skill | ~/.openclaw/skills/slack/ |
| **Medium** | Notion | Skill | ~/.openclaw/skills/notion/ |
| **Medium** | Todoist | Skill | ~/.openclaw/skills/todoist/ |
| **Medium** | Discord Channel | Communication | Gateway module |
| **Low** | Spotify | Skill | ~/.openclaw/skills/spotify/ |
| **Low** | Home Assistant | Skill | ~/.openclaw/skills/homeassistant/ |
| **Low** | Weather API | Skill | ~/.openclaw/skills/weather/ |

### Architecture Evolution Goals

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           FUTURE STATE VISION                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  CURRENT (2026 Q1)                      FUTURE (2026 Q2+)                       │
│  ════════════════════                   ═══════════════════                     │
│                                                                                  │
│  ┌─────────────────────┐                ┌─────────────────────┐                 │
│  │ 2 Skills            │                │ 10+ Skills          │                 │
│  │ (Gmail, Calendar)   │    ────►       │ (Full productivity) │                 │
│  └─────────────────────┘                └─────────────────────┘                 │
│                                                                                  │
│  ┌─────────────────────┐                ┌─────────────────────┐                 │
│  │ 2 Channels          │                │ 4+ Channels         │                 │
│  │ (Telegram, WhatsApp)│    ────►       │ (+Discord, SMS)     │                 │
│  └─────────────────────┘                └─────────────────────┘                 │
│                                                                                  │
│  ┌─────────────────────┐                ┌─────────────────────┐                 │
│  │ Manual Skill Add    │                │ Skill Marketplace   │                 │
│  │ (Copy files)        │    ────►       │ (Install command)   │                 │
│  └─────────────────────┘                └─────────────────────┘                 │
│                                                                                  │
│  ┌─────────────────────┐                ┌─────────────────────┐                 │
│  │ Single Agent        │                │ Multi-Agent         │                 │
│  │ (One gateway)       │    ────►       │ (Specialized roles) │                 │
│  └─────────────────────┘                └─────────────────────┘                 │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Part 6: Quick Reference - File Locations

### Configuration Files

| Purpose | Location |
|---------|----------|
| **Main OpenClaw config** | `~/.openclaw/openclaw.json` |
| **Systemd service** | `~/.config/systemd/user/openclaw-gateway.service` |
| **Environment vars** | `~/.config/systemd/user/openclaw-gateway.service.d/vertex.conf` |
| **Agent personality** | `~/.openclaw/workspace/SOUL.md` |
| **Agent tools reference** | `~/.openclaw/workspace/TOOLS.md` |
| **Agent behavior rules** | `~/.openclaw/workspace/AGENTS.md` |

### Skills & Scripts

| Purpose | Location |
|---------|----------|
| **Skill definitions** | `~/.openclaw/skills/<name>/SKILL.md` |
| **CLI scripts** | `~/.openclaw/scripts/<name>-cli.py` |
| **Scheduled scripts** | `~/.openclaw/scripts/<task>.sh` |

### Credentials & Data

| Purpose | Location |
|---------|----------|
| **OAuth credentials** | `~/.openclaw/keys/oauth-credentials.json` |
| **Gmail token** | `~/.openclaw/keys/gmail-token.pickle` |
| **Calendar token** | `~/.openclaw/keys/calendar-token.pickle` |
| **Vertex AI key** | `~/.openclaw/keys/vertex-auth.json` |
| **Memory database** | `~/.openclaw/data/memory.db` |

### Cron Jobs

| Schedule | Script | Purpose |
|----------|--------|---------|
| `0 8 * * *` | daily-briefing.sh | Morning greeting |
| `*/15 * * * *` | health-check.sh | Gateway health |
| `0 2 * * *` | log-cleanup.sh | Log management |
| `0 3 * * *` | backup-memory.sh | Database backup |
| `0 */6 * * *` | disk-monitor.sh | Disk monitoring |

---

## Navigation

- Previous: [07-skills.md](07-skills.md)
- Next: [09-lead-developer.md](09-lead-developer.md)
- Start: [01-overview.md](01-overview.md)
