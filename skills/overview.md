# SKILLS System

## What are SKILLS?

SKILLS are the core automation technology in OpenClaw. Each SKILL is a Python script that extends the agent's capabilities.

**Think of SKILLS as:** Tools the AI can call to perform specific tasks.

---

## How SKILLS Work

```
User Request
    ↓
OpenClaw identifies which SKILL to use
    ↓
Calls Python script with parameters
    ↓
Script executes (Gmail, Calendar, etc.)
    ↓
Returns result to user
```

---

## SKILL Structure

Each SKILL has:
1. **Python CLI script** - Does the actual work
2. **SKILL.md** - Tells OpenClaw how to use it
3. **Location** - `~/.openclaw/skills/<name>/`

### Example: Gmail SKILL

```
~/.openclaw/skills/gmail/
├── SKILL.md              # Instructions for OpenClaw
└── (uses system script)  # ~/.openclaw/scripts/gmail-cli.py
```

---

## Currently Available SKILLS

### 1. Gmail
**What it does:** Send and read emails

**Commands:**
```bash
# List unread emails
python3 ~/.openclaw/scripts/gmail-cli.py list --query "is:unread"

# Read specific email
python3 ~/.openclaw/scripts/gmail-cli.py read <message_id>

# Send email
python3 ~/.openclaw/scripts/gmail-cli.py send \
  --to "recipient@example.com" \
  --subject "Subject" \
  --body "Message"
```

**Use via Telegram/WhatsApp:**
- "Check my unread emails"
- "Send email to john@example.com about meeting"

---

### 2. Calendar
**What it does:** View and create calendar events

**Commands:**
```bash
# List upcoming events
python3 ~/.openclaw/scripts/calendar-cli.py list --days 7

# Create event
python3 ~/.openclaw/scripts/calendar-cli.py create \
  --title "Meeting" \
  --start "2026-02-10T10:00:00" \
  --end "2026-02-10T11:00:00"

# Delete event
python3 ~/.openclaw/scripts/calendar-cli.py delete <event_id>
```

**Use via Telegram/WhatsApp:**
- "What's on my calendar this week?"
- "Schedule meeting tomorrow at 2pm"

---

### 3. Browser (Built-in)
**What it does:** Automate web browsing with Playwright

**Capabilities:**
- Navigate to URLs
- Take screenshots
- Fill forms
- Extract data

**Use via Telegram/WhatsApp:**
- "Take a screenshot of example.com"
- "Check the price on amazon.com"

---

### 4. Web Search (Built-in)
**What it does:** Search the web via Brave API

**Use via Telegram/WhatsApp:**
- "Search for latest AI news"
- "What's the weather in San Francisco?"

---

### 5. Memory (Built-in)
**What it does:** Remember facts across conversations

**Storage:** SQLite database at `~/.openclaw/data/memory.db`

**Use via Telegram/WhatsApp:**
- "Remember my favorite color is blue"
- "What's my favorite color?"

---

## Creating a New SKILL

### 1. Create Python Script
```bash
# Location
~/.openclaw/scripts/<skill-name>-cli.py

# Make executable
chmod +x ~/.openclaw/scripts/<skill-name>-cli.py
```

### 2. Create SKILL.md
```bash
# Location
~/.openclaw/skills/<skill-name>/SKILL.md
```

### 3. SKILL.md Template
```markdown
---
name: skill-name
description: "What this skill does"
metadata:
  {
    "openclaw": {
      "emoji": "🔧",
      "requires": { "bins": ["python3"] }
    }
  }
---

# Skill Name

## Commands

### Do Something
\`\`\`bash
python3 ~/.openclaw/scripts/<skill>-cli.py action --param value
\`\`\`
```

### 4. Test
```bash
# Test script directly
python3 ~/.openclaw/scripts/<skill>-cli.py --help

# Test via OpenClaw
# Send message via Telegram/WhatsApp
```

---

## SKILL Best Practices

✅ **Keep scripts simple** - One script per skill  
✅ **Use argparse** - Clear command-line interface  
✅ **Return JSON** - Structured output for OpenClaw  
✅ **Handle errors** - Graceful failure messages  
✅ **Document commands** - Clear SKILL.md instructions  

---

## SKILL Locations

### On VM
```
~/.openclaw/skills/          # SKILL definitions
~/.openclaw/scripts/         # Python CLI scripts
~/.openclaw/keys/            # API credentials
```

### Authentication
- **Gmail/Calendar:** OAuth tokens in `~/.openclaw/keys/`
- **Other APIs:** Keys in `~/.openclaw/openclaw.json` or environment variables

---

## Troubleshooting

### SKILL Not Found
```bash
# List available skills
ls ~/.openclaw/skills/

# Check SKILL.md exists
cat ~/.openclaw/skills/<name>/SKILL.md
```

### Script Fails
```bash
# Test script directly
python3 ~/.openclaw/scripts/<name>-cli.py --help

# Check permissions
ls -l ~/.openclaw/scripts/<name>-cli.py

# View OpenClaw logs
journalctl --user -u openclaw-gateway -f
```

### Authentication Issues
```bash
# Gmail/Calendar: Check tokens exist
ls ~/.openclaw/keys/*.pickle

# Regenerate if needed (from local machine)
python3 auth_helper.py
```

---

## Examples of Potential SKILLS

### Already Implemented
- ✅ Gmail
- ✅ Calendar
- ✅ Browser
- ✅ Web Search
- ✅ Memory

### Could Add
- 📧 Slack integration
- 📁 Google Drive operations
- 📊 Data analysis (pandas)
- 🔄 GitHub operations
- 📝 Notion integration
- 💬 WhatsApp automation
- 📸 Image processing

---

## Why SKILLS Matter

**SKILLS are the automation engine:**
- Extend OpenClaw without modifying core code
- Reusable across different agents
- Easy to test and debug independently
- Clear separation of concerns

**This is why we chose OpenClaw SKILLS over OpenCode delegation** - simpler, more direct, easier to maintain.
