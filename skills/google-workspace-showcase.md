# Google Workspace Showcase

**Complete Google Workspace automation with OpenClaw SKILLS**

---

## Overview

Full integration with Google Workspace services for enterprise automation:

| Service | Status | Capabilities |
|---------|--------|--------------|
| **Gmail** | ✅ Active | Send/read emails, search inbox |
| **Calendar** | ✅ Active | Create/view events, manage schedule |
| **Drive** | ✅ Active | Upload/download/share files, search |
| **Sheets** | 🔄 Ready to deploy | Create/read/write spreadsheets |
| **Docs** | 🔄 Ready to deploy | Create/read/edit documents |
| **Slides** | 🔄 Ready to deploy | Create/read presentations |

---

## Deployment Steps

### 1. Upload Scripts to VM

```bash
# From local machine
cd /Users/folin/projects/digital-employee-infra/skills/google-workspace-scripts

# Upload Sheets
gcloud compute scp sheets-cli.py openclaw-desktop:~/.openclaw/scripts/ \
  --zone=us-central1-a --project=linkhealth-care-2024 --tunnel-through-iap

# Upload Docs
gcloud compute scp docs-cli.py openclaw-desktop:~/.openclaw/scripts/ \
  --zone=us-central1-a --project=linkhealth-care-2024 --tunnel-through-iap

# Upload Slides
gcloud compute scp slides-cli.py openclaw-desktop:~/.openclaw/scripts/ \
  --zone=us-central1-a --project=linkhealth-care-2024 --tunnel-through-iap
```

### 2. Make Scripts Executable

```bash
ssh openclaw-desktop
chmod +x ~/.openclaw/scripts/sheets-cli.py
chmod +x ~/.openclaw/scripts/docs-cli.py
chmod +x ~/.openclaw/scripts/slides-cli.py
```

### 3. Generate OAuth Tokens

**From local machine with browser access:**

```python
# Create oauth_setup.py
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/presentations'
]

flow = InstalledAppFlow.from_client_secrets_file(
    'oauth-credentials.json', SCOPES)
creds = flow.run_local_server(port=0)

# Save tokens
with open('sheets-token.pickle', 'wb') as f:
    pickle.dump(creds, f)
with open('docs-token.pickle', 'wb') as f:
    pickle.dump(creds, f)
with open('slides-token.pickle', 'wb') as f:
    pickle.dump(creds, f)

print("Tokens generated!")
```

```bash
# Run OAuth flow
python3 oauth_setup.py

# Upload tokens to VM
gcloud compute scp *-token.pickle openclaw-desktop:~/.openclaw/keys/ \
  --zone=us-central1-a --project=linkhealth-care-2024 --tunnel-through-iap
```

### 4. Create SKILL Definitions

**On VM:**

```bash
# Sheets SKILL
mkdir -p ~/.openclaw/skills/sheets
cat > ~/.openclaw/skills/sheets/SKILL.md << 'EOF'
---
name: sheets
description: "Create and manage Google Sheets spreadsheets"
metadata:
  {
    "openclaw": {
      "emoji": "📊",
      "requires": { "files": ["~/.openclaw/keys/sheets-token.pickle"] }
    }
  }
---

# Google Sheets Skill

## Commands

### Create Spreadsheet
\`\`\`bash
python3 ~/.openclaw/scripts/sheets-cli.py create "Spreadsheet Name"
\`\`\`

### Read Data
\`\`\`bash
python3 ~/.openclaw/scripts/sheets-cli.py read SPREADSHEET_ID
python3 ~/.openclaw/scripts/sheets-cli.py read SPREADSHEET_ID --range A1:B10
\`\`\`

### Write Data
\`\`\`bash
python3 ~/.openclaw/scripts/sheets-cli.py write SPREADSHEET_ID A1:B2 "Name;Email,John;john@example.com"
\`\`\`

### Append Data
\`\`\`bash
python3 ~/.openclaw/scripts/sheets-cli.py append SPREADSHEET_ID A:B "New;Row"
\`\`\`
EOF

# Docs SKILL
mkdir -p ~/.openclaw/skills/docs
cat > ~/.openclaw/skills/docs/SKILL.md << 'EOF'
---
name: docs
description: "Create and edit Google Docs documents"
metadata:
  {
    "openclaw": {
      "emoji": "📝",
      "requires": { "files": ["~/.openclaw/keys/docs-token.pickle"] }
    }
  }
---

# Google Docs Skill

## Commands

### Create Document
\`\`\`bash
python3 ~/.openclaw/scripts/docs-cli.py create "Document Title"
\`\`\`

### Read Document
\`\`\`bash
python3 ~/.openclaw/scripts/docs-cli.py read DOCUMENT_ID
\`\`\`

### Append Text
\`\`\`bash
python3 ~/.openclaw/scripts/docs-cli.py append DOCUMENT_ID "Text to add"
\`\`\`
EOF

# Slides SKILL
mkdir -p ~/.openclaw/skills/slides
cat > ~/.openclaw/skills/slides/SKILL.md << 'EOF'
---
name: slides
description: "Create and manage Google Slides presentations"
metadata:
  {
    "openclaw": {
      "emoji": "📊",
      "requires": { "files": ["~/.openclaw/keys/slides-token.pickle"] }
    }
  }
---

# Google Slides Skill

## Commands

### Create Presentation
\`\`\`bash
python3 ~/.openclaw/scripts/slides-cli.py create "Presentation Title"
\`\`\`

### Read Presentation
\`\`\`bash
python3 ~/.openclaw/scripts/slides-cli.py read PRESENTATION_ID
\`\`\`

### Add Slide
\`\`\`bash
python3 ~/.openclaw/scripts/slides-cli.py add-slide PRESENTATION_ID "Slide Title"
\`\`\`
EOF
```

### 5. Restart OpenClaw

```bash
systemctl --user restart openclaw-gateway
systemctl --user status openclaw-gateway
```

---

## Showcase Demo Script

### Demo 1: Automated Report Generation

```
User: "Create a new spreadsheet called Q1 Sales Report"
→ Creates spreadsheet
→ Returns ID and URL

User: "Add headers: Date, Product, Revenue"
→ Writes to A1:C1

User: "Add data: 2026-01-15, Widget, 1500"
→ Appends row

User: "Create a document summarizing the sales data"
→ Creates Google Doc
→ Adds summary text
```

### Demo 2: Meeting Preparation

```
User: "Create presentation called Team Sync Q1"
→ Creates Google Slides

User: "Add slide with title: Q1 Achievements"
→ Adds slide to presentation

User: "Schedule meeting for tomorrow 2pm"
→ Creates Calendar event with Meet link
```

### Demo 3: Document Workflow

```
User: "Create document called Project Proposal"
→ Creates Google Doc

User: "Add introduction paragraph"
→ Appends text to doc

User: "Share with team@company.com"
→ Uses Drive to share
```

---

## Use Cases

### Business Automation
- Generate weekly reports in Sheets
- Create meeting agendas in Docs
- Build presentation decks in Slides
- Auto-schedule follow-ups in Calendar

### Data Management
- Import CSV to Sheets
- Export reports to Docs
- Share files via Drive
- Track tasks in Sheets

### Collaboration
- Create shared documents
- Schedule team meetings
- Share presentations
- Manage project files

---

## Testing Commands

```bash
# Test Sheets
python3 ~/.openclaw/scripts/sheets-cli.py create "Test Sheet"

# Test Docs
python3 ~/.openclaw/scripts/docs-cli.py create "Test Doc"

# Test Slides
python3 ~/.openclaw/scripts/slides-cli.py create "Test Presentation"
```

---

## Showcase Talking Points

✅ **Complete Google Workspace Integration**
- All major services automated
- Single interface via OpenClaw
- Natural language commands

✅ **Enterprise-Ready**
- OAuth security
- Audit trail via logs
- Scalable architecture

✅ **Practical Use Cases**
- Report generation
- Meeting prep
- Document workflows
- Data management

✅ **Cost-Optimized**
- Free Google Workspace APIs
- Optimized AI model usage (33% savings)
- No additional infrastructure costs
