# OAuth Setup Guide for Google Workspace

**Simple step-by-step guide to enable Sheets, Docs, and Slides**

---

## Prerequisites

✅ You already have `oauth-credentials.json` (used for Gmail/Calendar)  
✅ Python 3 installed on your local machine  
✅ `gcloud` CLI configured

---

## Step 1: Install Python Library (Local Machine)

```bash
pip3 install google-auth-oauthlib google-api-python-client
```

---

## Step 2: Run OAuth Setup Script

```bash
cd /Users/folin/projects/digital-employee-infra/skills/google-workspace-scripts

# Make sure oauth-credentials.json is here
# (Copy from ~/.openclaw/keys/ if needed)

# Run setup
python3 setup-oauth.py
```

**What happens:**
1. Script opens browser
2. You log in to Google
3. Grant permissions for Sheets, Docs, Slides
4. Script saves 3 token files

---

## Step 3: Upload Tokens to VM

```bash
# Still in google-workspace-scripts/ directory
gcloud compute scp *-token.pickle openclaw-desktop:~/.openclaw/keys/ \
  --zone=us-central1-a \
  --project=linkhealth-care-2024 \
  --tunnel-through-iap
```

---

## Step 4: Upload Scripts to VM

```bash
# Upload CLI scripts
gcloud compute scp sheets-cli.py docs-cli.py slides-cli.py \
  openclaw-desktop:~/.openclaw/scripts/ \
  --zone=us-central1-a \
  --project=linkhealth-care-2024 \
  --tunnel-through-iap
```

---

## Step 5: Make Scripts Executable

```bash
ssh openclaw-desktop

chmod +x ~/.openclaw/scripts/sheets-cli.py
chmod +x ~/.openclaw/scripts/docs-cli.py
chmod +x ~/.openclaw/scripts/slides-cli.py
```

---

## Step 6: Create SKILL Definitions

```bash
# Still on VM

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
```bash
python3 ~/.openclaw/scripts/sheets-cli.py create "Spreadsheet Name"
```

### Read Data
```bash
python3 ~/.openclaw/scripts/sheets-cli.py read SPREADSHEET_ID
```

### Write Data
```bash
python3 ~/.openclaw/scripts/sheets-cli.py write SPREADSHEET_ID A1:B2 "Name;Email,John;john@example.com"
```
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
```bash
python3 ~/.openclaw/scripts/docs-cli.py create "Document Title"
```

### Read Document
```bash
python3 ~/.openclaw/scripts/docs-cli.py read DOCUMENT_ID
```

### Append Text
```bash
python3 ~/.openclaw/scripts/docs-cli.py append DOCUMENT_ID "Text to add"
```
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
```bash
python3 ~/.openclaw/scripts/slides-cli.py create "Presentation Title"
```

### Read Presentation
```bash
python3 ~/.openclaw/scripts/slides-cli.py read PRESENTATION_ID
```
EOF
```

---

## Step 7: Test Each Service

```bash
# Test Sheets
python3 ~/.openclaw/scripts/sheets-cli.py create "Test Spreadsheet"

# Test Docs
python3 ~/.openclaw/scripts/docs-cli.py create "Test Document"

# Test Slides
python3 ~/.openclaw/scripts/slides-cli.py create "Test Presentation"
```

**Each should return:**
- Created: [Name]
- ID: [ID]
- URL: [Google Drive URL]

---

## Step 8: Restart OpenClaw

```bash
systemctl --user restart openclaw-gateway
systemctl --user status openclaw-gateway
```

---

## Step 9: Test via Telegram/WhatsApp

```
"Create a spreadsheet called Q1 Sales"
"Create a document called Meeting Notes"
"Create a presentation called Team Update"
```

---

## Troubleshooting

### Browser doesn't open
```bash
# Make sure you're on LOCAL machine, not VM
# VM doesn't have browser access
```

### oauth-credentials.json not found
```bash
# Download from VM
gcloud compute scp openclaw-desktop:~/.openclaw/keys/oauth-credentials.json ./ \
  --zone=us-central1-a --tunnel-through-iap
```

### Token errors on VM
```bash
# Check tokens exist
ls -la ~/.openclaw/keys/*-token.pickle

# Check permissions
chmod 600 ~/.openclaw/keys/*-token.pickle
```

### Script not found
```bash
# Check scripts uploaded
ls -la ~/.openclaw/scripts/{sheets,docs,slides}-cli.py

# Make executable
chmod +x ~/.openclaw/scripts/{sheets,docs,slides}-cli.py
```

---

## Quick Reference

### All Commands in One Go

```bash
# LOCAL MACHINE
cd /Users/folin/projects/digital-employee-infra/skills/google-workspace-scripts
python3 setup-oauth.py
gcloud compute scp *-token.pickle openclaw-desktop:~/.openclaw/keys/ --zone=us-central1-a --tunnel-through-iap
gcloud compute scp {sheets,docs,slides}-cli.py openclaw-desktop:~/.openclaw/scripts/ --zone=us-central1-a --tunnel-through-iap

# VM
ssh openclaw-desktop
chmod +x ~/.openclaw/scripts/{sheets,docs,slides}-cli.py
# (Create SKILL.md files - see Step 6)
systemctl --user restart openclaw-gateway
```

---

## Success Checklist

- [ ] OAuth tokens generated (3 files)
- [ ] Tokens uploaded to VM
- [ ] Scripts uploaded to VM
- [ ] Scripts executable
- [ ] SKILL definitions created
- [ ] Gateway restarted
- [ ] Sheets test passed
- [ ] Docs test passed
- [ ] Slides test passed
- [ ] Telegram/WhatsApp test passed

---

**Time estimate:** 10-15 minutes total
