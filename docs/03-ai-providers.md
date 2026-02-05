# 03 - AI Providers

## Overview

The Digital Employee uses a **multi-tier fallback strategy** to ensure 24/7 availability while minimizing costs.

---

## Fallback Strategy

```
┌─────────────────────────────────────────────────────────────┐
│  Priority 1: Antigravity (FREE)                             │
│  └─ gemini-3-pro-low → gemini-3-flash → gemini-3-pro-high  │
│                                                             │
│  ↓ If quota exhausted (5hr reset)                          │
│                                                             │
│  Priority 2: Vertex AI (PAID - Cheapest First)             │
│  └─ gemini-2.0-flash → gemini-2.5-flash → gemini-1.5-pro   │
│                                                             │
│  Cost: $0.10-$1.25 per 1M input tokens                     │
│  Budget: $18,000 GCP credits                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Tier 1: Antigravity (Primary)

| Attribute | Value |
|-----------|-------|
| **Auth** | OAuth |
| **Cost** | FREE |
| **Models** | Claude 3.5 Opus, Gemini 3 Pro, Claude Sonnet 4.5 |
| **Quota** | Resets every 5 hours |
| **Best For** | Day-to-day usage |

**Pros**: Free, access to Claude and Gemini
**Cons**: Quota limits, occasional downtime

---

## Tier 2: Google AI Studio (Backup)

| Attribute | Value |
|-----------|-------|
| **Auth** | API Key |
| **Cost** | FREE (with limits) |
| **Models** | Gemini 1.5 Pro |
| **Use Case** | Immediate failover when Antigravity exhausted |

**Pros**: Free, reliable Google infrastructure
**Cons**: Rate limits, Gemini only

---

## Tier 3: Vertex AI (Safety Net)

| Attribute | Value |
|-----------|-------|
| **Auth** | Service Account |
| **Cost** | Pay-per-use ($18K credits) |
| **Models** | Gemini 2.0/2.5 Flash, Gemini 1.5 Pro |
| **Use Case** | Enterprise backup, guaranteed availability |

**Pros**: No quota limits, enterprise SLA
**Cons**: Costs money (but we have $18K credits)

### Pricing

| Model | Context | Input Cost | Output Cost |
|-------|---------|------------|-------------|
| gemini-2.0-flash | 1M tokens | $0.10 | $0.40 |
| gemini-2.0-flash-lite | 1M tokens | $0.075 | $0.30 |
| gemini-2.5-flash | 1M tokens | $0.15 | $0.60 |
| gemini-1.5-pro | 1M tokens | $1.25 | $5.00 |
| gemini-2.5-pro | 1M tokens | $1.25 | $10.00 |

---

## Model Management

### Check Current Model

```bash
openclaw models status
```

### Switch Models

```bash
# CLI
openclaw models set google-vertex/gemini-2.5-pro
openclaw models set google-antigravity/gemini-3-pro-low  # Back to free

# Via Telegram/WhatsApp
"Switch to gemini-2.5-pro"
"Use Claude Sonnet"
```

---

## Configuration

### Vertex AI Service Account

1. Create service account in GCP Console
2. Grant `Vertex AI User` role
3. Download JSON key
4. Save to `~/.openclaw/keys/vertex-auth.json`

### Environment Variables

In `~/.config/systemd/user/openclaw-gateway.service.d/vertex.conf`:

```ini
[Service]
Environment="GOOGLE_APPLICATION_CREDENTIALS=/home/USER/.openclaw/keys/vertex-auth.json"
Environment="GOOGLE_CLOUD_PROJECT=linkhealth-care-2024"
Environment="GOOGLE_CLOUD_LOCATION=us-central1"
```

Apply changes:

```bash
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway
```

---

## Navigation

- Previous: [02-infrastructure.md](02-infrastructure.md)
- Next: [04-communication.md](04-communication.md)
