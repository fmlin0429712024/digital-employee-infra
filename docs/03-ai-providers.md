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
│  Priority 2: Google AI Studio (FREE with limits)           │
│  └─ gemini-1.5-pro                                         │
│                                                             │
│  ↓ If rate limited                                         │
│                                                             │
│  Priority 3: Vertex AI (PAID - Cheapest First)             │
│  └─ gemini-2.0-flash → gemini-2.5-flash → gemini-1.5-pro   │
│                                                             │
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

Vertex AI is the **critical paid backup** that guarantees 24/7 availability when free tiers are exhausted. This section covers all related components.

### Why Vertex AI Matters

| Scenario | Without Vertex AI | With Vertex AI |
|----------|-------------------|----------------|
| Antigravity quota exhausted | Agent goes offline | Automatic fallback |
| AI Studio rate limited | Agent goes offline | Automatic fallback |
| Enterprise SLA needed | Not possible | Guaranteed uptime |

### Component Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      VERTEX AI ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │  GCP Project │────▶│   VM + SA    │────▶│  Vertex AI   │    │
│  │              │     │              │     │    Models    │    │
│  │ linkhealth-  │     │ openclaw-    │     │              │    │
│  │ care-2024    │     │ desktop      │     │ gemini-2.0   │    │
│  │              │     │              │     │ gemini-2.5   │    │
│  │ $18K credits │     │ SA: default  │     │ gemini-1.5   │    │
│  └──────────────┘     └──────────────┘     └──────────────┘    │
│                              │                                   │
│                              ▼                                   │
│                    ┌──────────────────┐                         │
│                    │   IAM Role:      │                         │
│                    │ aiplatform.user  │                         │
│                    └──────────────────┘                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Identifiers

| Component | Identifier | Purpose |
|-----------|------------|---------|
| **GCP Project** | `linkhealth-care-2024` | Billing, resource container |
| **VM Instance** | `openclaw-desktop` | Runs the Digital Employee |
| **Region** | `us-central1-a` | VM and API location |
| **VM Service Account** | `51058313466-compute@developer.gserviceaccount.com` | Default Compute Engine SA |
| **IAM Role** | `roles/aiplatform.user` | Grants Vertex AI access |
| **Budget** | $18,000 GCP credits | Available for AI usage |

### Authentication Methods

There are two ways to authenticate with Vertex AI:

#### Method 1: VM Service Account (Recommended)

Best for dedicated VMs. Uses the VM's built-in identity.

**Setup:**
```bash
# Grant Vertex AI User role to VM's default service account
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SA_EMAIL" \
  --role="roles/aiplatform.user"
```

**Current Setup:**
```bash
# Project
linkhealth-care-2024

# VM Service Account
51058313466-compute@developer.gserviceaccount.com

# IAM Role Granted
roles/aiplatform.user ✅
```

**Pros**: No key files to manage, automatic credential rotation
**Cons**: Only works on GCP VMs

#### Method 2: Service Account Key File

For external machines or explicit control.

**Setup:**
1. Create service account in GCP Console
2. Grant `Vertex AI User` role
3. Download JSON key
4. Save to `~/.openclaw/keys/vertex-auth.json`

**Environment Variables** (in systemd override):
```ini
[Service]
Environment="GOOGLE_APPLICATION_CREDENTIALS=/home/USER/.openclaw/keys/vertex-auth.json"
Environment="GOOGLE_CLOUD_PROJECT=linkhealth-care-2024"
Environment="GOOGLE_CLOUD_LOCATION=us-central1"
```

**Pros**: Works anywhere, explicit control
**Cons**: Key rotation is manual, security risk if leaked

### Available Models

| Model | Context | Input Cost | Output Cost | Best For |
|-------|---------|------------|-------------|----------|
| `gemini-2.0-flash` | 1M tokens | $0.10 | $0.40 | Fast, cheap responses |
| `gemini-2.0-flash-lite` | 1M tokens | $0.075 | $0.30 | Ultra-cheap fallback |
| `gemini-2.5-flash` | 1M tokens | $0.15 | $0.60 | Balanced performance |
| `gemini-1.5-flash` | 1M tokens | $0.075 | $0.30 | Legacy fast model |
| `gemini-1.5-pro` | 1M tokens | $1.25 | $5.00 | Complex reasoning |
| `gemini-2.5-pro` | 1M tokens | $1.25 | $10.00 | Best quality |

### Fallback Order in OpenClaw

```json
{
  "model": {
    "primary": "google-antigravity/gemini-3-pro-low",
    "fallbacks": [
      "google-antigravity/gemini-3-flash",
      "google-antigravity/gemini-3-pro-high",
      "google-vertex/gemini-2.0-flash",
      "google-vertex/gemini-2.5-flash",
      "google-vertex/gemini-1.5-pro"
    ]
  }
}
```

### Testing Vertex AI

**Verify IAM permissions:**
```bash
gcloud projects get-iam-policy PROJECT_ID \
  --flatten="bindings[].members" \
  --format="table(bindings.role)" \
  --filter="bindings.members:SERVICE_ACCOUNT_EMAIL"
```

**Test API access from VM:**
```python
import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project="linkhealth-care-2024", location="us-central1")
model = GenerativeModel("gemini-2.0-flash")
response = model.generate_content("Say hello")
print(response.text)
```

**Check OpenClaw status:**
```bash
openclaw models status
openclaw models status --probe --probe-provider google-vertex
```

### Future Considerations

#### Multiple Projects

If you need to use different GCP projects:

```bash
# Switch project
export GOOGLE_CLOUD_PROJECT=other-project-id

# Or in systemd
Environment="GOOGLE_CLOUD_PROJECT=other-project-id"
```

#### Cross-Project Access

To access Vertex AI from a different project:

1. Create a service account in the Vertex AI project
2. Grant it `roles/aiplatform.user`
3. Grant the VM's service account permission to impersonate it
4. Use workload identity federation

#### Cost Monitoring

Track Vertex AI spending:
```bash
# View billing in GCP Console
https://console.cloud.google.com/billing

# Or via CLI
gcloud billing accounts list
gcloud billing projects describe PROJECT_ID
```

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

### List All Configured Models

```bash
openclaw models status --json | jq '.configuredModels'
```

---

## Quick Reference

| Provider | Auth Method | Cost | Models |
|----------|-------------|------|--------|
| `google-antigravity` | OAuth | FREE | Claude, Gemini 3 |
| `google` | API Key | FREE (limited) | Gemini 1.5 |
| `google-vertex` | Service Account / VM SA | PAID | Gemini 2.0/2.5/1.5 |

---

## Navigation

- Previous: [02-infrastructure.md](02-infrastructure.md)
- Next: [04-communication.md](04-communication.md)
