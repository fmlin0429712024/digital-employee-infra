# Credentials Reference

## Quick Lookup

| Service | Auth Method | Location |
|---------|-------------|----------|
| **Vertex AI** | VM Service Account | Automatic (IAM role) |
| **Antigravity** | OAuth | `~/.openclaw/openclaw.json` |
| **Telegram** | Bot Token | `~/.openclaw/.env` |
| **WhatsApp** | Bot Token | `~/.openclaw/.env` |
| **Gmail** | OAuth Token | `~/.openclaw/keys/gmail-token.pickle` |
| **Calendar** | OAuth Token | `~/.openclaw/keys/calendar-token.pickle` |
| **Brave Search** | API Key | `~/.openclaw/openclaw.json` |

---

## Vertex AI (GCP)

### Service Account
```
51058313466-compute@developer.gserviceaccount.com
```

### IAM Role
```
roles/aiplatform.user
```

### Verify Access
```bash
gcloud projects get-iam-policy linkhealth-care-2024 \
  --flatten="bindings[].members" \
  --filter="bindings.members:51058313466-compute@developer.gserviceaccount.com"
```

---

## Telegram

### Bot Token Location
```
~/.openclaw/.env
TELEGRAM_BOT_TOKEN=<token>
```

### Get New Token
1. Message @BotFather
2. `/newbot` or `/mybots` → API Token

---

## Gmail & Calendar

### OAuth Tokens
```
~/.openclaw/keys/gmail-token.pickle
~/.openclaw/keys/calendar-token.pickle
```

### Regenerate
```bash
# From local machine
python3 auth_helper.py

# Upload to VM
gcloud compute scp *.pickle openclaw-desktop:~/.openclaw/keys/ \
  --zone=us-central1-a --tunnel-through-iap
```

---

## Brave Search

### API Key Location
```
~/.openclaw/openclaw.json
{
  "tools": {
    "web": {
      "search": {
        "apiKey": "BSA..."
      }
    }
  }
}
```

### Get New Key
https://brave.com/search/api/

---

## Backup Command

```bash
# Download all credentials
gcloud compute scp --recurse \
  openclaw-desktop:~/.openclaw/keys/ \
  ./backup-$(date +%Y%m%d)/ \
  --zone=us-central1-a --tunnel-through-iap
```
