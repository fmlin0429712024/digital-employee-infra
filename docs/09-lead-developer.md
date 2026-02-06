# 09 - Lead Developer Agent (OpenCode)

This document covers the installation, configuration, and integration of OpenCode as a "Lead Developer" agent that works alongside OpenClaw (the "Manager").

---

## The Dual-Agent Architecture

### Why Two Agents?

| Role | Agent | Specialization |
|------|-------|----------------|
| **Manager** | OpenClaw | Communication, scheduling, task delegation, general assistance |
| **Lead Developer** | OpenCode | Code writing, refactoring, bug fixes, technical implementation |

This separation provides:
- **Specialized tooling** - OpenCode has IDE-like features optimized for coding
- **Cost efficiency** - Use cheaper models for communication, powerful models for code
- **Clear responsibility** - Manager handles "what to do", Lead Developer handles "how to do it"
- **Independent scaling** - Can upgrade/change either agent without affecting the other

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    MANAGER + LEAD DEVELOPER ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   📱 Telegram / WhatsApp / Voice                                                │
│         │                                                                        │
│         │  User: "Add user authentication to my-webapp"                         │
│         ▼                                                                        │
│   ┌─────────────────────────────────────────────────────────────────┐           │
│   │                     🦞 OPENCLAW (Manager)                        │           │
│   │                                                                  │           │
│   │  • Receives and interprets request                              │           │
│   │  • Reads "code" skill instructions                              │           │
│   │  • Delegates to Lead Developer                                  │           │
│   │  • Reports results back to user                                 │           │
│   │                                                                  │           │
│   │  AI: Antigravity (FREE) → AI Studio → Vertex AI                │           │
│   └─────────────────────────────────────────────────────────────────┘           │
│         │                                                                        │
│         │  Delegation via code-cli.py                                           │
│         ▼                                                                        │
│   ┌─────────────────────────────────────────────────────────────────┐           │
│   │                  💻 OPENCODE (Lead Developer)                    │           │
│   │                                                                  │           │
│   │  • Analyzes codebase                                            │           │
│   │  • Plans implementation                                          │           │
│   │  • Writes/modifies code                                          │           │
│   │  • Returns structured results                                    │           │
│   │                                                                  │           │
│   │  AI: Google AI Studio (API Key - Free tier)                     │           │
│   └─────────────────────────────────────────────────────────────────┘           │
│         │                                                                        │
│         ▼                                                                        │
│   📁 ~/projects/<repo>  (Code changes written to disk)                          │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## What is OpenCode?

**OpenCode** is an open-source AI coding agent (MIT licensed) that provides Claude Code-like capabilities with multi-provider support.

| Feature | Description |
|---------|-------------|
| **Open Source** | MIT licensed, 95k+ GitHub stars |
| **Multi-Provider** | Supports Claude, Gemini, GPT, local models |
| **Privacy-First** | Code stays local, no external storage |
| **Terminal UI** | Interactive TUI with Vim-like editor |
| **Non-Interactive Mode** | `opencode run -p "prompt"` for automation |
| **File Operations** | Read, write, edit files in codebase |
| **Bash Execution** | Run commands and scripts |

### OpenCode vs Claude Code

| Aspect | OpenCode | Claude Code |
|--------|----------|-------------|
| **License** | MIT (Free) | Proprietary (Paid) |
| **AI Providers** | 75+ providers | Anthropic only |
| **Cost** | Pay provider rates | Anthropic API rates |
| **Customization** | Full config control | Limited |
| **Our Choice** | Gemini via AI Studio API | N/A |

---

## Installation

### Prerequisites

- Node.js v18+ (VM has v22)
- Google AI Studio API key (free tier available at aistudio.google.com)

### Install OpenCode

```bash
# SSH to VM (via IAP tunnel - see 02-infrastructure.md for details)
gcloud compute ssh openclaw-desktop --zone=us-central1-a --project=linkhealth-care-2024 --tunnel-through-iap

# Install via npm
npm i -g opencode-ai@latest

# Verify installation
opencode --version
```

---

## Configuration

### OpenCode Config File

**Location:** `~/.config/opencode/opencode.json`

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "google/gemini-2.5-flash"
}
```

### Environment Variables

**Add to `~/.bashrc`:**

```bash
# Gemini API Key for OpenCode (from Google AI Studio)
export GOOGLE_GENERATIVE_AI_API_KEY="your-api-key-here"
```

**Get your API key:**
1. Go to https://aistudio.google.com/apikey
2. Click "Create API key"
3. Copy and add to ~/.bashrc

### Model Selection

| Model | Use Case | Cost per 1M tokens |
|-------|----------|-------------------|
| **google/gemini-2.5-flash** | Default - fast, efficient | $0.15 in / $0.60 out |
| **google/gemini-2.5-pro** | Complex tasks (--complex flag) | $1.25 in / $10.00 out |
| **google/gemini-2.0-flash** | Fallback - cheapest | $0.10 in / $0.40 out |

---

## Integration with OpenClaw

### The "code" Skill

OpenClaw delegates coding tasks via the "code" skill:

**Skill Definition:** `~/.openclaw/skills/code/SKILL.md`

```markdown
---
name: code
description: "Delegate coding tasks to OpenCode Lead Developer agent"
metadata:
  {
    "openclaw":
      {
        "emoji": "💻",
        "requires": { "bins": ["opencode"] }
      }
  }
---

# Code Skill (Lead Developer)

Delegate coding tasks to the Lead Developer agent (OpenCode).

## Commands

### Run a Coding Task
```bash
python3 ~/.openclaw/scripts/code-cli.py run --project /path/to/project --task "Task description"
```

### Complex Task (uses gemini-2.5-pro)
```bash
python3 ~/.openclaw/scripts/code-cli.py run --project /path/to/project --task "Complex task" --complex
```

### List Projects
```bash
python3 ~/.openclaw/scripts/code-cli.py list
```

### Check Status
```bash
python3 ~/.openclaw/scripts/code-cli.py status
```
```

### CLI Wrapper Script

**Location:** `~/.openclaw/scripts/code-cli.py`

The wrapper script:
1. Validates the project path
2. Selects the appropriate model
3. Invokes OpenCode in non-interactive mode
4. Captures and returns structured output

```python
#!/usr/bin/env python3
"""OpenCode Lead Developer CLI for OpenClaw agent."""

import argparse
import subprocess
import json
import os
import sys
from pathlib import Path

PROJECTS_DIR = os.path.expanduser("~/projects")

def run_task(project_path, task, complex_mode=False):
    """Execute a coding task using OpenCode."""
    project = Path(project_path).expanduser().resolve()

    if not project.exists():
        print(f"ERROR: Project path does not exist: {project}")
        sys.exit(1)

    model = "google/gemini-2.5-pro" if complex_mode else "google/gemini-2.5-flash"

    cmd = ["opencode", "run", task, "-m", model, "--format", "json"]

    print(f"=== Lead Developer Task ===")
    print(f"Project: {project}")
    print(f"Task: {task}")
    print(f"Model: {model}")

    result = subprocess.run(cmd, cwd=str(project), capture_output=True, text=True, timeout=600)

    if result.returncode == 0:
        print("=== Task Completed ===")
        print(result.stdout)
    else:
        print(f"=== Task Failed ===")
        print(result.stderr)
        sys.exit(1)

# ... (list_projects, check_status, main functions)
```

---

## Usage Examples

### Via Telegram/WhatsApp

**User:** "Create a REST API endpoint for user registration in my-webapp"

**OpenClaw (Manager):**
1. Identifies this as a coding task
2. Reads the "code" skill
3. Executes: `python3 code-cli.py run --project ~/projects/my-webapp --task "Create REST API endpoint for user registration"`

**OpenCode (Lead Developer):**
1. Analyzes the codebase
2. Identifies existing patterns
3. Creates the endpoint code
4. Returns summary of changes

**OpenClaw (Manager):**
"Done! I created the user registration endpoint. Files modified:
- `src/routes/auth.py` - Added `/register` endpoint
- `src/models/user.py` - Added User model
- `tests/test_auth.py` - Added registration tests"

### Direct OpenCode Usage

For interactive coding sessions, SSH to VM and run OpenCode directly:

```bash
cd ~/projects/my-webapp
opencode
```

This opens the TUI for hands-on coding with AI assistance.

---

## Projects Workspace

All coding projects live in `~/projects/`:

```
~/projects/
├── my-webapp/           # Main web application
├── api-service/         # Backend API
├── data-pipeline/       # Data processing
└── scripts/             # Utility scripts
```

### Adding a New Project

```bash
cd ~/projects
git clone https://github.com/user/repo.git project-name
```

### Listing Projects

```bash
python3 ~/.openclaw/scripts/code-cli.py list
```

---

## Credentials & Authentication

### API Key Authentication

OpenCode uses a Google AI Studio API key (separate from OpenClaw's Antigravity OAuth):

| Item | Details |
|------|---------|
| **API Key Source** | Google AI Studio (aistudio.google.com) |
| **Environment Variable** | `GOOGLE_GENERATIVE_AI_API_KEY` |
| **Storage** | `~/.bashrc` and `code-cli.py` |
| **Free Tier** | 60 requests/minute, 1M tokens/day |

### Cost Tracking

Google AI Studio provides generous free tier. For higher usage:
- Monitor at https://aistudio.google.com/apikey (usage stats)
- Upgrade to pay-as-you-go if needed

---

## Troubleshooting

### OpenCode Not Found

```bash
# Check if installed
which opencode

# Reinstall if needed
npm i -g opencode-ai@latest
```

### API Key Not Working

```bash
# Check environment variable is set
echo $GOOGLE_GENERATIVE_AI_API_KEY

# Verify models are available
opencode models google

# Test directly
opencode run "Say hello" -m google/gemini-2.5-flash
```

### Task Timeout

The default timeout is 10 minutes. For large tasks, increase in code-cli.py:

```python
result = subprocess.run(cmd, ..., timeout=1200)  # 20 minutes
```

### Model Not Available

Refresh the models cache:

```bash
opencode models --refresh
opencode models google
```

---

## File Locations Summary

| File | Purpose |
|------|---------|
| `~/.npm-global/bin/opencode` | OpenCode binary |
| `~/.config/opencode/opencode.json` | OpenCode global config |
| `~/.openclaw/skills/code/SKILL.md` | Skill definition for OpenClaw |
| `~/.openclaw/scripts/code-cli.py` | CLI wrapper script |
| `~/.bashrc` | Contains `GOOGLE_GENERATIVE_AI_API_KEY` |
| `~/projects/` | Coding workspace root |

---

## Future Enhancements

| Enhancement | Description |
|-------------|-------------|
| **Git Integration** | Auto-commit changes after successful tasks |
| **PR Creation** | Automatically create pull requests |
| **Code Review** | Dedicated review workflow |
| **Cost Alerts** | Notify when usage exceeds threshold |
| **Session Persistence** | Continue multi-turn coding sessions |

---

## Navigation

- Previous: [08-architecture-journey.md](08-architecture-journey.md)
- Next: [10-agent-framework-vision.md](10-agent-framework-vision.md)
- Start: [01-overview.md](01-overview.md)
