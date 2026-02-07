# Current SKILLS Inventory

## Active SKILLS (On VM)

### 1. Gmail ✅
**Status:** Active  
**Location:** `~/.openclaw/skills/gmail/`  
**Script:** `~/.openclaw/scripts/gmail-cli.py`  
**Auth:** OAuth token (`~/.openclaw/keys/gmail-token.pickle`)

**Capabilities:**
- List emails (with filters)
- Read email content
- Send emails
- Search inbox

**Quick Test:**
```bash
python3 ~/.openclaw/scripts/gmail-cli.py list --query "is:unread" --max 5
```

---

### 2. Calendar ✅
**Status:** Active  
**Location:** `~/.openclaw/skills/calendar/`  
**Script:** `~/.openclaw/scripts/calendar-cli.py`  
**Auth:** OAuth token (`~/.openclaw/keys/calendar-token.pickle`)

**Capabilities:**
- List upcoming events
- Create new events
- Delete events
- Search calendar

**Quick Test:**
```bash
python3 ~/.openclaw/scripts/calendar-cli.py list --days 7
```

---

### 3. Google Drive ✅
**Status:** Active  
**Location:** `~/.openclaw/skills/drive/`  
**Script:** `~/.openclaw/scripts/drive-cli.py`  
**Auth:** OAuth token (`~/.openclaw/keys/drive-token.pickle`)

**Capabilities:**
- List files
- Upload files
- Download files
- Share files (with permissions)
- Search Drive
- Create folders
- Delete files (trash)
- Get file info

**Quick Test:**
```bash
python3 ~/.openclaw/scripts/drive-cli.py list --max 3
```

**Use via Telegram/WhatsApp:**
- "List my recent Drive files"
- "Upload this file to Drive"
- "Search Drive for budget report"
- Search calendar

**Quick Test:**
```bash
python3 ~/.openclaw/scripts/calendar-cli.py list --days 7
```

---

### 4. Browser (Built-in) ✅
**Status:** Active  
**Provider:** Playwright  
**Service:** `~/.openclaw/browser/`

**Capabilities:**
- Navigate to URLs
- Take screenshots
- Fill forms
- Extract page content
- Handle JavaScript

**Quick Test:**
```bash
# Via Telegram/WhatsApp
"Take a screenshot of google.com"
```

---

### 5. Web Search (Built-in) ✅
**Status:** Active  
**Provider:** Brave Search API  
**API Key:** In `openclaw.json`

**Capabilities:**
- Web search
- Real-time information
- News lookup

**Quick Test:**
```bash
# Via Telegram/WhatsApp
"Search for OpenAI latest news"
```

---

### 6. Memory (Built-in) ✅
**Status:** Active  
**Storage:** SQLite (`~/.openclaw/data/memory.db`)

**Capabilities:**
- Store facts
- Retrieve information
- Persistent across sessions

**Quick Test:**
```bash
# Via Telegram/WhatsApp
"Remember my favorite food is pizza"
"What's my favorite food?"
```

---

---

## Google Workspace Integration Status

### ✅ Fully Configured
- **Gmail** - Send/read emails
- **Calendar** - Manage events
- **Drive** - File management

### ⚠️ Via Drive (Indirect Access)
- **Google Docs** - Can download as .docx via Drive
- **Google Sheets** - Can download as .xlsx via Drive
- **Google Slides** - Can download as .pptx via Drive

**Note:** Drive CLI can access all Google Workspace files. When downloading Docs/Sheets/Slides, they auto-convert to Office formats.

### ❌ Not Configured (Could Add)
- **Google Forms** - Form creation/responses
- **Google Sites** - Website management
- **Google Meet** - Meeting scheduling (Calendar can create meet links)

---

## SKILLS Not Deployed

### OpenCode (Installed but Not Used)
**Status:** ⚠️ Installed but inactive  
**Reason:** Using OpenClaw SKILLS instead  
**Location:** `~/.npm-global/bin/opencode`

**Why not using:**
- SKILLS system is simpler
- Single-agent architecture preferred
- Less overhead

---

## SKILL Statistics

| SKILL | Status | Auth Method | Last Tested |
|-------|--------|-------------|-------------|
| Gmail | ✅ Active | OAuth | Feb 2026 |
| Calendar | ✅ Active | OAuth | Feb 2026 |
| **Drive** | ✅ Active | OAuth | Feb 2026 |
| Browser | ✅ Active | Built-in | Feb 2026 |
| Web Search | ✅ Active | API Key | Feb 2026 |
| Memory | ✅ Active | Built-in | Feb 2026 |

---

## Verify All SKILLS

### Check SKILLS Directory
```bash
ssh openclaw-desktop
ls -la ~/.openclaw/skills/
```

### Check Scripts
```bash
ls -la ~/.openclaw/scripts/
```

### Test Each SKILL
```bash
# Gmail
python3 ~/.openclaw/scripts/gmail-cli.py list --max 1

# Calendar
python3 ~/.openclaw/scripts/calendar-cli.py list --days 1

# Drive
python3 ~/.openclaw/scripts/drive-cli.py list --max 3

# Browser (via OpenClaw)
# Send: "Take screenshot of example.com"

# Search (via OpenClaw)
# Send: "Search for test"

# Memory (via OpenClaw)
# Send: "Remember test=123"
```

---

## Adding New SKILLS

### Priority List (Potential)
1. **Slack** - Team communication
2. **Google Drive** - File management
3. **GitHub** - Code operations
4. **Notion** - Note taking
5. **Data Analysis** - Pandas/CSV processing

### Steps to Add
1. Create Python CLI script
2. Create SKILL.md definition
3. Test script independently
4. Test via OpenClaw
5. Document in this file

---

## SKILL Maintenance

### Monthly Tasks
- [ ] Test all SKILLS still work
- [ ] Rotate OAuth tokens (90 days)
- [ ] Check for API changes
- [ ] Update documentation

### When Adding New SKILL
- [ ] Create script in `~/.openclaw/scripts/`
- [ ] Create SKILL.md in `~/.openclaw/skills/`
- [ ] Test thoroughly
- [ ] Update this inventory
- [ ] Document in `overview.md`
