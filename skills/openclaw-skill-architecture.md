# OpenClaw Skill Architecture

Understanding how skills work in OpenClaw - the key to extending your Digital Employee's capabilities.

---

## Quick Summary

| Component | Location | Purpose |
|-----------|----------|---------|
| **TOOLS.md** | `~/.openclaw/workspace/TOOLS.md` | Agent's cheat sheet - quick reference for all tools |
| **SKILL.md** | `~/.openclaw/skills/<name>/SKILL.md` | Detailed instructions for one specific skill |
| **CLI Script** | `~/.openclaw/scripts/<name>-cli.py` | The actual executable that does the work |
| **Token/Credentials** | `~/.openclaw/keys/` | Authentication for APIs |

---

## The Two-Layer System

### Layer 1: TOOLS.md (The Cheat Sheet)

**Location:** `~/.openclaw/workspace/TOOLS.md`

**Purpose:** Quick reference that the agent reads at the START of every session.

**What goes here:**
- Brief overview of each available tool
- Common command examples
- Important notes (like "don't use markdown in slides")

**Example entry:**
```markdown
## Gmail

You have access to Gmail via the gmail-cli.py script.

**List emails:**
python3 ~/.openclaw/scripts/gmail-cli.py list --query "is:unread" --max 5

**Send email:**
python3 ~/.openclaw/scripts/gmail-cli.py send "to@email.com" "Subject" "Body"
```

**Key insight:** TOOLS.md is loaded into the agent's context at session start. Keep it concise - every byte costs tokens.

---

### Layer 2: SKILL.md (The Manual)

**Location:** `~/.openclaw/skills/<skill-name>/SKILL.md`

**Purpose:** Detailed documentation that OpenClaw can reference when needed.

**What goes here:**
- Full command documentation
- All options and flags
- Examples for complex use cases
- Prerequisites and requirements

**Structure:**
```markdown
---
name: gmail
description: "Send and read emails via Gmail API"
metadata:
  {
    "openclaw":
      {
        "emoji": "📧",
        "requires": { "files": ["~/.openclaw/keys/gmail-token.pickle"] }
      }
  }
---

# Gmail Skill

Detailed documentation here...

## Commands

### list
List emails with optional filtering...

### send
Send an email...
```

**Key insight:** SKILL.md files are NOT loaded at session start. OpenClaw loads them on-demand when it detects it needs that skill.

---

## How They Work Together

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER REQUEST                                 │
│                  "Send an email to Bob"                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     TOOLS.md (Always Loaded)                     │
│                                                                  │
│  Agent sees: "Gmail - use gmail-cli.py to send emails"          │
│  Agent knows: This task needs the Gmail skill                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              SKILL.md (Loaded On-Demand)                         │
│                                                                  │
│  Agent reads: ~/.openclaw/skills/gmail/SKILL.md                 │
│  Agent learns: Full command syntax, all options                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CLI SCRIPT (Executed)                         │
│                                                                  │
│  python3 ~/.openclaw/scripts/gmail-cli.py send ...              │
└─────────────────────────────────────────────────────────────────┘
```

---

## The requires Field

The `requires` field in SKILL.md metadata tells OpenClaw what dependencies a skill needs:

```yaml
"requires": {
  "bins": ["command"],           # Required CLI binaries
  "anyBins": ["cmd1", "cmd2"],   # At least one of these
  "files": ["~/.path/to/file"]   # Required files must exist
}
```

**Examples:**

```yaml
# Gmail requires token file
"requires": { "files": ["~/.openclaw/keys/gmail-token.pickle"] }

# GitHub CLI requires gh binary
"requires": { "bins": ["gh"] }

# Coding skill needs any one of these
"requires": { "anyBins": ["claude", "opencode", "aider"] }
```

**What happens if requirements aren't met:**
- Skill shows as "missing" in `openclaw skills list`
- Agent won't try to use it
- User sees what's missing via `openclaw skills info <name>`

---

## Best Practices

### TOOLS.md Best Practices

1. **Keep it short** - Agent reads this every session (token cost)
2. **Include examples** - Show actual commands, not just descriptions
3. **Add warnings** - Like "don't use markdown in slides"
4. **Update after changes** - Restart gateway to pick up changes

### SKILL.md Best Practices

1. **Be comprehensive** - This is the full manual
2. **Use frontmatter** - The YAML header with name, description, requires
3. **Include prerequisites** - What APIs need enabling, what tokens needed
4. **Show all options** - Document every flag and argument

### CLI Script Best Practices

1. **Use argparse** - Standard Python argument parsing
2. **Return clear output** - Agent reads stdout to know what happened
3. **Handle errors gracefully** - Print helpful error messages
4. **Make executable** - `chmod +x script.py`

---

## Directory Structure

```
~/.openclaw/
├── workspace/
│   ├── TOOLS.md          # Quick reference (always loaded)
│   ├── SOUL.md           # Agent personality
│   ├── AGENTS.md         # Agent behavior rules
│   └── MEMORY.md         # Long-term memory
│
├── skills/
│   ├── gmail/
│   │   └── SKILL.md      # Gmail skill documentation
│   ├── gcalendar/
│   │   └── SKILL.md      # Calendar skill documentation
│   └── drive/
│       └── SKILL.md      # Drive skill documentation
│
├── scripts/
│   ├── gmail-cli.py      # Gmail CLI executable
│   ├── calendar-cli.py   # Calendar CLI executable
│   ├── drive-cli.py      # Drive CLI executable
│   ├── sheets-cli.py     # Sheets CLI executable
│   ├── docs-cli.py       # Docs CLI executable
│   └── slides-cli.py     # Slides CLI executable
│
└── keys/
    ├── gmail-token.pickle
    ├── calendar-token.pickle
    ├── drive-token.pickle
    ├── sheets-token.pickle
    ├── docs-token.pickle
    └── slides-token.pickle
```

---

## Adding a New Skill (Checklist)

1. [ ] Create CLI script: `~/.openclaw/scripts/<name>-cli.py`
2. [ ] Make executable: `chmod +x ~/.openclaw/scripts/<name>-cli.py`
3. [ ] Test script directly: `python3 ~/.openclaw/scripts/<name>-cli.py --help`
4. [ ] Create skill folder: `mkdir ~/.openclaw/skills/<name>/`
5. [ ] Create SKILL.md: `~/.openclaw/skills/<name>/SKILL.md`
6. [ ] Add to TOOLS.md: Quick reference entry
7. [ ] Restart gateway: `systemctl --user restart openclaw-gateway`
8. [ ] Verify: `openclaw skills list`
9. [ ] Test via chat: Ask agent to use the skill

---

## Common Issues

### Skill shows "missing"
```bash
openclaw skills info <skill-name>
```
Check what requirement is not met.

### Agent doesn't use the skill
1. Is it in TOOLS.md? (Agent needs to know it exists)
2. Restart gateway after changes
3. Start new session (`/reset`)

### Agent uses wrong syntax
1. Check TOOLS.md examples match actual CLI
2. Test CLI manually first: `python3 script.py --help`
3. Update TOOLS.md with correct syntax

### Script errors
```bash
python3 ~/.openclaw/scripts/<name>-cli.py --help
python3 ~/.openclaw/scripts/<name>-cli.py <command>
```
Test outside of OpenClaw first.

---

## Key Takeaways for Presentation

1. **TOOLS.md = Cheat Sheet** - Loaded every session, keep it concise
2. **SKILL.md = Full Manual** - Loaded on-demand, be comprehensive
3. **CLI Scripts = The Workers** - Actual executables that do the work
4. **requires = Dependencies** - Tells OpenClaw what's needed
5. **Restart gateway after changes** - `systemctl --user restart openclaw-gateway`
6. **Test scripts directly first** - Before expecting the agent to use them

---

## Current Skills on openclaw-desktop

| Skill | CLI Script | Token | Status |
|-------|------------|-------|--------|
| Gmail | gmail-cli.py | gmail-token.pickle | ✅ Active |
| Calendar | calendar-cli.py | calendar-token.pickle | ✅ Active |
| Drive | drive-cli.py | drive-token.pickle | ✅ Active |
| Sheets | sheets-cli.py | sheets-token.pickle | ✅ Active |
| Docs | docs-cli.py | docs-token.pickle | ✅ Active |
| Slides | slides-cli.py | slides-token.pickle | ✅ Active |

---

## References

- [07-skills.md](../docs/07-skills.md) - Original skills documentation
- [current-skills.md](current-skills.md) - Current skill inventory
