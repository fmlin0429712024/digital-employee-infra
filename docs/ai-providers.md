# AI Providers

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

## Tier 1: Antigravity (Primary)

| Attribute | Value |
|-----------|-------|
| **Auth** | OAuth |
| **Cost** | FREE |
| **Models** | Claude 3.5 Opus, Gemini 3 Pro, Claude Sonnet 4.5 |
| **Quota** | Resets every 5 hours |

## Tier 2: Google AI Studio (Backup)

| Attribute | Value |
|-----------|-------|
| **Auth** | API Key |
| **Cost** | FREE (with limits) |
| **Models** | Gemini 1.5 Pro |
| **Use Case** | Immediate failover when Antigravity exhausted |

## Tier 3: Vertex AI (Safety Net)

| Attribute | Value |
|-----------|-------|
| **Auth** | Service Account |
| **Cost** | Pay-per-use ($18K credits) |
| **Models** | Gemini 2.0/2.5 Flash, Gemini 1.5 Pro |
| **Use Case** | Enterprise backup, guaranteed availability |

### Vertex AI Pricing

| Model | Context | Input Cost | Output Cost |
|-------|---------|------------|-------------|
| gemini-2.0-flash | 1M tokens | $0.10 | $0.40 |
| gemini-2.0-flash-lite | 1M tokens | $0.075 | $0.30 |
| gemini-2.5-flash | 1M tokens | $0.15 | $0.60 |
| gemini-1.5-pro | 1M tokens | $1.25 | $5.00 |
| gemini-2.5-pro | 1M tokens | $1.25 | $10.00 |

## Switch Models

```bash
# Via CLI
openclaw models status
openclaw models set google-vertex/gemini-2.5-pro
openclaw models set google-antigravity/gemini-3-pro-low  # Back to free

# Via Telegram/WhatsApp
"Switch to gemini-2.5-pro"
"Use Claude Sonnet"
```

## Required Environment Variables

For Vertex AI to work, these must be set in the systemd service:

```bash
GOOGLE_APPLICATION_CREDENTIALS=/path/to/vertex-auth.json
GOOGLE_CLOUD_PROJECT=linkhealth-care-2024
GOOGLE_CLOUD_LOCATION=us-central1
```
