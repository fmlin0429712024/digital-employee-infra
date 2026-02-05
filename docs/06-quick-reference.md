# 06 - Quick Reference

One-page reference for common commands, paths, and status.

---

## Capability Status

### Foundation

| Capability | Technology | Status |
|------------|------------|--------|
| 24/7 Cloud Host | GCP n2-standard-4 | ✅ |
| AI Orchestration | OpenClaw Gateway | ✅ |
| Multi-model Fallback | Antigravity → Vertex AI | ✅ |
| Telegram Messaging | "Pet" | ✅ |
| WhatsApp Messaging | "Mirror" | ✅ |
| Voice STT | Whisper (local) | ✅ |
| Voice TTS | edge-tts | ✅ |
| Web Search | Brave API | ✅ |
| Version Control | GitHub SSH | ✅ |

### Extended Capabilities

| Capability | Technology | Status |
|------------|------------|--------|
| Browser Automation | Playwright + Chromium | ✅ |
| Persistent Memory | SQLite | ✅ |
| Document Processing | Poppler, Tesseract, pandas | ✅ |
| Email Gateway | Gmail API | ✅ |
| Calendar Integration | Google Calendar API | ✅ |
| File Storage | GCS Bucket | ✅ |
| Scheduled Tasks | Cron | ✅ |

---

## Common Commands

### Connect to VM

```bash
gcloud compute ssh --zone "us-central1-a" "openclaw-desktop" --project "linkhealth-care-2024"
```

### Gateway Management

```bash
openclaw gateway status       # Check health
openclaw gateway restart      # Restart
systemctl --user status openclaw-gateway
systemctl --user restart openclaw-gateway
```

### Model Management

```bash
openclaw models status
openclaw models set google-vertex/gemini-2.5-pro
openclaw models set google-antigravity/gemini-3-pro-low
```

### View Logs

```bash
# Gateway logs
tail -f /tmp/openclaw/openclaw-*.log

# Cron logs
tail -f /tmp/openclaw/cron.log
```

### Cron Jobs

```bash
crontab -l    # List jobs
crontab -e    # Edit jobs
```

---

## Key Paths

### Cloud Resources

| Resource | Location |
|----------|----------|
| GCP Console | https://console.cloud.google.com/ |
| GCP Project | `linkhealth-care-2024` |
| VM Instance | `openclaw-desktop` (us-central1-a) |
| GCS Bucket | `gs://openclaw-files-linkhealth` |

### VM Paths

| Resource | Path |
|----------|------|
| OpenClaw Config | `~/.openclaw/openclaw.json` |
| Memory Database | `~/.openclaw/data/memory.db` |
| OAuth Credentials | `~/.openclaw/keys/oauth-credentials.json` |
| Gmail Token | `~/.openclaw/keys/gmail-token.pickle` |
| Calendar Token | `~/.openclaw/keys/calendar-token.pickle` |
| Vertex Auth (backup) | `~/.openclaw/keys/vertex-auth.json` |
| Helper Scripts | `~/.openclaw/scripts/` |
| Logs | `/tmp/openclaw/` |

### Vertex AI Authentication

| Component | Value |
|-----------|-------|
| **Auth Method** | VM Default Service Account (recommended) |
| **Service Account** | `51058313466-compute@developer.gserviceaccount.com` |
| **IAM Role** | `roles/aiplatform.user` |
| **Project** | `linkhealth-care-2024` |
| **Region** | `us-central1` |

---

## Scheduled Tasks

| Schedule | Script | Description |
|----------|--------|-------------|
| `0 8 * * *` | daily-briefing.sh | Morning greeting (8 AM) |
| `*/15 * * * *` | health-check.sh | Gateway health check |

---

## API Quick Reference

### Gmail

```python
from gmail_helper import list_messages, get_message, send_email

messages = list_messages(query="is:unread")
email = get_message(messages[0]["id"])
send_email("to@example.com", "Subject", "Body")
```

### Calendar

```python
from calendar_helper import list_upcoming_events, create_event

events = list_upcoming_events(days_ahead=7)
create_event("Meeting", "2026-02-10T10:00:00", "2026-02-10T11:00:00")
```

### Storage

```python
from storage_helper import upload_file, download_file, list_files

upload_file("/local/file.pdf", "remote/file.pdf")
download_file("remote/file.pdf", "/local/file.pdf")
files = list_files(prefix="documents/")
```

### Playwright

```javascript
const { chromium } = require('playwright');
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('https://example.com');
await page.screenshot({ path: 'screenshot.png' });
await browser.close();
```

### SQLite Memory

```python
import sqlite3
conn = sqlite3.connect(os.path.expanduser("~/.openclaw/data/memory.db"))
conn.execute("INSERT INTO memory (category, key, value) VALUES (?, ?, ?)",
             ("fact", "user_name", "Forest"))
conn.commit()
```

---

## Troubleshooting

### Gateway Won't Start

```bash
# Check status
systemctl --user status openclaw-gateway

# Check logs
journalctl --user -u openclaw-gateway -f

# Verify environment
cat ~/.config/systemd/user/openclaw-gateway.service.d/vertex.conf
```

### OAuth Token Expired

```bash
# Re-run auth from local machine
python3 auth_helper.py

# Copy new token to VM
gcloud compute scp oauth-token.pickle openclaw-desktop:~/.openclaw/keys/gmail-token.pickle --zone=us-central1-a
```

### Storage Permission Denied

```bash
# Check VM scopes
gcloud compute instances describe openclaw-desktop --zone=us-central1-a --format="get(serviceAccounts[0].scopes)"

# Should include: https://www.googleapis.com/auth/cloud-platform
```

---

## Documentation Index

| # | Document | Topic |
|---|----------|-------|
| 01 | [01-overview.md](01-overview.md) | What is a Digital Employee |
| 02 | [02-infrastructure.md](02-infrastructure.md) | GCP VM & environment setup |
| 03 | [03-ai-providers.md](03-ai-providers.md) | Model fallback strategy |
| 04 | [04-communication.md](04-communication.md) | Messaging & voice |
| 05 | [05-capabilities.md](05-capabilities.md) | Extended capabilities |
| 06 | [06-quick-reference.md](06-quick-reference.md) | This document |

---

## Navigation

- Previous: [05-capabilities.md](05-capabilities.md)
- Start: [01-overview.md](01-overview.md)
