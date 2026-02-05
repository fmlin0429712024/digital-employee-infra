# 05 - Extended Capabilities

Complete reference for all extended capabilities with code examples.

---

## Table of Contents

1. [Browser Automation](#browser-automation)
2. [Persistent Memory](#persistent-memory)
3. [Document Processing](#document-processing)
4. [Email Gateway](#email-gateway)
5. [Calendar Integration](#calendar-integration)
6. [File Storage](#file-storage)
7. [Scheduled Tasks](#scheduled-tasks)

---

## Browser Automation

**Technology**: Playwright + Chromium

### Use Cases

- Web research and data extraction
- Taking screenshots of pages
- Filling and submitting forms
- Monitoring website changes
- Generating PDFs from web pages

### Quick Example

```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Navigate
  await page.goto('https://example.com');

  // Take screenshot
  await page.screenshot({ path: 'screenshot.png' });

  // Extract text
  const title = await page.title();
  console.log('Title:', title);

  // Fill form
  await page.fill('#search', 'query');
  await page.click('#submit');

  // Generate PDF
  await page.pdf({ path: 'page.pdf' });

  await browser.close();
})();
```

### Environment Setup

```bash
export NODE_PATH="$HOME/.npm-global/lib/node_modules"
```

---

## Persistent Memory

**Technology**: SQLite

**Database Location**: `~/.openclaw/data/memory.db`

### Schema

```sql
-- Conversation history
conversations (id, channel, user_id, message_id, role, content, timestamp)

-- User preferences
preferences (id, user_id, data, updated_at)

-- Long-term facts
memory (id, category, key, value, source, created_at)

-- Task history
tasks (id, description, status, result, created_at, completed_at)
```

### Usage Examples

```python
import sqlite3

DB_PATH = "~/.openclaw/data/memory.db"

def remember_fact(category, key, value, source=None):
    conn = sqlite3.connect(os.path.expanduser(DB_PATH))
    conn.execute(
        "INSERT INTO memory (category, key, value, source) VALUES (?, ?, ?, ?)",
        (category, key, value, source)
    )
    conn.commit()
    conn.close()

def recall_facts(category):
    conn = sqlite3.connect(os.path.expanduser(DB_PATH))
    cursor = conn.execute(
        "SELECT key, value FROM memory WHERE category = ?", (category,)
    )
    facts = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    return facts

def log_conversation(channel, role, content, user_id=None):
    conn = sqlite3.connect(os.path.expanduser(DB_PATH))
    conn.execute(
        "INSERT INTO conversations (channel, user_id, role, content) VALUES (?, ?, ?, ?)",
        (channel, user_id, role, content)
    )
    conn.commit()
    conn.close()
```

---

## Document Processing

### PDF Extraction

```python
import pdfplumber

def extract_pdf_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_pdf_tables(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            tables.extend(page_tables)
    return tables
```

### OCR (Image to Text)

```python
import pytesseract
from PIL import Image

def ocr_image(image_path, lang='eng'):
    """Extract text from image. lang options: 'eng', 'chi_sim', etc."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang=lang)
    return text
```

### Spreadsheet Processing

```python
import pandas as pd

def read_excel(file_path, sheet_name=0):
    return pd.read_excel(file_path, sheet_name=sheet_name)

def read_csv(file_path):
    return pd.read_csv(file_path)

def write_excel(df, file_path):
    df.to_excel(file_path, index=False)
```

### CLI Tools

```bash
# PDF to text
pdftotext input.pdf output.txt

# PDF to images
pdftoppm input.pdf output -png

# OCR an image
tesseract image.png output -l eng
```

---

## Email Gateway

**Technology**: Gmail API

**Credentials**: `~/.openclaw/keys/oauth-credentials.json`
**Token**: `~/.openclaw/keys/gmail-token.pickle`

### Helper Script

Location: `~/.openclaw/scripts/gmail_helper.py`

```python
#!/usr/bin/env python3
import os
import pickle
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build

TOKEN_PATH = os.path.expanduser("~/.openclaw/keys/gmail-token.pickle")

def get_gmail_service():
    with open(TOKEN_PATH, "rb") as f:
        creds = pickle.load(f)
    return build("gmail", "v1", credentials=creds)

def list_messages(max_results=10, query="is:unread"):
    service = get_gmail_service()
    results = service.users().messages().list(
        userId="me", maxResults=max_results, q=query
    ).execute()
    return results.get("messages", [])

def get_message(msg_id):
    service = get_gmail_service()
    msg = service.users().messages().get(userId="me", id=msg_id, format="full").execute()
    headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}

    body = ""
    if "parts" in msg["payload"]:
        for part in msg["payload"]["parts"]:
            if part["mimeType"] == "text/plain":
                body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                break

    return {
        "id": msg_id,
        "from": headers.get("From", ""),
        "subject": headers.get("Subject", ""),
        "body": body
    }

def send_email(to, subject, body):
    service = get_gmail_service()
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
```

### Usage

```python
from gmail_helper import list_messages, get_message, send_email

# List unread emails
messages = list_messages(query="is:unread")

# Read an email
email = get_message(messages[0]["id"])
print(f"From: {email['from']}")
print(f"Subject: {email['subject']}")

# Send an email
send_email("recipient@example.com", "Hello", "This is the body")
```

---

## Calendar Integration

**Technology**: Google Calendar API

**Token**: `~/.openclaw/keys/calendar-token.pickle`

### Helper Script

Location: `~/.openclaw/scripts/calendar_helper.py`

```python
#!/usr/bin/env python3
import os
import pickle
from datetime import datetime, timedelta
from googleapiclient.discovery import build

TOKEN_PATH = os.path.expanduser("~/.openclaw/keys/calendar-token.pickle")

def get_calendar_service():
    with open(TOKEN_PATH, "rb") as f:
        creds = pickle.load(f)
    return build("calendar", "v3", credentials=creds)

def list_upcoming_events(max_results=10, days_ahead=7):
    service = get_calendar_service()
    now = datetime.utcnow().isoformat() + "Z"
    end = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + "Z"

    results = service.events().list(
        calendarId="primary",
        timeMin=now,
        timeMax=end,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    return [
        {
            "id": e["id"],
            "summary": e.get("summary", "No title"),
            "start": e["start"].get("dateTime", e["start"].get("date")),
            "end": e["end"].get("dateTime", e["end"].get("date")),
        }
        for e in results.get("items", [])
    ]

def create_event(summary, start_time, end_time, description=""):
    service = get_calendar_service()
    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_time, "timeZone": "America/Los_Angeles"},
        "end": {"dateTime": end_time, "timeZone": "America/Los_Angeles"},
    }
    return service.events().insert(calendarId="primary", body=event).execute()
```

### Usage

```python
from calendar_helper import list_upcoming_events, create_event

# List upcoming events
events = list_upcoming_events(days_ahead=7)
for e in events:
    print(f"{e['start']}: {e['summary']}")

# Create an event
create_event(
    summary="Team Meeting",
    start_time="2026-02-10T10:00:00",
    end_time="2026-02-10T11:00:00",
    description="Weekly sync"
)
```

---

## File Storage

**Technology**: Google Cloud Storage

**Bucket**: `openclaw-files-linkhealth`

### Helper Script

Location: `~/.openclaw/scripts/storage_helper.py`

```python
#!/usr/bin/env python3
import os
from google.cloud import storage

DEFAULT_BUCKET = "openclaw-files-linkhealth"

def get_client():
    return storage.Client()

def upload_file(local_path, remote_path=None, bucket_name=None):
    bucket_name = bucket_name or DEFAULT_BUCKET
    remote_path = remote_path or os.path.basename(local_path)

    client = get_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(remote_path)
    blob.upload_from_filename(local_path)

    return f"gs://{bucket_name}/{remote_path}"

def download_file(remote_path, local_path=None, bucket_name=None):
    bucket_name = bucket_name or DEFAULT_BUCKET
    local_path = local_path or os.path.basename(remote_path)

    client = get_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(remote_path)
    blob.download_to_filename(local_path)

    return local_path

def list_files(prefix="", bucket_name=None):
    bucket_name = bucket_name or DEFAULT_BUCKET
    client = get_client()
    bucket = client.bucket(bucket_name)
    return [blob.name for blob in bucket.list_blobs(prefix=prefix)]

def upload_string(content, remote_path, bucket_name=None):
    bucket_name = bucket_name or DEFAULT_BUCKET
    client = get_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(remote_path)
    blob.upload_from_string(content)
    return f"gs://{bucket_name}/{remote_path}"
```

### Usage

```python
from storage_helper import upload_file, download_file, list_files

# Upload a file
url = upload_file("/path/to/local/file.pdf", "documents/file.pdf")
print(f"Uploaded: {url}")

# Download a file
download_file("documents/file.pdf", "/tmp/downloaded.pdf")

# List files
files = list_files(prefix="documents/")
for f in files:
    print(f)
```

### CLI Usage

```bash
# Upload
gsutil cp local_file.txt gs://openclaw-files-linkhealth/path/

# Download
gsutil cp gs://openclaw-files-linkhealth/path/file.txt ./

# List
gsutil ls gs://openclaw-files-linkhealth/
```

---

## Scheduled Tasks

**Technology**: Cron

### Current Schedule

| Schedule | Task | Description |
|----------|------|-------------|
| `0 8 * * *` | daily-briefing.sh | Morning greeting at 8 AM |
| `*/15 * * * *` | health-check.sh | Gateway health check every 15 min |
| `0 2 * * *` | log-cleanup.sh | Compress old logs, delete after 30 days |
| `0 3 * * *` | backup-memory.sh | Backup SQLite to GCS |
| `0 */6 * * *` | disk-monitor.sh | Check disk usage, alert if >80% |

### Managing Cron Jobs

```bash
# View current jobs
crontab -l

# Edit jobs
crontab -e

# View logs
tail -f /tmp/openclaw/cron.log
```

### Cron Syntax Reference

```
* * * * * command
│ │ │ │ │
│ │ │ │ └─ Day of week (0-7, Sun=0 or 7)
│ │ │ └─── Month (1-12)
│ │ └───── Day of month (1-31)
│ └─────── Hour (0-23)
└───────── Minute (0-59)
```

### Common Schedules

```bash
# Every hour
0 * * * *

# Every day at midnight
0 0 * * *

# Every Monday at 9 AM
0 9 * * 1

# Every 30 minutes
*/30 * * * *
```

---

## Reliability & Maintenance

Automated systems to keep the Digital Employee running smoothly.

### Log Management

**Script**: `~/.openclaw/scripts/log-cleanup.sh`

- Compresses logs older than 1 day
- Deletes compressed logs older than 30 days
- Runs daily at 2 AM

### Database Backup

**Script**: `~/.openclaw/scripts/backup-memory.sh`

- Backs up SQLite memory database to GCS
- Location: `gs://openclaw-files-linkhealth/backups/memory/`
- Retention: 30 days
- Runs daily at 3 AM

**Restore from backup:**
```bash
gsutil cp gs://openclaw-files-linkhealth/backups/memory/memory-YYYY-MM-DD.db ~/.openclaw/data/memory.db
```

### Disk Monitoring

**Script**: `~/.openclaw/scripts/disk-monitor.sh`

- Checks disk usage every 6 hours
- Alerts if usage exceeds 80%
- Logs to `/tmp/openclaw/cron.log`

### Security Updates

**Technology**: Unattended Upgrades

- Automatically installs security patches
- Runs daily
- Config: `/etc/apt/apt.conf.d/20auto-upgrades`

---

## Environment Variables

Required in `~/.bashrc`:

```bash
export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:$PATH"
export NODE_PATH="$HOME/.npm-global/lib/node_modules"
```

For OpenClaw Gateway (in systemd service):

```ini
GOOGLE_APPLICATION_CREDENTIALS=/path/to/vertex-auth.json
GOOGLE_CLOUD_PROJECT=project-id
GOOGLE_CLOUD_LOCATION=us-central1
TELEGRAM_BOT_TOKEN=token
```

---

## Navigation

- Previous: [04-communication.md](04-communication.md)
- Next: [06-quick-reference.md](06-quick-reference.md)
