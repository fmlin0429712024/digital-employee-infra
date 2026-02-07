# Architecture Overview

## Current System (Feb 2026)

```
┌─────────────────────────────────────────────────────┐
│              COMMAND CENTER                          │
│                                                      │
│  📱 Telegram    📱 WhatsApp    🎤 Voice             │
│    "Pet"         "Mirror"      FFmpeg               │
│                                                      │
│                     ▼                                │
│  ┌──────────────────────────────────────────────┐   │
│  │        🦞 OPENCLAW GATEWAY                    │   │
│  │         (n2-standard-4 VM)                    │   │
│  └──────────────────────────────────────────────┘   │
│                     ▼                                │
│  ┌─────────────┐  ┌─────────────┐  ┌───────────┐   │
│  │ Antigravity │→ │  Vertex AI  │→ │  Skills   │   │
│  │   (FREE)    │  │   (PAID)    │  │  System   │   │
│  └─────────────┘  └─────────────┘  └───────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## Infrastructure

| Component | Specification |
|-----------|---------------|
| **VM** | openclaw-desktop (n2-standard-4) |
| **CPU** | 4 vCPU |
| **RAM** | 16GB |
| **Disk** | 100GB SSD |
| **Region** | us-central1-a |
| **OS** | Ubuntu 22.04 LTS |
| **Project** | linkhealth-care-2024 |

---

## AI Model Strategy

### Primary: Vertex AI (Optimized)
```
google-vertex/gemini-2.0-flash  ($0.10/1M input)
```

### Fallback Chain
1. `google-antigravity/gemini-3-flash` (FREE)
2. `google-vertex/gemini-2.5-flash` ($0.15/1M)
3. `google-antigravity/gemini-3-pro-high` (FREE)
4. `google-vertex/gemini-1.5-pro` ($1.25/1M)

**Strategy:** Use cheapest first, escalate only if needed.

---

## Communication Channels

| Channel | Purpose | Status |
|---------|---------|--------|
| **Telegram** | Quick commands | ✅ Active |
| **WhatsApp** | Deep conversations | ✅ Active |
| **Voice** | STT/TTS via FFmpeg | ✅ Active |

---

## Core Capabilities

### Built-in
- ✅ Browser automation (Playwright)
- ✅ Persistent memory (SQLite)
- ✅ Document processing (PDF/OCR)
- ✅ Web search (Brave API)
- ✅ File storage (GCS)

### Skills (Custom)
- ✅ Gmail integration
- ✅ Google Calendar
- ✅ Scheduled tasks (cron)

---

## What's NOT Deployed

| Component | Status | Reason |
|-----------|--------|--------|
| GPU VM | ❌ Not deployed | Tested, not cost-effective |
| Ollama (for heartbeats) | ⚠️ Installed but not used | OpenClaw doesn't support config |
| OpenCode | ⚠️ Installed but not used | Using OpenClaw SKILLS instead |
| Local LLM inference | ❌ Not deployed | Using Vertex AI |

---

## Authentication

### Vertex AI
- **Method:** VM Service Account
- **SA:** `51058313466-compute@developer.gserviceaccount.com`
- **Role:** `roles/aiplatform.user`

### Antigravity
- **Method:** OAuth
- **Email:** `fmlin429@gmail.com`

### Messaging
- **Telegram:** Bot token in `~/.openclaw/.env`
- **WhatsApp:** Bot token in `~/.openclaw/.env`

---

## Key Design Decisions

### 1. Single Agent (OpenClaw)
**Why:** Simpler than dual-agent (OpenClaw + OpenCode)
- SKILLS system handles coding tasks
- Less complexity, easier maintenance

### 2. Vertex AI Primary
**Why:** Reliable, scalable, $18K credits available
- Antigravity as free tier
- Automatic fallback on quota exhaustion

### 3. Standard VM (No GPU)
**Why:** Cost-effective for current workload
- Vertex AI handles inference
- No need for local GPU acceleration

### 4. SKILLS Over Delegation
**Why:** More direct, less overhead
- Skills = Python scripts called by OpenClaw
- No need for separate agent coordination

---

## Network & Security

### Firewall
- ✅ SSH via IAP tunnel only (no direct internet SSH)
- ✅ HTTPS/HTTP allowed (for web access if needed)
- ✅ Internal GCP traffic allowed

### Access Control
- ✅ Service account for Vertex AI (no user keys)
- ✅ OAuth tokens for Gmail/Calendar
- ✅ Bot tokens for messaging (environment variables)

---

## Monitoring

### Gateway Health
```bash
systemctl --user status openclaw-gateway
openclaw gateway status
```

### Logs
```bash
journalctl --user -u openclaw-gateway -f
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log
```

### Costs
```
GCP Console → Billing → Reports → Filter: Vertex AI
```

---

## Future Considerations

### Potential Additions
- Context caching (when OpenClaw adds support)
- Rate limiting (application-level)
- Ollama integration (when config supported)
- GPU VM (if PHI/PII requirements emerge)

### Not Planned
- Multiple VMs (single VM sufficient)
- Kubernetes (overkill for current scale)
- Multiple regions (us-central1 adequate)
