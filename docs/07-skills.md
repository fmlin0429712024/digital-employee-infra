# 07 - Skills Development

How to create, configure, and manage custom skills for the Digital Employee.

---

## What Are Skills?

Skills are **instructions that teach the agent how to perform specific tasks**. They bridge the gap between the agent's built-in tools (bash, exec, etc.) and external capabilities (Gmail, Calendar, APIs).

```
┌─────────────────────────────────────────────────────────────────┐
│                      SKILL ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │    User      │────▶│    Agent     │────▶│   Skill      │    │
│  │   Request    │     │   (OpenClaw) │     │  (SKILL.md)  │    │
│  │              │     │              │     │              │    │
│  │ "Send email" │     │ Reads skill  │     │ Instructions │    │
│  │              │     │ instructions │     │ + CLI cmds   │    │
│  └──────────────┘     └──────────────┘     └──────────────┘    │
│                              │                                   │
│                              ▼                                   │
│                    ┌──────────────────┐                         │
│                    │  exec/bash       │                         │
│                    │  Runs CLI script │                         │
│                    │  gmail-cli.py    │                         │
│                    └──────────────────┘                         │
│                              │                                   │
│                              ▼                                   │
│                    ┌──────────────────┐                         │
│                    │  External API    │                         │
│                    │  (Gmail, etc.)   │                         │
│                    └──────────────────┘                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Skill Components

A complete skill consists of:

| Component | Location | Purpose |
|-----------|----------|---------|
| **SKILL.md** | `~/.openclaw/skills/<name>/SKILL.md` | Instructions for the agent |
| **CLI Script** | `~/.openclaw/scripts/<name>-cli.py` | Executable that does the work |
| **TOOLS.md Entry** | `~/.openclaw/workspace/TOOLS.md` | Quick reference for agent |
| **OAuth/Credentials** | `~/.openclaw/keys/` | Authentication tokens |

---

## Creating a New Skill

### Step 1: Create the CLI Script

The CLI script is what the agent will execute. It should:
- Accept command-line arguments
- Return clear output
- Handle errors gracefully

**Template:**

```python
#!/usr/bin/env python3
"""<Skill Name> CLI for OpenClaw agent.

Usage:
  <name>-cli.py <command> [options]
"""

import argparse

def main():
    parser = argparse.ArgumentParser(description="<Skill> CLI for OpenClaw")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Add subcommands
    list_parser = subparsers.add_parser("list", help="List items")
    list_parser.add_argument("--max", type=int, default=10)

    args = parser.parse_args()

    if args.command == "list":
        # Do something
        print("Results here")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

**Save to:** `~/.openclaw/scripts/<name>-cli.py`

**Make executable:**
```bash
chmod +x ~/.openclaw/scripts/<name>-cli.py
```

### Step 2: Create SKILL.md

The SKILL.md file teaches the agent how to use your CLI script.

**Location:** `~/.openclaw/skills/<name>/SKILL.md`

**Structure:**

```markdown
---
name: <skill-name>
description: "One-line description of what this skill does"
metadata:
  {
    "openclaw":
      {
        "emoji": "📧",
        "requires": { "files": ["~/.openclaw/keys/<token-file>"] }
      }
  }
---

# <Skill Name> Skill

Description of the skill and what it can do.

## Prerequisites

- List required tokens/credentials
- List required APIs

## Commands

### Command 1

Description of the command.

\`\`\`bash
python3 ~/.openclaw/scripts/<name>-cli.py command1 --option value
\`\`\`

### Command 2

\`\`\`bash
python3 ~/.openclaw/scripts/<name>-cli.py command2 arg1 arg2
\`\`\`

## Examples

Practical examples the agent can follow.
```

### Step 3: Update TOOLS.md

Add a quick reference to `~/.openclaw/workspace/TOOLS.md`:

```markdown
## <Skill Name>

You have access to <skill> via the <name>-cli.py script.

**Common commands:**
\`\`\`bash
python3 ~/.openclaw/scripts/<name>-cli.py list
python3 ~/.openclaw/scripts/<name>-cli.py create "arg1" "arg2"
\`\`\`
```

### Step 4: Restart Gateway

```bash
systemctl --user restart openclaw-gateway
```

### Step 5: Verify Skill

```bash
openclaw skills list | grep <skill-name>
```

Should show: `✓ ready │ 📧 <skill-name>`

---

## Current Skills

### 📧 Gmail Skill

**Purpose:** Send and read emails via Gmail API

**CLI Script:** `~/.openclaw/scripts/gmail-cli.py`

**Commands:**

| Command | Description |
|---------|-------------|
| `list` | List emails (--query, --max) |
| `read <id>` | Read a specific email |
| `send <to> <subject> <body>` | Send an email |

**Example:**
```bash
python3 ~/.openclaw/scripts/gmail-cli.py send "user@example.com" "Subject" "Body"
```

**Prerequisites:**
- Gmail API enabled in GCP
- OAuth token at `~/.openclaw/keys/gmail-token.pickle`

---

### 📅 Google Calendar Skill

**Purpose:** Create and manage calendar events

**CLI Script:** `~/.openclaw/scripts/calendar-cli.py`

**Commands:**

| Command | Description |
|---------|-------------|
| `list` | List upcoming events (--days, --max) |
| `create <title> <start> <end>` | Create event (--attendees, --description) |
| `delete <id>` | Delete an event |

**Example:**
```bash
python3 ~/.openclaw/scripts/calendar-cli.py create "Meeting" "2026-02-05T18:00:00" "2026-02-05T19:00:00" --attendees "email@example.com"
```

**Time Format:** `YYYY-MM-DDTHH:MM:SS` (America/Chicago timezone)

**Prerequisites:**
- Calendar API enabled in GCP
- OAuth token at `~/.openclaw/keys/calendar-token.pickle`

---

## Skill Requirements

The `requires` field in SKILL.md metadata specifies what the skill needs:

```yaml
"requires": {
  "bins": ["command"],           # Required CLI binaries
  "anyBins": ["cmd1", "cmd2"],   # At least one of these
  "files": ["~/.path/to/file"]   # Required files exist
}
```

**Examples:**

```yaml
# Requires specific binary
"requires": { "bins": ["gh"] }

# Requires any one of these
"requires": { "anyBins": ["claude", "codex", "opencode"] }

# Requires credential file
"requires": { "files": ["~/.openclaw/keys/gmail-token.pickle"] }
```

---

## Troubleshooting

### Skill shows "missing"

Check requirements:
```bash
openclaw skills info <skill-name>
```

Common causes:
- Required file doesn't exist
- Required binary not installed
- SKILL.md syntax error

### Agent doesn't use the skill

1. Check TOOLS.md has the skill documented
2. Restart gateway: `systemctl --user restart openclaw-gateway`
3. Start a new conversation (agent reads TOOLS.md at session start)

### CLI script errors

Test the script directly:
```bash
python3 ~/.openclaw/scripts/<name>-cli.py --help
python3 ~/.openclaw/scripts/<name>-cli.py list
```

### Permission denied

Make script executable:
```bash
chmod +x ~/.openclaw/scripts/<name>-cli.py
```

---

## File Locations Summary

| File | Path |
|------|------|
| **Skill definitions** | `~/.openclaw/skills/<name>/SKILL.md` |
| **CLI scripts** | `~/.openclaw/scripts/<name>-cli.py` |
| **Agent tools reference** | `~/.openclaw/workspace/TOOLS.md` |
| **Agent personality** | `~/.openclaw/workspace/SOUL.md` |
| **Agent behavior** | `~/.openclaw/workspace/AGENTS.md` |
| **OAuth credentials** | `~/.openclaw/keys/` |

---

## Future Skill Ideas

| Skill | Purpose | API/Service |
|-------|---------|-------------|
| Google Drive | File storage, sharing | Drive API |
| Slack | Team messaging | Slack API |
| Notion | Notes and databases | Notion API |
| Todoist | Task management | Todoist API |
| Spotify | Music control | Spotify API |
| Home Assistant | Smart home control | HA API |
| Weather | Weather forecasts | OpenWeather API |

---

## Navigation

- Previous: [06-quick-reference.md](06-quick-reference.md)
- Start: [01-overview.md](01-overview.md)
